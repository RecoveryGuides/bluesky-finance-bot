#!/usr/bin/env python3
"""
BOT - Pełna lista tematów: finanse, survival, długi, zdrowie, kryzys
"""

import warnings
import os
warnings.filterwarnings('ignore')

import json
import random
import time
from datetime import datetime
from atproto import Client, models

# ============================================================================
# 🎯 PEŁNA LISTA TEMATÓW (jak wcześniej chciałeś)
# ============================================================================

TOPICS = {
    # Podstawowe finanse
    'money': ['money', 'cash', 'dollar', 'finance', 'financial', 'budget', 'spend', 'save', 'income', 'expense'],
    'debt': ['debt', 'credit', 'loan', 'owe', 'borrow', 'lend', 'payment', 'collection', 'creditor', 'interest'],
    
    # Survival/przetrwanie
    'survival': ['survival', 'prepper', 'emergency', 'crisis', 'prepared', 'disaster', 'shtf', 'bugout', 'homestead'],
    'crisis': ['crisis', 'emergency', 'disaster', 'collapse', 'breakdown', 'failure', 'meltdown'],
    
    # Zdrowie/medyczne
    'health': ['medical', 'hospital', 'doctor', 'health', 'bill', 'insurance', 'treatment', 'sick', 'illness', 'medicine'],
    'medical_debt': ['medical debt', 'hospital bill', 'insurance claim', 'healthcare cost', 'treatment payment'],
    
    # Praca/biznes
    'work': ['work', 'job', 'career', 'business', 'boss', 'employer', 'income', 'salary', 'unemployed', 'fired'],
    'business': ['business', 'company', 'startup', 'entrepreneur', 'selfemployed', 'freelance', 'sidehustle'],
    
    # Dom/rodzina
    'home': ['home', 'house', 'rent', 'mortgage', 'property', 'living', 'apartment', 'eviction', 'foreclosure'],
    'family': ['family', 'kids', 'children', 'parents', 'partner', 'relationship', 'marriage', 'divorce'],
    
    # Psychologia/stres
    'stress': ['stress', 'anxiety', 'worry', 'overwhelmed', 'pressure', 'mental', 'depression', 'burnout', 'exhausted'],
    'mindset': ['mindset', 'psychology', 'attitude', 'perspective', 'outlook', 'mentality', 'thinking'],
    
    # Przyszłość/planowanie
    'future': ['future', 'plan', 'goal', 'dream', 'retirement', 'savings', 'investment', 'wealth', 'rich', 'poor'],
    'planning': ['planning', 'strategy', 'preparation', 'organization', 'structure', 'system'],
    
    # Bezpieczeństwo/ochrona
    'security': ['security', 'safety', 'protection', 'defense', 'precaution', 'prevent', 'avoid', 'risk'],
    'safety': ['safety', 'secure', 'protected', 'shielded', 'guarded', 'insured', 'covered'],
    
    # Kryzys ekonomiczny
    'economic': ['economic', 'economy', 'recession', 'inflation', 'unemployment', 'poverty', 'bankruptcy'],
    'financial_crisis': ['financial crisis', 'money troubles', 'broke', 'struggling', 'paycheck to paycheck'],
    
    # Pomoc/wsparcie
    'help': ['help', 'advice', 'tip', 'suggestion', 'recommend', 'support', 'guide', 'assistance', 'aid'],
    'support': ['support', 'help', 'assist', 'guide', 'mentor', 'coach', 'advisor', 'consultant'],
    
    # Prawo/prawa
    'legal': ['legal', 'law', 'rights', 'contract', 'agreement', 'lawsuit', 'court', 'attorney', 'lawyer'],
    'rights': ['rights', 'entitlement', 'privilege', 'protection', 'guarantee', 'warranty'],
}

# Wszystkie słowa kluczowe
ALL_KEYWORDS = []
for keywords in TOPICS.values():
    ALL_KEYWORDS.extend(keywords)

print(f"📚 Loaded {len(TOPICS)} topics with {len(ALL_KEYWORDS)} keywords")

# ============================================================================
# 💬 KOMPLETNE KOMENTARZE DLA WSZYSTKICH TEMATÓW
# ============================================================================

