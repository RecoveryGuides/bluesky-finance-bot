#!/usr/bin/env python3
"""
BOT - Unika duplikatów, komentuje różne posty z różnych kont
"""

import warnings
import os
warnings.filterwarnings('ignore')

import json
import random
import time
from datetime import datetime, timedelta
from atproto import Client, models
from collections import defaultdict

# ============================================================================
# 🎯 PEŁNA LISTA TEMATÓW
# ============================================================================

TOPICS = {
    'money': ['money', 'cash', 'finance', 'budget', 'income', 'expense'],
    'debt': ['debt', 'credit', 'loan', 'owe', 'interest'],
    'survival': ['survival', 'emergency', 'crisis', 'prepared'],
    'health': ['health', 'medical', 'hospital', 'doctor', 'insurance'],
    'work': ['work', 'job', 'career', 'salary', 'unemployed'],
    'home': ['home', 'house', 'rent', 'mortgage', 'eviction'],
    'stress': ['stress', 'anxiety', 'worry', 'pressure'],
    'future': ['future', 'plan', 'goal', 'savings', 'investment'],
    'security': ['security', 'safety', 'protection', 'risk'],
    'economic': ['economic', 'economy', 'recession', 'inflation'],
}

ALL_KEYWORDS = []
for keywords in TOPICS.values():
    ALL_KEYWORDS.extend(keywords)

print(f"📚 Loaded {len(TOPICS)} topics with {len(ALL_KEYWORDS)} keywords")

# ============================================================================
# 💬 KOMENTARZE
# ============================================================================

COMMENTS = [
    # Finanse/długi
    "Stressed about debt? You're not alone. The first step is knowing your options.",
    "Credit card companies don't want you to know these negotiation scripts.",
    "Medical debt is negotiable. Most people don't know this.",
    "Your credit score can recover faster than you think with the right strategy.",
    
    # Survival/kryzys
    "When crisis hits, having a plan is everything. Start with 72 hours of essentials.",
    "Survival isn't about doomsday - it's about being prepared for Tuesday's emergency.",
    "Financial preparedness IS survival preparedness. No money = no options in crisis.",
    
    # Zdrowie/medyczne
    "Medical bills are often negotiable. Always ask for an itemized statement.",
    "Medical debt collectors have strict rules they must follow.",
    "You can often negotiate payment plans directly with hospitals at 0% interest.",
    
    # Praca/biznes
    "Side hustles aren't just for extra cash—they're your financial safety net.",
    "Multiple income streams = financial resilience. Don't rely on one source.",
    
    # Psychologia/mindset
    "Your money mindset determines your financial outcomes more than income.",
    "Money shame keeps people stuck. Talking about finances breaks the cycle.",
    
    # Planowanie
    "Where does your money really go each month? Most people underestimate by 30%.",
    "The 50/30/20 budget rule saved my finances. Anyone else use it?",
    
    # Kryzys
    "When money gets tight, prioritize: 1) Shelter 2) Utilities 3) Food 4) Transportation.",
    "Negotiate EVERYTHING during hardship: rent, utilities, medical bills, credit cards.",
    
    # Ogólne
    "Progress, not perfection, is the goal with money.",
    "Small financial wins create momentum for bigger changes.",
]

print(f"💬 Loaded {len(COMMENTS)} comments")

# ============================================================================
# 🤖 BOT Z SYSTEMEM ANTY-DUPLIKATÓW
# ============================================================================

