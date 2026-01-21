#!/usr/bin/env python3
"""
GUARANTEED BOT WITH HISTORY TRACKING
1 komentarz co 2 godziny, nie komentuje tego samego posta 2x, dodaje link co 5 komentarz
"""

import json
import random
import time
import os
from datetime import datetime
from atproto import Client, models

# ============================================================================
# 🎯 BARDZO SZEROKA TEMATYKA - żeby zawsze znaleźć post
# ============================================================================

TOPICS = {
    # Podstawowe (zawsze znajdzie)
    'money': ['money', 'cash', 'dollar', 'finance', 'financial', 'budget', 'spend', 'save'],
    'life': ['life', 'living', 'day', 'today', 'people', 'world', 'time', 'experience'],
    'help': ['help', 'advice', 'tip', 'suggestion', 'recommend', 'support', 'guide'],
    'problem': ['problem', 'issue', 'trouble', 'difficult', 'hard', 'challenge', 'struggle'],
    'question': ['question', 'ask', 'wonder', 'curious', 'thinking', 'opinion', 'discuss'],
    
    # Twoje tematy
    'survival': ['survival', 'prepper', 'emergency', 'crisis', 'prepared', 'disaster', 'shtf'],
    'debt': ['debt', 'credit', 'loan', 'owe', 'borrow', 'lend', 'payment', 'collection'],
    'health': ['medical', 'hospital', 'doctor', 'health', 'bill', 'insurance', 'treatment'],
    'work': ['work', 'job', 'career', 'business', 'boss', 'employer', 'income', 'salary'],
    'home': ['home', 'house', 'rent', 'mortgage', 'property', 'living', 'apartment'],
    'family': ['family', 'kids', 'children', 'parents', 'partner', 'relationship', 'marriage'],
    'future': ['future', 'plan', 'goal', 'dream', 'retirement', 'savings', 'investment'],
    'stress': ['stress', 'anxiety', 'worry', 'overwhelmed', 'pressure', 'mental', 'depression'],
    'success': ['success', 'win', 'achieve', 'accomplish', 'progress', 'growth', 'improvement'],
}

# Wszystkie słowa kluczowe razem
ALL_KEYWORDS = []
for keywords in TOPICS.values():
    ALL_KEYWORDS.extend(keywords)

# ============================================================================
# 💬 KOMENTARZE DLA KAŻDEGO TEMATU
# ============================================================================