COMMENTS = [
    # Finanse/długi
    "Stressed about debt? You're not alone. The first step is knowing your options.",
    "Credit card companies don't want you to know these negotiation scripts.",
    "Did you know you can often settle debt for 30-50% less? True story.",
    "That collection call tomorrow? Could be your opportunity to negotiate.",
    "The 'debt snowball' method changed my financial life. Anyone else tried it?",
    "Medical debt is negotiable. Most people don't know this.",
    "Your credit score can recover faster than you think with the right strategy.",
    "Stop the harassing calls with one certified letter template.",
    "Consolidation vs. settlement? The choice depends on your unique situation.",
    
    # Survival/kryzys
    "When crisis hits, having a plan is everything. Start with 72 hours of essentials.",
    "Survival isn't about doomsday - it's about being prepared for Tuesday's emergency.",
    "The most important survival tool isn't in your bugout bag - it's between your ears.",
    "Financial preparedness IS survival preparedness. No money = no options in crisis.",
    "Start with one week of food and water. That alone puts you ahead of 95% of people.",
    "Practice skills before you need them. Muscle memory works when adrenaline doesn't.",
    
    # Zdrowie/medyczne
    "Medical bills are the #1 cause of bankruptcy in America. Know your rights.",
    "Hospital bills are often negotiable. Always ask for an itemized statement.",
    "Medical debt collectors have strict rules they must follow. Learn the FDCPA.",
    "You can often negotiate payment plans directly with hospitals at 0% interest.",
    "Never pay a medical bill without verifying your insurance was billed correctly first.",
    
    # Praca/biznes
    "Side hustles aren't just for extra cash—they're your financial safety net.",
    "Multiple income streams = financial resilience. Don't rely on one source.",
    "When your job disappears, your skills don't. Always be learning marketable skills.",
    "Building a personal brand online creates opportunities when traditional jobs don't.",
    
    # Psychologia/mindset
    "Your money mindset determines your financial outcomes more than income.",
    "Scarcity vs. abundance thinking changes financial decisions dramatically.",
    "Money shame keeps people stuck. Talking about finances breaks the cycle.",
    "Financial confidence comes from knowledge, not from account balance.",
    "The comparison trap steals joy and wastes money.",
    "Gratitude practices reduce impulsive spending significantly.",
    
    # Planowanie/przyszłość
    "Where does your money really go each month? Most people underestimate by 30%.",
    "The 50/30/20 budget rule saved my finances. Anyone else use it?",
    "That 'emergency fund' advice? Non-negotiable. Start with $500, then $1000.",
    "Paying yourself first isn't selfish—it's smart financial planning.",
    "Financial automation changed everything for me. Bills on autopilot = peace.",
    
    # Kryzys/awaryjne
    "When money gets tight, prioritize: 1) Shelter 2) Utilities 3) Food 4) Transportation.",
    "The 72-hour financial crisis plan everyone should have.",
    "Negotiate EVERYTHING during hardship: rent, utilities, medical bills, credit cards.",
    "Cash is king during financial emergencies. Liquidate non-essentials quickly.",
    "Financial triage: What must be paid now vs. what can wait 30-60-90 days?",
    
    # Ogólne/uniwersalne
    "Progress, not perfection, is the goal with money.",
    "Small financial wins create momentum for bigger changes.",
    "Financial peace is possible at any income level.",
    "Your financial future is created by today's small decisions.",
    "Asking for help is strength, not weakness. Everyone needs support sometimes.",
]

print(f"💬 Loaded {len(COMMENTS)} comments")

# ============================================================================
# 🤖 RESZTA KODU (taka sama jak poprzednio, ale z pełnymi tematami)
# ============================================================================

