#!/usr/bin/env python3
"""
🚀 FINANCE GROWTH BOT FOR BLUESKY - WORKING VERSION
Bot komentuje posty o finansach i co 5 komentarz dodaje link do sklepu
"""

import json
import random
import time
import os
from datetime import datetime
from atproto import Client, models

# ============================================================================
# 📝 BAZA WIEDZY: 50 NAJLEPSZYCH SENTENCJI FINANSOWYCH
# ============================================================================

FINANCIAL_SENTENCES = [
    # Debt & Credit (15 sentences)
    "Stressed about debt? The first step is knowing your options.",
    "Credit card companies don't want you to know these negotiation scripts.",
    "Did you know you can often settle debt for 30-50% less?",
    "That collection call could be your opportunity to negotiate.",
    "The 'debt snowball' method changed my financial life.",
    "Medical debt is negotiable. Most people don't know this.",
    "Your credit score can recover faster than you think.",
    "Stop the harassing calls with one certified letter template.",
    "Consolidation vs. settlement? Depends on your unique situation.",
    "Financial emergencies happen. Having a plan B is non-negotiable.",
    "Bankruptcy isn't failure—it's a legal financial tool when needed.",
    "Minimum payments keep you in debt for decades. Break the cycle.",
    "Balance transfer cards can be smart IF you have a payoff plan.",
    "Debt collectors have quotas too. Use this to your advantage.",
    "The Fair Debt Collection Practices Act protects you. Learn your rights.",
    
    # Money Management (15 sentences)
    "Where does your money really go? Most people underestimate by 30%.",
    "The 50/30/20 budget rule saved my finances. Anyone else use it?",
    "Cash envelopes aren't old-school—they're psychologically effective.",
    "Subscription creep is real. $10 here, $15 there adds up to hundreds yearly.",
    "That 'emergency fund' advice? Non-negotiable. Start with $500.",
    "Paying yourself first isn't selfish—it's smart financial planning.",
    "Financial automation changed everything. Bills on autopilot = peace.",
    "Side hustles aren't just for extra cash—they're your financial safety net.",
    "The latte factor is real. But don't deprive yourself—budget for treats.",
    "Zero-based budgeting: Every dollar has a job. Game-changer for control.",
    "Sinking funds for irregular expenses prevent financial surprises.",
    "Weekly money dates keep finances on track.",
    "Financial infidelity damages relationships. Transparency is key.",
    "Living below your means is the ultimate financial freedom.",
    "Financial margin = options. No margin = stress.",
    
    # Crisis & Survival (10 sentences)
    "When money gets tight: 1) Shelter 2) Utilities 3) Food 4) Transportation.",
    "The 72-hour financial crisis plan everyone should have.",
    "Survival mode budgeting focuses on needs, cuts all wants temporarily.",
    "$30 can feed one person for a week with strategic shopping.",
    "Financial first aid: Stop bleeding cash before long-term issues.",
    "Crisis doesn't last forever. Temporary measures for temporary problems.",
    "Negotiate EVERYTHING during hardship: rent, utilities, medical bills.",
    "Cash is king during financial emergencies. Liquidate non-essentials quickly.",
    "Financial triage: What must be paid now vs. what can wait?",
    "One month's expenses saved changes everything during job loss.",
    
    # Mindset & Psychology (10 sentences)
    "Your money mindset determines outcomes more than income.",
    "Scarcity vs. abundance thinking changes financial decisions dramatically.",
    "Money shame keeps people stuck. Talking about finances breaks the cycle.",
    "Financial literacy is the great equalizer in modern society.",
    "The comparison trap steals joy and wastes money.",
    "Gratitude practices reduce impulsive spending significantly.",
    "Financial boundaries are healthy—with family, friends, and yourself.",
    "Financial confidence comes from knowledge, not account balance.",
    "Financial peace is possible at any income level.",
    "Your financial future is created by today's small decisions."
]

# ============================================================================
# 🤖 GŁÓWNA KLASA BOTA
# ============================================================================