COMMENTS = [
    # Uniwersalne
    "This is so relatable. Taking things one step at a time makes a huge difference.",
    "Many people face similar challenges. Small consistent actions build up over time.",
    "Practical advice often beats theoretical perfection. Start with what you can do today.",
    "Progress isn't always linear. Celebrate the small wins along the way.",
    "Having a clear plan reduces anxiety significantly. Break big problems into small steps.",
    
    # Finansowe
    "Financial stress affects so many people. Tracking expenses is the first step to control.",
    "Debt can feel overwhelming, but negotiation and payment plans are often possible.",
    "Medical bills have more flexibility than people realize. Always ask for options.",
    "Building even a small emergency fund creates psychological safety.",
    "Automating finances was a game-changer for me. One less thing to worry about.",
    "Stressed about debt? You're not alone. The first step is knowing your options.",
    "Credit card companies don't want you to know these negotiation scripts.",
    "Did you know you can often settle debt for 30-50% less? True story.",
    "That collection call tomorrow? Could be your opportunity to negotiate.",
    "The 'debt snowball' method changed my financial life. Anyone else tried it?",
    "Medical debt is negotiable. Most people don't know this.",
    "Your credit score can recover faster than you think with the right strategy.",
    "Debt validation letters are a powerful tool few consumers use.",
    "Stop the harassing calls with one certified letter template.",
    "Consolidation vs. settlement? The choice depends on your unique situation.",
    "Those late fees aren't fixed. Everything is negotiable with creditors.",
    "Financial emergencies happen. Having a plan B is non-negotiable.",
    "The statute of limitations on debt varies by state. Know your rights.",
    "Credit counseling agencies can help, but choose carefully.",
    "Bankruptcy isn't failure—it's a legal financial tool when needed.",
    "The 11-word phrase that can stop debt collectors: 'This is an inconvenient time, please call back tomorrow.'",
    "Your debt-to-income ratio matters more than your credit score for some loans.",
    "Credit repair companies promising miracles are usually scams. DIY is better.",
    "Those 'pre-approved' credit offers? They're not doing you any favors.",
    "Minimum payments keep you in debt for decades. Break the cycle.",
    "Balance transfer cards can be smart IF you have a payoff plan.",
    "Debt collectors have quotas too. Use this to your advantage.",
    "The Fair Debt Collection Practices Act protects you. Learn your rights.",
    "Financial anxiety is real. Taking control starts with one small step.",
    "Your debt isn't a moral failing. It's a math problem with solutions.",
    "Where does your money really go each month? Most people underestimate by 30%.",
    "The 50/30/20 budget rule saved my finances. Anyone else use it?",
    "Cash envelopes aren't old-school—they're psychologically effective.",
    "Subscription creep is real. $10 here, $15 there adds up to hundreds yearly.",
    "That 'emergency fund' advice? Non-negotiable. Start with $500, then $1000.",
    "Paying yourself first isn't selfish—it's smart financial planning.",
    "Financial automation changed everything for me. Bills on autopilot = peace.",
    "Side hustles aren't just for extra cash—they're your financial safety net.",
    "The latte factor is real. But don't deprive yourself—budget for treats.",
    "Zero-based budgeting: Every dollar has a job. Game-changer for control.",
    "Sinking funds for irregular expenses prevent financial surprises.",
    "Cash flow problems aren't income problems—they're timing problems.",
    "Weekly money dates with yourself keep finances on track.",
    "Financial infidelity damages relationships. Transparency is key.",
    "Money scripts from childhood affect adult spending. Awareness helps.",
    "The envelope system works because it's tangible. Digital isn't always better.",
    "Budgeting apps are tools, not solutions. Discipline is the solution.",
    "Living below your means is the ultimate financial freedom.",
    "Financial minimalism: More money, less stress, fewer decisions.",
    "Price per use is a better metric than purchase price for many things.",
    "The 24-hour rule prevents impulse purchases. Wait, then decide.",
    "Financial margin = options. No margin = stress.",
    "Budgeting isn't restriction—it's permission to spend on what matters.",
    "Cash-only challenges reset spending habits effectively.",
    "Your budget should fit your life, not force you into someone else's template.",
    "When money gets tight, prioritize: 1) Shelter 2) Utilities 3) Food 4) Transportation.",
    "The 72-hour financial crisis plan everyone should have.",
    "Survival mode budgeting focuses on needs, cuts all wants temporarily.",
    "$30 can feed one person for a week with strategic shopping.",
    "Financial first aid: Stop bleeding cash before addressing long-term issues.",
    "Crisis doesn't last forever. Temporary measures for temporary problems.",
    "When overwhelmed, focus on today's bills only. Don't project future anxiety.",
    "Community resources exist for emergencies. Pride shouldn't prevent using them.",
    "Negotiate EVERYTHING during hardship: rent, utilities, medical bills.",
    "The priority pyramid: Physiological needs first, then safety, then everything else.",
    "Cash is king during financial emergencies. Liquidate non-essentials quickly.",
    "Financial triage: What must be paid now vs. what can wait?",
    "Crisis budgeting is different from regular budgeting. Survival first.",
    "Temporary hardship programs exist with most major creditors.",
    "The 'financial first aid kit' should include: cash, important documents, budget.",
    "When income drops suddenly, act within 72 hours to preserve cash.",
    "Emergency funds aren't luxuries—they're necessities.",
    "Financial resilience is built BEFORE the crisis, not during.",
    "One month's expenses saved changes everything during job loss.",
    "Side income streams provide stability when main income falters.",
    "Barter and trade regain value during financial hardship.",
    "Financial crisis reveals true priorities quickly.",
    "Survival mode is temporary. Plan your exit strategy from day one.",
    "Community support matters more than ever during financial stress.",
    "Every financial crisis contains opportunity for positive change.",
    "Your money mindset determines your financial outcomes more than income.",
    "Scarcity vs. abundance thinking changes financial decisions dramatically.",
    "Financial self-talk matters. 'I can't afford it' vs 'I choose to spend differently.'",
    "Money shame keeps people stuck. Talking about finances breaks the cycle.",
    "Delayed gratification is a muscle that strengthens with practice.",
    "Financial literacy is the great equalizer in modern society.",
    "Your network determines your net worth. Surround yourself with financially smart people.",
    "Money is a tool, not a goal. Tools build the life you want.",
    "Financial confidence comes from knowledge, not from account balance.",
    "The comparison trap steals joy and wastes money.",
    "Gratitude practices reduce impulsive spending significantly.",
    "Financial boundaries are healthy—with family, friends, and yourself.",
    "Money scripts from childhood run in the background. Time to update them.",
    "Financial therapy addresses the emotional side of money decisions.",
    "Scarcity mentality creates more scarcity. Break the cycle.",
    "Abundance isn't about having more—it's about appreciating what you have.",
    "Financial anxiety decreases as financial literacy increases.",
    "Money conversations should be routine, not taboo.",
    "Your financial identity can evolve. Past mistakes don't define future success.",
    "Small financial wins create momentum for bigger changes.",
    "Financial empowerment feels better than any purchase.",
    "Money is energy. How you direct it determines what grows in your life.",
    "Financial peace is possible at any income level.",
    "Progress, not perfection, is the goal with money.",
    "Your financial future is created by today's small decisions.",
    
    # Survival/Przetrwanie
    "Being prepared isn't about fear - it's about having options when things go wrong.",
    "The most important survival tool is between your ears. Knowledge beats gear every time.",
    "Start with basics: water, food, shelter, security. Everything else builds from there.",
    "Financial preparedness IS emergency preparedness. Resources equal options.",
    "Practice skills before you need them. Muscle memory works when adrenaline doesn't.",
    
    # Psychologiczne
    "Mindset shift is everything. What seems impossible today becomes manageable tomorrow.",
    "Self-talk matters. How we describe our situation affects how we feel about it.",
    "Progress over perfection. Done is better than perfect when you're struggling.",
    "Asking for help is strength, not weakness. Everyone needs support sometimes.",
    "Small daily improvements compound into massive changes over months and years.",
]