class Bot:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE')
        self.password = os.getenv('BLUESKY_PASSWORD')
        self.client = None
        self.counter = 0
        
        # Pliki
        self.stats_file = 'stats.json'
        self.history_file = 'history.json'
        self.setup_files()
        
        print("🤖 BOT - Full topics version")
    
    def setup_files(self):
        """Tworzy pliki"""
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w') as f:
                json.dump({
                    'total': 0,
                    'links': 0,
                    'today': 0,
                    'created': datetime.now().isoformat()
                }, f)
        
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump({'posts': []}, f)
    
    def load_stats(self):
        """Ładuje statystyki"""
        try:
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
            
            # Reset daily
            today = datetime.now().strftime('%Y-%m-%d')
            if stats.get('last_date', '') != today:
                stats['today'] = 0
                stats['last_date'] = today
            
            return stats
        except:
            return {'total': 0, 'today': 0, 'links': 0}
    
    def save_stats(self, stats):
        """Zapisuje statystyki"""
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def load_history(self):
        """Ładuje historię"""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                return set(data.get('posts', []))
        except:
            return set()
    
    def save_history(self, post_uri):
        """Zapisuje do historii"""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
        except:
            data = {'posts': []}
        
        if post_uri not in data['posts']:
            data['posts'].append(post_uri)
            if len(data['posts']) > 300:  # Większy limit dla większej puli postów
                data['posts'] = data['posts'][-300:]
            
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
    
    def find_post(self):
        """Znajduje post - teraz z pełnymi tematami"""
        print("🔍 Finding post with full topics...")
        
        posts = []
        history = self.load_history()
        
        # Metoda 1: Timeline (główne źródło)
        try:
            timeline = self.client.get_timeline(limit=50)  # Więcej postów
            
            if hasattr(timeline, 'feed'):
                for item in timeline.feed:
                    try:
                        post = item.post
                        
                        if not hasattr(post, 'record'):
                            continue
                        
                        if post.author.did == self.client.me.did:
                            continue
                        
                        if post.uri in history:
                            continue
                        
                        if not hasattr(post, 'like_count') or post.like_count < 20:  # 20+ like'ów
                            continue
                        
                        text = post.record.text.lower()
                        
                        # Sprawdzaj WSZYSTKIE tematy
                        if any(k in text for k in ALL_KEYWORDS[:50]):  # Sprawdź pierwsze 50 słów
                            # Określ konkretny temat
                            detected_topic = 'general'
                            for topic_name, keywords in TOPICS.items():
                                if any(keyword in text for keyword in keywords[:5]):
                                    detected_topic = topic_name
                                    break
                            
                            posts.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count,
                                'score': post.like_count,
                                'topic': detected_topic
                            })
                            
                            if len(posts) >= 15:  # Więcej opcji do wyboru
                                break
                                
                    except:
                        continue
                        
        except Exception as e:
            print(f"⚠️  Timeline error: {str(e)[:40]}")
        
        # Metoda 2: Konta finansowe/survivalowe
        if len(posts) < 5:
            accounts = [
                'bloomberg.bsky.social',
                'wsj.bsky.social', 
                'cnbc.bsky.social',
                'survival.bsky.social',
                'prepper.bsky.social',
                'personalfinance.bsky.social'
            ]
            
            for acc in accounts[:4]:  # Sprawdź pierwsze 4
                try:
                    profile = self.client.get_profile(acc)
                    feed = self.client.get_author_feed(profile.did, limit=8)  # Więcej postów
                    
                    for item in feed.feed:
                        post = item.post
                        
                        if post.uri in history:
                            continue
                        
                        if not hasattr(post, 'like_count') or post.like_count < 15:
                            continue
                        
                        # Sprawdź temat
                        text = post.record.text.lower()
                        detected_topic = 'news'
                        for topic_name, keywords in TOPICS.items():
                            if any(keyword in text for keyword in keywords[:3]):
                                detected_topic = topic_name
                                break
                        
                        posts.append({
                            'uri': post.uri,
                            'cid': post.cid,
                            'text': post.record.text,
                            'author': post.author.handle,
                            'likes': post.like_count,
                            'score': post.like_count * 2,  # Wyższy score z kont tematycznych
                            'topic': detected_topic
                        })
                        
                except:
                    continue
        
        # Sortuj po score (popularność) i temacie
        if posts:
            # Priorytet: wyższy score, potem temat finansowy/survivalowy
            def sort_key(p):
                base_score = p['score']
                # Bonus dla tematów finansowych/survivalowych
                if p['topic'] in ['money', 'debt', 'survival', 'crisis', 'health', 'financial_crisis']:
                    base_score *= 1.5
                return base_score
            
            posts.sort(key=sort_key, reverse=True)
            print(f"✅ Found {len(posts)} posts across {len(set(p['topic'] for p in posts))} topics")
            return posts[:5]  # Zwróć top 5
        
        return []
    
    def make_comment(self, topic='general'):
        """Tworzy komentarz dopasowany do tematu"""
        self.counter += 1
        
        # Wybierz komentarze dla tematu
        if topic in ['money', 'debt', 'financial_crisis', 'economic']:
            relevant = [c for c in COMMENTS if any(word in c.lower() for word in ['debt', 'money', 'financial', 'credit'])]
        elif topic in ['survival', 'crisis', 'emergency', 'security']:
            relevant = [c for c in COMMENTS if any(word in c.lower() for word in ['survival', 'crisis', 'emergency', 'prepared'])]
        elif topic in ['health', 'medical_debt']:
            relevant = [c for c in COMMENTS if any(word in c.lower() for word in ['medical', 'hospital', 'bill', 'health'])]
        elif topic in ['stress', 'mindset']:
            relevant = [c for c in COMMENTS if any(word in c.lower() for word in ['stress', 'mindset', 'psychology', 'mental'])]
        else:
            relevant = COMMENTS
        
        if not relevant:
            relevant = COMMENTS
        
        comment = random.choice(relevant)
        
        # Link co 5 komentarz
        if self.counter % 5 == 0:
            link = "https://www.payhip.com/daveprime"
            comment = f"{comment}\n\n🔗 Step-by-step guides: {link}"
        
        return comment
    
    def post_comment(self, post_uri, post_cid, comment):
        """Publikuje komentarz"""
        try:
            # Losowe opóźnienie 30-90 sekund
            time.sleep(random.randint(30, 90))
            
            ref = {'uri': post_uri, 'cid': post_cid}
            
            self.client.send_post(
                text=comment,
                reply_to={'root': ref, 'parent': ref}
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Post error: {str(e)[:60]}")
            
            # Alternative method
            try:
                self.client.send_post(
                    text=comment,
                    reply_to=models.AppBskyFeedPost.ReplyRef(
                        parent=models.create_strong_ref(post_uri),
                        root=models.create_strong_ref(post_uri)
                    )
                )
                return True
            except:
                return False
    
    def run(self):
        """Główna funkcja"""
        print("="*60)
        print("🚀 BOT STARTING - FULL TOPICS VERSION")
        print("="*60)
        
        # Sprawdź dane
        if not self.handle or not self.password:
            print("❌ No credentials")
            return
        
        # Limit dzienny
        stats = self.load_stats()
        if stats.get('today', 0) >= 12:
            print("⏹️ Daily limit reached (12 comments)")
            return
        
        # Połącz
        try:
            self.client = Client()
            self.client.login(self.handle, self.password)
            print(f"✅ Connected as: {self.handle}")
        except Exception as e:
            print(f"❌ Connect error: {e}")
            return
        
        # Losowe opóźnienie
        time.sleep(random.randint(30, 60))
        
        # Znajdź post
        posts = self.find_post()
        
        if not posts:
            print("💔 No suitable posts found")
            return
        
        # Weź najlepszy
        post = posts[0]
        print(f"\n🏆 Selected post:")
        print(f"   👤 @{post['author']}")
        print(f"   👍 {post['likes']} likes")
        print(f"   🏷️  Topic: {post['topic']}")
        print(f"   📄 {post['text'][:80]}...")
        
        # Stwórz dopasowany komentarz
        comment = self.make_comment(post['topic'])
        print(f"   💬 Comment ({post['topic']}): {comment[:70]}...")
        
        # Publikuj
        success = self.post_comment(post['uri'], post['cid'], comment)
        
        if not success:
            print("   ❌ Failed to post")
            return
        
        # Zapisz do historii
        self.save_history(post['uri'])
        
        # Aktualizuj statystyki
        stats['total'] = stats.get('total', 0) + 1
        stats['today'] = stats.get('today', 0) + 1
        
        if self.counter % 5 == 0:
            stats['links'] = stats.get('links', 0) + 1
            print("   🔗 Shop link added!")
        
        self.save_stats(stats)
        
        # Podsumowanie
        print("\n" + "="*60)
        print("✅ BOT COMPLETE")
        print("="*60)
        print(f"💬 Total comments: {stats['total']}")
        print(f"📅 Today: {stats['today']}/12")
        print(f"🔗 Shop links: {stats['links']}")
        print(f"🎯 Next shop link in: {5 - (self.counter % 5)} comments")
        print(f"⏰ Next run: In 2 hours")
        print("="*60)

# Uruchom
if __name__ == '__main__':
    bot = Bot()
    bot.run()