class FinanceGrowthBot:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE', '')
        self.password = os.getenv('BLUESKY_PASSWORD', '')
        self.client = None
        
        # Inicjalizacja plików
        self.initialize_files()
        
        # Liczniki
        self.comment_counter = 0
        self.comments_today = 0
        
        print(f"🤖 Finance Growth Bot v4.0")
        print(f"📊 Załadowano {len(FINANCIAL_SENTENCES)} sentencji finansowych")
    
    def initialize_files(self):
        """Tworzy pliki danych jeśli nie istnieją"""
        # Plik statystyk
        if not os.path.exists('bot_stats.json'):
            stats = {
                'total_comments': 0,
                'comments_today': 0,
                'shop_links_posted': 0,
                'last_reset': datetime.now().isoformat(),
                'created': datetime.now().isoformat(),
                'version': '4.0'
            }
            with open('bot_stats.json', 'w') as f:
                json.dump(stats, f, indent=2)
            print("📁 Utworzono bot_stats.json")
        
        # Plik historii komentarzy
        if not os.path.exists('comments_history.json'):
            with open('comments_history.json', 'w') as f:
                json.dump([], f)
            print("📁 Utworzono comments_history.json")
    
    def load_stats(self):
        """Ładuje statystyki"""
        try:
            with open('bot_stats.json', 'r') as f:
                return json.load(f)
        except:
            return {'total_comments': 0, 'comments_today': 0}
    
    def save_stats(self, stats):
        """Zapisuje statystyki"""
        with open('bot_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
    
    def load_commented_posts(self):
        """Ładuje listę już skomentowanych postów"""
        try:
            with open('comments_history.json', 'r') as f:
                history = json.load(f)
            return {item['post_uri'] for item in history if 'post_uri' in item}
        except:
            return set()
    
    def save_comment(self, post_uri, comment_text):
        """Zapisuje komentarz do historii"""
        try:
            with open('comments_history.json', 'r') as f:
                history = json.load(f)
        except:
            history = []
        
        history.append({
            'post_uri': post_uri,
            'comment': comment_text[:200],
            'timestamp': datetime.now().isoformat(),
            'comment_number': self.comment_counter
        })
        
        # Zachowaj tylko ostatnie 100 komentarzy
        if len(history) > 100:
            history = history[-100:]
        
        with open('comments_history.json', 'w') as f:
            json.dump(history, f)
    
    # ============================================================================
    # 🎯 LOGIKA WYSZUKIWANIA POSTÓW
    # ============================================================================
    
    def search_finance_posts(self):
        """Wyszukuje posty o finansach"""
        print("🔍 Szukam postów o finansach...")
        
        posts_found = []
        commented_posts = self.load_commented_posts()
        
        try:
            # METODA 1: Przeszukaj feed (najprostsze)
            print("  📰 Sprawdzam feed...")
            timeline = self.client.get_timeline(limit=50)
            
            for item in timeline.feed:
                post = item.post
                
                # Podstawowe filtry
                if post.uri in commented_posts:
                    continue
                
                if post.author.did == self.client.me.did:
                    continue
                
                if post.like_count < 15:  # Min 15 polubień
                    continue
                
                # Sprawdź czy to temat finansowy
                post_text = post.record.text.lower()
                finance_keywords = [
                    'debt', 'credit', 'money', 'finance', 'budget',
                    'loan', 'mortgage', 'bank', 'cash', 'income',
                    'bill', 'financial', 'crisis', 'emergency'
                ]
                
                if any(keyword in post_text for keyword in finance_keywords):
                    posts_found.append({
                        'uri': post.uri,
                        'cid': post.cid,
                        'text': post.record.text,
                        'author': post.author.handle,
                        'likes': post.like_count,
                        'replies': post.reply_count,
                        'reposts': post.repost_count
                    })
                    
                    print(f"    ✅ Znaleziono: @{post.author.handle} ({post.like_count} 👍)")
                    
                    if len(posts_found) >= 5:  # Max 5 postów
                        break
            
            # METODA 2: Wyszukiwanie (jeśli feed nie wystarczy)
            if len(posts_found) < 2:
                print("  🔎 Wyszukuję po hashtagach...")
                search_terms = ['debt', 'money', 'budget', 'finance']
                
                for term in search_terms:
                    try:
                        # Poprawna składnia API
                        results = self.client.app.bsky.feed.search_posts(
                            params={'q': term, 'limit': 10}
                        )
                        
                        for post in results.posts:
                            if len(posts_found) >= 5:
                                break
                            
                            if post.uri in commented_posts:
                                continue
                            
                            if post.author.did == self.client.me.did:
                                continue
                            
                            if post.like_count < 10:
                                continue
                            
                            posts_found.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count
                            })
                            
                            print(f"    🔍 '{term}': @{post.author.handle}")
                            
                    except Exception as e:
                        print(f"    ⚠️  Błąd wyszukiwania '{term}': {str(e)[:50]}")
                        continue
        
        except Exception as e:
            print(f"❌ Błąd wyszukiwania postów: {e}")
        
        print(f"🎯 Znaleziono {len(posts_found)} postów")
        return posts_found
    
    # ============================================================================
    # 💬 GENEROWANIE KOMENTARZY
    # ============================================================================
    
    def should_add_shop_link(self):
        """Czy dodać link do sklepu? (co 5 komentarz)"""
        self.comment_counter += 1
        return self.comment_counter % 5 == 0
    
    def format_comment(self, base_comment):
        """Formatuje komentarz, dodaje link jeśli trzeba"""
        shop_link = "https://www.payhip.com/daveprime"
        
        if self.should_add_shop_link():
            ctas = [
                f"\n\n👉 Praktyczne przewodniki: {shop_link}",
                f"\n\n🔗 Szablony i skrypty: {shop_link}",
                f"\n\n📘 Krok po kroku: {shop_link}"
            ]
            return base_comment + random.choice(ctas)
        
        return base_comment
    
    def generate_relevant_comment(self, post_text=""):
        """Generuje komentarz pasujący do tematu posta"""
        if post_text:
            post_lower = post_text.lower()
            
            # Wybierz odpowiednie sentencje
            if any(word in post_lower for word in ['debt', 'owe', 'collection', 'credit']):
                # Temat: długi
                category = [s for s in FINANCIAL_SENTENCES if any(
                    w in s.lower() for w in ['debt', 'credit', 'owe', 'collection']
                )]
            elif any(word in post_lower for word in ['budget', 'save', 'spend', 'money']):
                # Temat: budżet
                category = [s for s in FINANCIAL_SENTENCES if any(
                    w in s.lower() for w in ['budget', 'save', 'money', 'spend']
                )]
            elif any(word in post_lower for word in ['crisis', 'emergency', 'hardship']):
                # Temat: kryzys
                category = [s for s in FINANCIAL_SENTENCES if any(
                    w in s.lower() for w in ['crisis', 'emergency', 'hardship']
                )]
            else:
                category = FINANCIAL_SENTENCES
            
            if not category:
                category = FINANCIAL_SENTENCES
            
            sentence = random.choice(category)
        else:
            sentence = random.choice(FINANCIAL_SENTENCES)
        
        return self.format_comment(sentence)
    
    # ============================================================================
    # 📤 PUBLIKOWANIE KOMENTARZY
    # ============================================================================
    
    def post_comment_to_bluesky(self, post_uri, post_cid, comment):
        """Publikuje komentarz na Bluesky"""
        try:
            # Stwórz referencję do posta
            parent_ref = models.create_strong_ref(post_uri, post_cid)
            
            # Wyślij odpowiedź
            response = self.client.send_post(
                text=comment,
                reply_to=models.AppBskyFeedPost.ReplyRef(
                    parent=parent_ref,
                    root=parent_ref
                )
            )
            
            print(f"💬 Opublikowano komentarz")
            if self.comment_counter % 5 == 0:
                print("   🔗 + link do sklepu")
            
            return True
            
        except Exception as e:
            print(f"❌ Błąd publikacji: {e}")
            return False
    
    # ============================================================================
    # 🚀 GŁÓWNA FUNKCJA
    # ============================================================================
    
    def run(self):
        """Główna funkcja bota"""
        print("="*60)
        print("🚀 URUCHAMIAM FINANCE GROWTH BOT")
        print("="*60)
        print(f"⏰ Godzina: {datetime.now().strftime('%H:%M:%S')}")
        
        # Załaduj statystyki
        stats = self.load_stats()
        print(f"📊 Poprzednie komentarze: {stats['total_comments']}")
        print(f"🔗 Linki do sklepu: {stats['shop_links_posted']}")
        
        # Połącz z Bluesky
        print("\n🔗 Łączę się z Bluesky...")
        try:
            self.client = Client()
            self.client.login(self.handle, self.password)
            print(f"✅ Połączono jako: {self.handle}")
            
            # Pobierz informacje o koncie
            profile = self.client.get_profile(self.client.me.did)
            print(f"👤 Nazwa: {getattr(profile, 'display_name', 'N/A')}")
            print(f"👥 Obserwujący: {getattr(profile, 'followers_count', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Błąd połączenia: {e}")
            print("💡 Sprawdź BLUESKY_HANDLE i BLUESKY_PASSWORD")
            return
        
        # Znajdź posty
        print("\n" + "="*60)
        posts = self.search_finance_posts()
        
        if not posts:
            print("\n🎯 Nie znaleziono odpowiednich postów")
            print("\n💡 WSKAZÓWKI:")
            print("1. Upewnij się, że konto bota obserwuje konta o finansach")
            print("2. Poczekaj kilka godzin - nowe konta mają pusty feed")
            print("3. Sprawdź czy konto jest aktywne na bsky.app")
            
            # Zapisz statystyki nawet przy braku postów
            stats['last_run'] = datetime.now().isoformat()
            stats['last_status'] = 'no_posts_found'
            self.save_stats(stats)
            return
        
        print(f"\n🎯 Rozpoczynam komentowanie {min(3, len(posts))} postów")
        
        # Komentuj posty
        comments_posted = 0
        max_comments = 3  # Maksymalnie 3 komentarze na sesję
        
        for i, post in enumerate(posts[:max_comments]):
            print(f"\n📝 Post {i+1}/{min(max_comments, len(posts))}")
            print(f"   👤 Autor: @{post['author']}")
            print(f"   👍 Polubienia: {post['likes']}")
            print(f"   💬 Treść: {post['text'][:80]}...")
            
            # Wygeneruj komentarz
            comment = self.generate_relevant_comment(post['text'])
            print(f"   🤖 Nasz komentarz: {comment[:80]}...")
            
            # Opublikuj komentarz
            success = self.post_comment_to_bluesky(post['uri'], post['cid'], comment)
            
            if success:
                comments_posted += 1
                
                # Zapisz w historii
                self.save_comment(post['uri'], comment)
                
                # Zaktualizuj statystyki
                stats['total_comments'] = stats.get('total_comments', 0) + 1
                stats['comments_today'] = stats.get('comments_today', 0) + 1
                
                if self.comment_counter % 5 == 0:
                    stats['shop_links_posted'] = stats.get('shop_links_posted', 0) + 1
                    print(f"   🔗 Dodano link do sklepu!")
            
            # Odczekaj między komentarzami (2-4 minuty)
            if i < len(posts[:max_comments]) - 1:
                delay = random.randint(120, 240)
                print(f"   ⏳ Czekam {delay//60} minut...")
                time.sleep(delay)
        
        # Zapisz końcowe statystyki
        stats['last_run'] = datetime.now().isoformat()
        stats['last_status'] = 'success'
        stats['last_comments'] = comments_posted
        self.save_stats(stats)
        
        # Podsumowanie
        print("\n" + "="*60)
        print("✅ BOT ZAKOŃCZYŁ PRACĘ")
        print("="*60)
        print(f"💬 Opublikowane komentarze: {comments_posted}")
        print(f"🔗 Linki do sklepu w tej sesji: {self.comment_counter // 5}")
        print(f"📊 Łącznie komentarzy: {stats['total_comments']}")
        print(f"🛒 Łącznie linków: {stats['shop_links_posted']}")
        
        # Info o następnym linku
        next_link_at = 5 - (self.comment_counter % 5)
        print(f"🎯 Następny link za: {next_link_at} komentarzy")
        
        # Weryfikacja plików
        print("\n📁 PLIKI:")
        for filename in ['bot_stats.json', 'comments_history.json']:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"  ✅ {filename} ({size} bajtów)")
            else:
                print(f"  ❌ {filename} - BRAK!")
        
        print("\n🔗 TWÓJ SKLEP: https://www.payhip.com/daveprime")
        print("="*60)

# ============================================================================
# 🎪 URUCHOMIENIE
# ============================================================================

if __name__ == '__main__':
    print("🔧 Sprawdzam konfigurację...")
    
    # Sprawdź zmienne środowiskowe
    if not os.getenv('BLUESKY_HANDLE'):
        print("❌ BRAK: BLUESKY_HANDLE")
        print("💡 Ustaw w GitHub Secrets lub zmiennych środowiskowych")
        exit(1)
    
    if not os.getenv('BLUESKY_PASSWORD'):
        print("❌ BRAK: BLUESKY_PASSWORD")
        print("💡 Ustaw w GitHub Secrets lub zmiennych środowiskowych")
        exit(1)
    
    print("✅ Konfiguracja poprawna")
    
    # Uruchom bota
    try:
        bot = FinanceGrowthBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n⏹️ Bot zatrzymany przez użytkownika")
    except Exception as e:
        print(f"\n❌ Niespodziewany błąd: {e}")