# ============================================================================
# 🤖 KLASA BOTA
# ============================================================================

class GuaranteedBotWithHistory:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE')
        self.password = os.getenv('BLUESKY_PASSWORD')
        self.client = None
        self.comment_counter = 0
        
        # Pliki danych
        self.stats_file = 'bot_stats.json'
        self.history_file = 'commented_posts.json'
        self.setup_files()
        
        print("🤖 GUARANTEED BOT WITH HISTORY TRACKING")
    
    def setup_files(self):
        """Setup all data files"""
        # Stats file
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w') as f:
                json.dump({
                    'total_comments': 0,
                    'shop_links': 0,
                    'last_success': '',
                    'created': datetime.now().isoformat(),
                    'daily_comments': 0,
                    'last_reset': datetime.now().isoformat()
                }, f)
        
        # History file - przechowuje już skomentowane posty
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump({
                    'commented_posts': [],
                    'last_updated': datetime.now().isoformat()
                }, f)
    
    def load_stats(self):
        """Load statistics"""
        try:
            with open(self.stats_file, 'r') as f:
                stats = json.load(f)
            
            # Reset daily counter if new day
            today = datetime.now().strftime('%Y-%m-%d')
            last_reset = stats.get('last_reset', '').split('T')[0]
            if last_reset != today:
                stats['daily_comments'] = 0
                stats['last_reset'] = datetime.now().isoformat()
            
            return stats
        except:
            return {'total_comments': 0, 'daily_comments': 0, 'shop_links': 0}
    
    def save_stats(self, stats):
        """Save statistics"""
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def load_commented_posts(self):
        """Load already commented posts"""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                return set(data.get('commented_posts', []))
        except:
            return set()
    
    def save_commented_post(self, post_uri):
        """Save commented post to history"""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
        except:
            data = {'commented_posts': [], 'last_updated': ''}
        
        # Add new post if not already there
        if post_uri not in data['commented_posts']:
            data['commented_posts'].append(post_uri)
            data['last_updated'] = datetime.now().isoformat()
            
            # Keep only last 200 posts to prevent file from growing too large
            if len(data['commented_posts']) > 200:
                data['commented_posts'] = data['commented_posts'][-200:]
            
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"  📝 Added to history: {post_uri[:50]}...")
    
    # ============================================================================
    # 🎯 GWARANTOWANE ZNALEZIENIE POSTU (Z HISTORIĄ)
    # ============================================================================
    
    def find_post_guaranteed(self):
        """Find a post with 100% guarantee - checks history first"""
        print("🎯 GUARANTEED POST FINDER (with history check)")
        
        all_posts = []
        commented_posts = self.load_commented_posts()
        print(f"  📋 Already commented on: {len(commented_posts)} posts")
        
        # METHOD 1: Get timeline with ERROR HANDLING
        print("  📰 Method 1: Safe timeline scan")
        try:
            timeline = self.client.get_timeline(limit=50)
            
            if hasattr(timeline, 'feed'):
                for i, item in enumerate(timeline.feed):
                    try:
                        post = item.post
                        
                        # Skip if missing critical attributes
                        if not hasattr(post, 'record') or not hasattr(post.record, 'text'):
                            continue
                        
                        # Skip own posts
                        if post.author.did == self.client.me.did:
                            continue
                        
                        # Skip already commented posts
                        if post.uri in commented_posts:
                            continue
                        
                        # Skip very low engagement
                        if not hasattr(post, 'like_count') or post.like_count < 25:
                            continue
                        
                        # Skip old posts (older than 30 days)
                        try:
                            post_date = datetime.fromisoformat(post.record.created_at.replace('Z', '+00:00'))
                            days_old = (datetime.now() - post_date).days
                            if days_old > 30:
                                continue
                        except:
                            pass
                        
                        # Get text safely
                        post_text = post.record.text.lower()
                        
                        # Check against ALL keywords (very broad)
                        if any(keyword in post_text for keyword in ALL_KEYWORDS[:25]):
                            score = post.like_count
                            
                            # Determine topic
                            post_topic = 'general'
                            for topic, keywords in TOPICS.items():
                                if any(keyword in post_text for keyword in keywords[:4]):
                                    post_topic = topic
                                    break
                            
                            all_posts.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count,
                                'score': score,
                                'topic': post_topic,
                                'source': 'timeline',
                                'is_new': True
                            })
                            
                            if len(all_posts) >= 15:
                                break
                                
                    except AttributeError:
                        continue
                    except Exception:
                        continue
        
        except Exception as e:
            print(f"    ⚠️  Timeline error: {str(e)[:60]}")
        
        # METHOD 2: Get posts from followed accounts
        if len(all_posts) < 5:
            print("  👥 Method 2: Followed accounts")
            try:
                accounts_to_check = ['wsj.bsky.social', 'bloomberg.bsky.social', 'cnbc.bsky.social', 'forbes.bsky.social']
                
                for account in accounts_to_check:
                    try:
                        acc_profile = self.client.get_profile(account)
                        feed = self.client.get_author_feed(acc_profile.did, limit=8)
                        
                        for item in feed.feed:
                            post = item.post
                            
                            # Skip already commented
                            if post.uri in commented_posts:
                                continue
                            
                            if not hasattr(post, 'like_count') or post.like_count < 30:
                                continue
                            
                            post_text = post.record.text.lower()
                            
                            all_posts.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count,
                                'score': post.like_count * 2,
                                'topic': 'news_finance',
                                'source': f'account:{account}',
                                'is_new': True
                            })
                            
                    except Exception:
                        continue
                    
                    if len(all_posts) >= 10:
                        break
                        
            except Exception as e:
                print(f"    ⚠️  Followed accounts error: {str(e)[:60]}")
        
        # METHOD 3: SEARCH with safe wrapper
        if len(all_posts) < 3:
            print("  🔍 Method 3: Safe search")
            search_terms = ['money tips', 'financial advice', 'debt help', 'survival tips', 'emergency prep']
            
            for term in search_terms:
                try:
                    response = self.client.app.bsky.feed.search_posts(
                        params={'q': term, 'limit': 12}
                    )
                    
                    if hasattr(response, 'posts'):
                        for post in response.posts:
                            try:
                                # Skip already commented
                                if post.uri in commented_posts:
                                    continue
                                
                                if not hasattr(post, 'like_count') or post.like_count < 20:
                                    continue
                                
                                post_text = post.record.text.lower()
                                
                                all_posts.append({
                                    'uri': post.uri,
                                    'cid': post.cid,
                                    'text': post.record.text,
                                    'author': post.author.handle,
                                    'likes': post.like_count,
                                    'score': post.like_count,
                                    'topic': 'search_result',
                                    'source': f'search:{term}',
                                    'is_new': True
                                })
                                
                            except AttributeError:
                                continue
                                
                except Exception:
                    print(f"    ⚠️  Search '{term}' error")
                    continue
        
        # METHOD 4: EMERGENCY - Get NEW post from Bloomberg
        if len(all_posts) == 0:
            print("  🚨 Method 4: EMERGENCY - New Bloomberg post")
            try:
                bloomberg = self.client.get_profile('bloomberg.bsky.social')
                feed = self.client.get_author_feed(bloomberg.did, limit=5)
                
                for item in feed.feed:
                    post = item.post
                    
                    # Skip already commented
                    if post.uri in commented_posts:
                        continue
                    
                    if not hasattr(post, 'like_count') or post.like_count < 10:
                        continue
                    
                    all_posts.append({
                        'uri': post.uri,
                        'cid': post.cid,
                        'text': post.record.text,
                        'author': post.author.handle,
                        'likes': post.like_count,
                        'score': 999,
                        'topic': 'fallback',
                        'source': 'emergency:bloomberg',
                        'is_new': True
                    })
                    print(f"    ✅ NEW emergency post from @bloomberg.bsky.social")
                    break
                    
            except Exception as e:
                print(f"    ❌ Emergency method failed: {str(e)[:60]}")
        
        # Sort by score and return
        if all_posts:
            all_posts.sort(key=lambda x: x['score'], reverse=True)
            print(f"✅ Found {len(all_posts)} NEW posts (not commented before)")
            return all_posts[:5]  # Return top 5 new posts
        
        return []
    
    # ============================================================================
    # 💬 GENERATE COMMENT
    # ============================================================================
    
    def generate_comment(self, topic='general'):
        """Generate appropriate comment"""
        self.comment_counter += 1
        
        # Select comment based on topic
        if topic in ['money', 'debt', 'finance', 'news_finance']:
            financial_comments = [c for c in COMMENTS if any(word in c.lower() for word in ['financial', 'debt', 'money', 'bill', 'fund'])]
            if financial_comments:
                comment = random.choice(financial_comments)
            else:
                comment = random.choice(COMMENTS)
        
        elif topic in ['survival', 'emergency', 'crisis', 'fallback']:
            survival_comments = [c for c in COMMENTS if any(word in c.lower() for word in ['survival', 'prepared', 'emergency', 'crisis', 'practice'])]
            if survival_comments:
                comment = random.choice(survival_comments)
            else:
                comment = random.choice(COMMENTS)
        
        elif topic in ['stress', 'problem', 'help']:
            support_comments = [c for c in COMMENTS if any(word in c.lower() for word in ['stress', 'anxiety', 'help', 'support', 'mindset'])]
            if support_comments:
                comment = random.choice(support_comments)
            else:
                comment = random.choice(COMMENTS)
        
        else:
            comment = random.choice(COMMENTS)
        
        # Add shop link every 5th comment
        if self.comment_counter % 5 == 0:
            shop_link = "https://www.payhip.com/daveprime"
            ctas = [
                f"\n\n🔗 Practical guides: {shop_link}",
                f"\n\n📘 Step-by-step solutions: {shop_link}",
                f"\n\n👉 Actionable templates: {shop_link}"
            ]
            comment = comment + random.choice(ctas)
            print("  🔗 Adding shop link (every 5th comment)")
        
        return comment
    
    # ============================================================================
    # 📤 SAFE COMMENT POSTING
    # ============================================================================
    
    def post_comment_safely(self, post_uri, post_cid, comment):
        """Post comment safely with error handling"""
        try:
            print(f"  📤 Publishing comment...")
            
            # Method 1: Simple dictionary approach
            parent_ref = {
                'uri': post_uri,
                'cid': post_cid
            }
            
            self.client.send_post(
                text=comment,
                reply_to={
                    'root': parent_ref,
                    'parent': parent_ref
                }
            )
            
            print("  ✅ COMMENT PUBLISHED!")
            return True
            
        except Exception as e:
            print(f"  ❌ Method 1 failed: {str(e)[:80]}")
            
            # Method 2: Alternative approach
            try:
                print("  🔄 Trying alternative method...")
                self.client.send_post(
                    text=comment,
                    reply_to=models.AppBskyFeedPost.ReplyRef(
                        parent=models.create_strong_ref(post_uri),
                        root=models.create_strong_ref(post_uri)
                    )
                )
                print("  ✅ COMMENT PUBLISHED (alternative)")
                return True
            except Exception as e2:
                print(f"  ❌ All methods failed: {str(e2)[:80]}")
                return False
    
    # ============================================================================
    # 🚀 MAIN FUNCTION
    # ============================================================================
    
    def run_guaranteed(self):
        """Main function - guaranteed to work with history"""
        print("="*70)
        print("🚀 GUARANTEED BOT WITH HISTORY TRACKING")
        print("="*70)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load stats
        stats = self.load_stats()
        commented_count = len(self.load_commented_posts())
        print(f"📊 Stats: {stats['total_comments']} total, {stats['daily_comments']} today")
        print(f"📋 History: {commented_count} posts already commented")
        
        # Check daily limit (max 12 per day)
        if stats.get('daily_comments', 0) >= 12:
            print("⏹️ Daily limit reached (12 comments)")
            return
        
        # Connect
        if not self.handle or not self.password:
            print("❌ Missing credentials")
            return
        
        try:
            self.client = Client()
            self.client.login(self.handle, self.password)
            print(f"✅ Connected as: {self.handle}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return
        
        # Human delay (45-90 seconds)
        delay = random.randint(45, 90)
        print(f"⏳ Human-like delay: {delay} seconds")
        time.sleep(delay)
        
        # Find NEW posts GUARANTEED (not commented before)
        posts = self.find_post_guaranteed()
        
        if not posts:
            print("\n💔 NO NEW POSTS FOUND - all potential posts already commented")
            print("   Will try again in next run")
            return
        
        # Select best NEW post
        best_post = posts[0]
        print(f"\n🏆 BEST NEW POST SELECTED:")
        print(f"   👤 @{best_post['author']}")
        print(f"   👍 {best_post['likes']} likes")
        print(f"   🏷️  Topic: {best_post['topic']}")
        print(f"   📅 Source: {best_post['source']}")
        print(f"   📄 {best_post['text'][:80]}...")
        
        # Generate comment
        comment = self.generate_comment(best_post['topic'])
        print(f"   💬 Comment: {comment[:80]}...")
        
        # Post comment safely
        success = self.post_comment_safely(best_post['uri'], best_post['cid'], comment)
        
        if not success:
            print("   ❌ Failed to post comment")
            return
        
        # Save to history so we don't comment again
        self.save_commented_post(best_post['uri'])
        
        # Update statistics
        stats['total_comments'] = stats.get('total_comments', 0) + 1
        stats['daily_comments'] = stats.get('daily_comments', 0) + 1
        stats['last_success'] = datetime.now().isoformat()
        stats['last_post'] = best_post['author']
        stats['last_likes'] = best_post['likes']
        
        if self.comment_counter % 5 == 0:
            stats['shop_links'] = stats.get('shop_links', 0) + 1
        
        self.save_stats(stats)
        
        # Final summary
        print("\n" + "="*70)
        print("✅ BOT COMPLETE - NEW POST COMMENTED!")
        print("="*70)
        print(f"💬 Total comments: {stats['total_comments']}")
        print(f"📅 Today: {stats['daily_comments']}/12")
        print(f"🔗 Shop links: {stats.get('shop_links', 0)}")
        print(f"📋 Total unique posts: {commented_count + 1}")
        print(f"🎯 Next shop link in: {5 - (self.comment_counter % 5)} comments")
        print(f"⏰ Next run: In 2 hours")
        print("="*70)

# ============================================================================
# 🎪 RUN
# ============================================================================

if __name__ == '__main__':
    print("🔥 GUARANTEED BOT WITH HISTORY STARTING...")
    bot = GuaranteedBotWithHistory()
    bot.run_guaranteed()