class SmartBot:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE')
        self.password = os.getenv('BLUESKY_PASSWORD')
        self.client = None
        
        # Pliki z danymi
        self.stats_file = 'stats.json'
        self.history_file = 'history.json'
        self.authors_file = 'authors.json'
        
        self.setup_files()
        print("🤖 SMART BOT - Anti-duplicate system")
    
    def setup_files(self):
        """Tworzy pliki z danymi"""
        default_stats = {
            'total_comments': 0,
            'today_comments': 0,
            'last_date': datetime.now().strftime('%Y-%m-%d'),
            'unique_authors': 0,
            'links_posted': 0
        }
        
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w') as f:
                json.dump(default_stats, f)
        
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump({'posts': [], 'last_cleanup': datetime.now().isoformat()}, f)
        
        if not os.path.exists(self.authors_file):
            with open(self.authors_file, 'w') as f:
                json.dump({'authors': {}, 'recent_authors': []}, f)
    
    def load_stats(self):
        """Ładuje statystyki"""
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except:
            return {'total_comments': 0, 'today_comments': 0}
    
    def save_stats(self, stats):
        """Zapisuje statystyki"""
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def load_history(self):
        """Ładuje historię postów"""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                return set(data.get('posts', []))
        except:
            return set()
    
    def save_to_history(self, post_uri, author_handle, topic):
        """Zapisuje post do historii"""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
        except:
            data = {'posts': [], 'last_cleanup': datetime.now().isoformat()}
        
        # Dodaj nowy post
        entry = {
            'uri': post_uri,
            'author': author_handle,
            'topic': topic,
            'timestamp': datetime.now().isoformat()
        }
        
        if entry not in data['posts']:
            data['posts'].append(entry)
            
            # Ogranicz do 500 wpisów
            if len(data['posts']) > 500:
                data['posts'] = data['posts'][-500:]
            
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        # Dodaj autora do listy ostatnich
        self.update_authors_file(author_handle)
    
    def load_authors(self):
        """Ładuje dane o autorach"""
        try:
            with open(self.authors_file, 'r') as f:
                return json.load(f)
        except:
            return {'authors': {}, 'recent_authors': []}
    
    def update_authors_file(self, author_handle):
        """Aktualizuje listę autorów"""
        try:
            with open(self.authors_file, 'r') as f:
                data = json.load(f)
        except:
            data = {'authors': {}, 'recent_authors': []}
        
        # Dodaj do ostatnich autorów
        if author_handle not in data['recent_authors']:
            data['recent_authors'].append(author_handle)
        
        # Ogranicz do 50 ostatnich autorów
        if len(data['recent_authors']) > 50:
            data['recent_authors'] = data['recent_authors'][-50:]
        
        # Zwiększ licznik dla autora
        if author_handle not in data['authors']:
            data['authors'][author_handle] = 0
        data['authors'][author_handle] += 1
        
        with open(self.authors_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def is_author_recent(self, author_handle):
        """Sprawdza czy autor był ostatnio komentowany"""
        data = self.load_authors()
        return author_handle in data['recent_authors'][-10:]  # Ostatnie 10 autorów
    
    def should_skip_post(self, post_uri, author_handle, text):
        """Decyduje czy pominąć post"""
        # 1. Sprawdź czy już komentowany
        history = self.load_history()
        for entry in history:
            if entry['uri'] == post_uri:
                return True
        
        # 2. Sprawdź czy ten autor był ostatnio komentowany
        if self.is_author_recent(author_handle):
            print(f"   ⏩ Skipping - author @{author_handle} was recently commented")
            return True
        
        # 3. Sprawdź czy to spam/za krótkie
        if len(text.split()) < 5:
            return True
        
        # 4. Sprawdź czy zawiera słowa kluczowe
        text_lower = text.lower()
        if not any(keyword in text_lower for keyword in ALL_KEYWORDS[:30]):
            return False  # Nie skaczemy - może być ogólny post
        
        return False
    
    def find_diverse_posts(self):
        """Szuka RÓŻNYCH postów z RÓŻNYCH kont"""
        print("🔍 Searching for diverse posts...")
        
        all_posts = []
        history = self.load_history()
        recent_authors = self.load_authors()['recent_authors']
        
        # STRATEGIA 1: Timeline z różnych kont
        try:
            timeline = self.client.get_timeline(limit=100)
            
            if hasattr(timeline, 'feed'):
                for item in timeline.feed:
                    try:
                        post = item.post
                        
                        if not hasattr(post, 'record'):
                            continue
                        
                        # Pomiń swoje posty
                        if post.author.did == self.client.me.did:
                            continue
                        
                        author_handle = post.author.handle
                        post_uri = post.uri
                        text = post.record.text
                        
                        # Sprawdź czy pomijać
                        if self.should_skip_post(post_uri, author_handle, text):
                            continue
                        
                        # Wymagaj minimalnej popularności (opcjonalne)
                        likes = getattr(post, 'like_count', 0)
                        if likes < 3:  # Bardzo niski próg
                            continue
                        
                        # Określ temat
                        text_lower = text.lower()
                        topic = 'general'
                        for topic_name, keywords in TOPICS.items():
                            if any(keyword in text_lower for keyword in keywords):
                                topic = topic_name
                                break
                        
                        # Oblicz score (różne czynniki)
                        score = likes
                        
                        # Bonus za nowego autora
                        if author_handle not in recent_authors:
                            score += 50
                        
                        # Bonus za temat finansowy
                        if topic in ['money', 'debt', 'economic']:
                            score += 30
                        
                        # Bonus za świeżość posta
                        if hasattr(post, 'indexed_at'):
                            score += 10
                        
                        all_posts.append({
                            'uri': post_uri,
                            'cid': post.cid,
                            'text': text,
                            'author': author_handle,
                            'likes': likes,
                            'topic': topic,
                            'score': score,
                            'source': 'timeline'
                        })
                        
                    except Exception as e:
                        continue
                        
            print(f"   📊 Timeline: {len([p for p in all_posts if p['source'] == 'timeline'])} posts")
            
        except Exception as e:
            print(f"   ⚠️ Timeline error: {str(e)[:40]}")
        
        # STRATEGIA 2: Wyszukiwanie po słowach kluczowych
        if len(all_posts) < 15:
            keywords_to_search = random.sample(ALL_KEYWORDS, min(5, len(ALL_KEYWORDS)))
            
            for keyword in keywords_to_search:
                try:
                    results = self.client.app.bsky.feed.search_posts({
                        'q': keyword,
                        'limit': 15
                    })
                    
                    if hasattr(results, 'posts'):
                        for post in results.posts:
                            try:
                                author_handle = post.author.handle
                                post_uri = post.uri
                                text = post.record.text
                                
                                if self.should_skip_post(post_uri, author_handle, text):
                                    continue
                                
                                likes = getattr(post, 'like_count', 0)
                                if likes < 2:
                                    continue
                                
                                # Określ temat
                                text_lower = text.lower()
                                topic = 'general'
                                for topic_name, keywords in TOPICS.items():
                                    if any(k in text_lower for k in keywords):
                                        topic = topic_name
                                        break
                                
                                score = likes * 2  # Większy bonus za wyszukiwanie
                                
                                if author_handle not in recent_authors:
                                    score += 100  # Duży bonus za nowego autora
                                
                                all_posts.append({
                                    'uri': post_uri,
                                    'cid': post.cid,
                                    'text': text,
                                    'author': author_handle,
                                    'likes': likes,
                                    'topic': topic,
                                    'score': score,
                                    'source': 'search',
                                    'keyword': keyword
                                })
                                
                            except:
                                continue
                                
                except:
                    continue
        
        print(f"   📈 Total candidates: {len(all_posts)} posts")
        
        # STRATEGIA 3: Konta tematyczne (jeśli mało)
        if len(all_posts) < 10:
            topical_accounts = [
                'bloomberg.bsky.social',
                'wsj.bsky.social',
                'personalfinance.bsky.social',
                'getfinanced.bsky.social',
                'money.bsky.social'
            ]
            
            for account in random.sample(topical_accounts, min(3, len(topical_accounts))):
                try:
                    profile = self.client.get_profile(account)
                    feed = self.client.get_author_feed(profile.did, limit=8)
                    
                    if hasattr(feed, 'feed'):
                        for item in feed.feed:
                            post = item.post
                            author_handle = post.author.handle
                            post_uri = post.uri
                            
                            if self.should_skip_post(post_uri, author_handle, post.record.text):
                                continue
                            
                            likes = getattr(post, 'like_count', 0)
                            
                            all_posts.append({
                                'uri': post_uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': author_handle,
                                'likes': likes,
                                'topic': 'finance_news',
                                'score': likes + 20,
                                'source': 'topical_account'
                            })
                            
                except:
                    continue
        
        # Filtruj i sortuj
        if all_posts:
            # Usuń duplikaty po URI
            unique_posts = []
            seen_uris = set()
            for post in all_posts:
                if post['uri'] not in seen_uris:
                    seen_uris.add(post['uri'])
                    unique_posts.append(post)
            
            print(f"   ✨ Unique posts: {len(unique_posts)}")
            
            # Sortuj po score (najlepsze na górze)
            unique_posts.sort(key=lambda x: x['score'], reverse=True)
            
            # Zwróć różne autorów
            final_selection = []
            seen_authors = set()
            
            for post in unique_posts:
                if post['author'] not in seen_authors:
                    seen_authors.add(post['author'])
                    final_selection.append(post)
                
                if len(final_selection) >= 5:
                    break
            
            # Jeśli za mało różnych autorów, dodaj kolejne posty
            if len(final_selection) < 3:
                for post in unique_posts:
                    if post not in final_selection:
                        final_selection.append(post)
                    
                    if len(final_selection) >= 3:
                        break
            
            print(f"   🎯 Final selection: {len(final_selection)} posts from {len(seen_authors)} authors")
            return final_selection
        
        return []
    
    def get_comment_for_topic(self, topic):
        """Zwraca komentarz dopasowany do tematu"""
        if topic in ['money', 'debt', 'economic']:
            relevant = [c for c in COMMENTS if any(w in c.lower() for w in ['debt', 'money', 'credit', 'financial'])]
        elif topic in ['survival', 'security']:
            relevant = [c for c in COMMENTS if any(w in c.lower() for w in ['survival', 'crisis', 'emergency', 'prepared'])]
        elif topic in ['health']:
            relevant = [c for c in COMMENTS if any(w in c.lower() for w in ['medical', 'hospital', 'health'])]
        elif topic in ['work', 'home']:
            relevant = [c for c in COMMENTS if any(w in c.lower() for w in ['work', 'job', 'home', 'rent'])]
        elif topic in ['stress']:
            relevant = [c for c in COMMENTS if any(w in c.lower() for w in ['stress', 'mindset', 'mental'])]
        elif topic in ['future']:
            relevant = [c for c in COMMENTS if any(w in c.lower() for w in ['future', 'plan', 'savings'])]
        else:
            relevant = COMMENTS
        
        return random.choice(relevant) if relevant else random.choice(COMMENTS)
    
    def post_reply(self, post_uri, post_cid, comment_text):
        """Publikuje odpowiedź"""
        try:
            # Losowe opóźnienie 45-120 sekund
            delay = random.randint(45, 120)
            print(f"   ⏳ Waiting {delay} seconds before posting...")
            time.sleep(delay)
            
            ref = {'uri': post_uri, 'cid': post_cid}
            
            self.client.send_post(
                text=comment_text,
                reply_to={'root': ref, 'parent': ref}
            )
            
            return True
            
        except Exception as e:
            print(f"   ❌ Post error: {str(e)[:60]}")
            return False
    
    def cleanup_old_data(self):
        """Czyści stare dane"""
        try:
            # Historia
            with open(self.history_file, 'r') as f:
                history_data = json.load(f)
            
            # Usuń posty starsze niż 7 dni
            week_ago = datetime.now() - timedelta(days=7)
            history_data['posts'] = [
                p for p in history_data['posts'] 
                if datetime.fromisoformat(p['timestamp']) > week_ago
            ]
            
            with open(self.history_file, 'w') as f:
                json.dump(history_data, f, indent=2)
            
            # Autorzy
            with open(self.authors_file, 'r') as f:
                authors_data = json.load(f)
            
            # Ogranicz ostatnich autorów
            if len(authors_data['recent_authors']) > 50:
                authors_data['recent_authors'] = authors_data['recent_authors'][-50:]
            
            with open(self.authors_file, 'w') as f:
                json.dump(authors_data, f, indent=2)
                
            print("   🧹 Cleaned up old data")
            
        except Exception as e:
            print(f"   ⚠️ Cleanup error: {e}")
    
    def run(self):
        """Główna funkcja bota"""
        print("="*60)
        print("🚀 SMART BOT STARTING - DIVERSITY FOCUS")
        print("="*60)
        
        # Sprawdź dane logowania
        if not self.handle or not self.password:
            print("❌ Missing BLUESKY_HANDLE or BLUESKY_PASSWORD")
            return
        
        # Załaduj statystyki i sprawdź limit
        stats = self.load_stats()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if stats.get('last_date') != today:
            stats['today_comments'] = 0
            stats['last_date'] = today
        
        if stats.get('today_comments', 0) >= 8:
            print(f"⏹️ Daily limit reached: {stats['today_comments']}/8")
            return
        
        # Połącz z BlueSky
        try:
            self.client = Client()
            self.client.login(self.handle, self.password)
            print(f"✅ Connected as: @{self.handle}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return
        
        # Oczyść stare dane
        self.cleanup_old_data()
        
        # Losowe opóźnienie przed rozpoczęciem
        initial_delay = random.randint(30, 90)
        print(f"⏳ Initial delay: {initial_delay} seconds")
        time.sleep(initial_delay)
        
        # Znajdź RÓŻNE posty
        posts = self.find_diverse_posts()
        
        if not posts:
            print("💔 No suitable posts found")
            return
        
        # Wybierz NAJLEPSZY post (różny autor, dobry temat)
        selected_post = None
        authors_data = self.load_authors()
        
        for post in posts:
            if not self.is_author_recent(post['author']):
                selected_post = post
                break
        
        if not selected_post:
            selected_post = posts[0]  # Weź najlepszy ogólnie
        
        print(f"\n🎯 SELECTED POST:")
        print(f"   👤 Author: @{selected_post['author']}")
        print(f"   👍 Likes: {selected_post['likes']}")
        print(f"   🏷️  Topic: {selected_post['topic']}")
        print(f"   📝 Preview: {selected_post['text'][:100]}...")
        print(f"   🔍 Source: {selected_post.get('source', 'unknown')}")
        
        # Stwórz komentarz
        comment = self.get_comment_for_topic(selected_post['topic'])
        print(f"   💬 Comment: {comment[:80]}...")
        
        # Publikuj
        success = self.post_reply(
            selected_post['uri'],
            selected_post['cid'],
            comment
        )
        
        if not success:
            print("   ❌ Failed to post comment")
            return
        
        # Zapisz do historii
        self.save_to_history(
            selected_post['uri'],
            selected_post['author'],
            selected_post['topic']
        )
        
        # Aktualizuj statystyki
        stats['total_comments'] = stats.get('total_comments', 0) + 1
        stats['today_comments'] = stats.get('today_comments', 0) + 1
        stats['unique_authors'] = len(authors_data['authors'])
        
        # Link co 4 komentarz
        if stats['total_comments'] % 4 == 0:
            stats['links_posted'] = stats.get('links_posted', 0) + 1
        
        self.save_stats(stats)
        
        # Podsumowanie
        print("\n" + "="*60)
        print("✅ BOT COMPLETE - DIVERSITY SYSTEM")
        print("="*60)
        print(f"📊 Statistics:")
        print(f"   Total comments: {stats['total_comments']}")
        print(f"   Today: {stats['today_comments']}/8")
        print(f"   Unique authors: {stats['unique_authors']}")
        print(f"   Next link in: {4 - (stats['total_comments'] % 4)} comments")
        print(f"⏰ Next run: In 2 hours")
        print("="*60)

# Uruchom
if __name__ == '__main__':
    bot = SmartBot()
    bot.run()
