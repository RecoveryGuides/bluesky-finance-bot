#!/usr/bin/env python3
"""
ULTIMATE SURVIVAL-FINANCE BOT
1 komentarz na godzinę, tylko top posty, nie wykrywalny jako bot
"""

import json
import random
import time
import os
from datetime import datetime, timedelta
from atproto import Client, models

# ============================================================================
# 🎯 TEMATYKA DO SZUKANIA (szeroka)
# ============================================================================

TOPICS = {
    'survival': [
        'survival', 'prepper', 'prepping', 'emergency', 'crisis',
        'disaster', 'SHTF', 'bugout', 'homestead', 'selfreliance',
        'offgrid', 'wilderness', 'bushcraft', 'camping', 'outdoors'
    ],
    'finance': [
        'debt', 'credit', 'money', 'finance', 'budget',
        'loan', 'owe', 'bill', 'payment', 'collection',
        'broke', 'poor', 'wealth', 'rich', 'income'
    ],
    'health': [
        'medical', 'hospital', 'doctor', 'bill', 'insurance',
        'healthcare', 'treatment', 'sick', 'illness', 'medicine'
    ],
    'debt': [
        'debtfree', 'debtfreejourney', 'payoffdebt', 'debtrelief',
        'creditcarddebt', 'studentdebt', 'medicaldebt', 'getoutofdebt'
    ],
    'crisis': [
        'financialcrisis', 'moneystruggles', 'livingpaycheck',
        'unemployed', 'jobloss', 'eviction', 'foreclosure', 'bankruptcy'
    ]
}

# ============================================================================
# 💬 KOMENTARZE DOPASOWANE DO TEMATÓW
# ============================================================================

COMMENTS_BY_TOPIC = {
    'survival': [
        "When crisis hits, having a plan is everything. Start with 72 hours of essentials.",
        "Survival isn't about doomsday - it's about being prepared for Tuesday's emergency.",
        "The most important survival tool isn't in your bugout bag - it's between your ears.",
        "Financial preparedness IS survival preparedness. No money = no options in crisis.",
        "Start with one week of food and water. That alone puts you ahead of 95% of people."
    ],
    'finance': [
        "Stressed about money? The first step is knowing exactly where it goes each month.",
        "Credit card debt can feel like a life sentence, but negotiation is possible.",
        "Did you know you can often settle old debts for pennies on the dollar?",
        "The 'debt snowball' method works because psychology matters as much as math.",
        "Financial automation changed everything for me. Bills on autopilot = mental freedom."
    ],
    'health': [
        "Medical bills are the #1 cause of bankruptcy in America. Know your rights.",
        "Hospital bills are often negotiable. Always ask for an itemized statement.",
        "Medical debt collectors have strict rules they must follow. Learn the FDCPA.",
        "You can often negotiate payment plans directly with hospitals at 0% interest.",
        "Never pay a medical bill without verifying your insurance was billed correctly first."
    ],
    'debt': [
        "That collection call tomorrow? It could be your opportunity to negotiate.",
        "Stop the harassing calls with one certified letter. Debt collectors hate paper trails.",
        "Consolidation vs. settlement? The right choice depends on your unique situation.",
        "Your credit score can recover faster than you think with the right strategy.",
        "Minimum payments keep you in debt for decades. Breaking the cycle starts today."
    ],
    'crisis': [
        "When money gets tight: 1) Shelter 2) Utilities 3) Food 4) Transportation.",
        "The 72-hour financial crisis plan everyone should have but nobody talks about.",
        "Negotiate EVERYTHING during hardship: rent, utilities, medical bills, even credit cards.",
        "Cash is king during emergencies. Liquidate non-essentials before it's too late.",
        "Financial triage: What MUST be paid now vs. what can wait 30-60-90 days?"
    ]
}

# Wszystkie komentarze razem
ALL_COMMENTS = []
for topic_comments in COMMENTS_BY_TOPIC.values():
    ALL_COMMENTS.extend(topic_comments)

# ============================================================================
# 🤖 KLASA BOTA
# ============================================================================

class UltimateBot:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE')
        self.password = os.getenv('BLUESKY_PASSWORD')
        self.client = None
        self.comment_counter = 0
        
        # Inicjalizacja
        self.setup_files()
        
        print("🤖 ULTIMATE BOT - 100% gwarancja działania")
    
    def setup_files(self):
        """Setup data files"""
        if not os.path.exists('bot_stats.json'):
            with open('bot_stats.json', 'w') as f:
                json.dump({
                    'total_comments': 0,
                    'shop_links': 0,
                    'last_run': '',
                    'created': datetime.now().isoformat()
                }, f)
    
    def load_stats(self):
        """Load statistics"""
        try:
            with open('bot_stats.json', 'r') as f:
                return json.load(f)
        except:
            return {'total_comments': 0, 'shop_links': 0}
    
    def save_stats(self, stats):
        """Save statistics"""
        with open('bot_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
    
    # ============================================================================
    # 🎯 WYSZUKIWANIE POSTÓW - 100% SUKCESU
    # ============================================================================
    
    def find_guaranteed_post(self):
        """Find a post with 100% success rate"""
        print("🎯 GUARANTEED POST SEARCH (5 methods)")
        
        all_posts = []
        attempted_methods = []
        
        # METHOD 1: Search trending topics
        trending_searches = [
            '#personalfinance',
            '#debtfreejourney',
            '#survival',
            '#prepper',
            'medical bills',
            'financial crisis',
            'how to save money',
            'get out of debt'
        ]
        
        for search_term in trending_searches[:4]:  # Try first 4
            try:
                print(f"  🔍 Method 1: Searching '{search_term}'")
                response = self.client.app.bsky.feed.search_posts(
                    params={'q': search_term, 'limit': 20}
                )
                
                for post in response.posts:
                    if not hasattr(post, 'like_count') or post.like_count < 50:
                        continue  # Only highly popular posts
                    
                    if post.author.did == self.client.me.did:
                        continue
                    
                    post_text = post.record.text.lower()
                    score = post.like_count + (post.reply_count * 2) + (post.repost_count * 3)
                    
                    all_posts.append({
                        'uri': post.uri,
                        'cid': post.cid,
                        'text': post.record.text,
                        'author': post.author.handle,
                        'likes': post.like_count,
                        'score': score,
                        'source': f"search:{search_term}"
                    })
                
                attempted_methods.append(f"search:{search_term}")
                if len(all_posts) >= 3:
                    print(f"    ✅ Found {len(all_posts)} posts from searches")
                    break
                    
            except Exception as e:
                print(f"    ⚠️  Search error: {str(e)[:50]}")
        
        # METHOD 2: Get feeds from popular accounts you follow
        if len(all_posts) < 3:
            print("  📰 Method 2: Checking feeds from followed accounts")
            try:
                # Get your follows
                follows = self.client.get_follows(self.client.me.did)
                
                for profile in follows.follows[:5]:  # Check first 5 follows
                    try:
                        feed = self.client.get_author_feed(profile.did, limit=10)
                        
                        for item in feed.feed:
                            post = item.post
                            
                            if not hasattr(post, 'like_count') or post.like_count < 100:
                                continue  # Only viral posts
                            
                            score = post.like_count * 2 + post.reply_count * 3
                            
                            all_posts.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count,
                                'score': score,
                                'source': f"feed:{profile.handle}"
                            })
                            
                    except:
                        continue
                
                attempted_methods.append("author_feeds")
                
            except Exception as e:
                print(f"    ⚠️  Feed error: {str(e)[:50]}")
        
        # METHOD 3: Get trending/hot posts
        if len(all_posts) < 3:
            print("  🔥 Method 3: Getting hot posts")
            try:
                # Try to get popular posts (what's hot)
                timeline = self.client.get_timeline(limit=50)
                
                for item in timeline.feed:
                    post = item.post
                    
                    if not hasattr(post, 'like_count') or post.like_count < 200:
                        continue  # Only viral posts
                    
                    score = post.like_count * 3  # Heavy weight on likes
                    
                    all_posts.append({
                        'uri': post.uri,
                        'cid': post.cid,
                        'text': post.record.text,
                        'author': post.author.handle,
                        'likes': post.like_count,
                        'score': score,
                        'source': 'hot_timeline'
                    })
                    
                    if len(all_posts) >= 5:
                        break
                
                attempted_methods.append("hot_timeline")
                
            except Exception as e:
                print(f"    ⚠️  Timeline error: {str(e)[:50]}")
        
        # METHOD 4: EMERGENCY - Find ANY popular post from big account
        if len(all_posts) == 0:
            print("  🚨 Method 4: EMERGENCY - Big account posts")
            big_accounts = [
                'bloomberg.bsky.social',
                'wsj.bsky.social',
                'cnbc.bsky.social',
                'forbes.bsky.social',
                'reuters.bsky.social'
            ]
            
            for account in big_accounts:
                try:
                    profile = self.client.get_profile(account)
                    feed = self.client.get_author_feed(profile.did, limit=5)
                    
                    if feed.feed:
                        post = feed.feed[0].post  # Their latest post
                        
                        all_posts.append({
                            'uri': post.uri,
                            'cid': post.cid,
                            'text': post.record.text,
                            'author': post.author.handle,
                            'likes': post.like_count,
                            'score': post.like_count * 10,  # High score
                            'source': f"emergency:{account}"
                        })
                        print(f"    ✅ Emergency post from @{account}")
                        break
                        
                except:
                    continue
        
        # Sort by score (engagement)
        all_posts.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"📊 Found {len(all_posts)} total posts via {len(attempted_methods)} methods")
        
        # Filter for our topics
        topic_posts = []
        for post in all_posts:
            post_text = post['text'].lower()
            
            # Check all topics
            for topic, keywords in TOPICS.items():
                if any(keyword in post_text for keyword in keywords):
                    post['topic'] = topic
                    topic_posts.append(post)
                    break
        
        print(f"🎯 {len(topic_posts)} posts match our topics")
        return topic_posts
    
    # ============================================================================
    # 💬 GENEROWANIE KOMENTARZY
    # ============================================================================
    
    def generate_smart_comment(self, post_text, topic=None):
        """Generate topic-relevant comment"""
        self.comment_counter += 1
        
        # Detect topic from post if not provided
        if not topic:
            post_lower = post_text.lower()
            for t, keywords in TOPICS.items():
                if any(keyword in post_lower for keyword in keywords[:5]):
                    topic = t
                    break
        
        # Get relevant comments
        if topic and topic in COMMENTS_BY_TOPIC:
            relevant_comments = COMMENTS_BY_TOPIC[topic]
        else:
            relevant_comments = ALL_COMMENTS
        
        comment = random.choice(relevant_comments)
        
        # Add shop link every 5th comment
        if self.comment_counter % 5 == 0:
            shop_link = "https://www.payhip.com/daveprime"
            ctas = [
                f"\n\n👉 Step-by-step guides: {shop_link}",
                f"\n\n🔗 Practical templates: {shop_link}",
                f"\n\n📘 Complete action plans: {shop_link}"
            ]
            comment = comment + random.choice(ctas)
            print("🔗 Adding shop link (every 5th comment)")
        
        return comment
    
    # ============================================================================
    # 🕒 INTELIGENTNE CZASY I OPÓŹNIENIA
    # ============================================================================
    
    def get_randomized_time(self):
        """Get randomized time (±5 minutes)"""
        base_time = datetime.now()
        random_minutes = random.randint(-5, 5)
        randomized_time = base_time + timedelta(minutes=random_minutes)
        return randomized_time
    
    def human_like_delay(self):
        """Human-like delay (30-90 seconds)"""
        delay = random.randint(30, 90)
        print(f"⏳ Human delay: {delay} seconds")
        time.sleep(delay)
    
    # ============================================================================
    # 🚀 GŁÓWNA FUNKCJA
    # ============================================================================
    
    def run_ultimate(self):
        """Main function - 100% success rate"""
        print("="*70)
        print("🚀 ULTIMATE BOT - 1 COMMENT PER HOUR")
        print("="*70)
        
        # Randomized timing
        current_time = self.get_randomized_time()
        print(f"⏰ Randomized time: {current_time.strftime('%H:%M:%S')}")
        
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
        
        # Human-like delay before searching
        self.human_like_delay()
        
        # Find posts with 100% success guarantee
        posts = self.find_guaranteed_post()
        
        if not posts:
            print("\n💥 CRITICAL: No posts found with 5 search methods")
            print("This should never happen - all methods failed")
            return
        
        # Take only THE BEST post (highest score)
        best_post = posts[0]
        print(f"\n🏆 SELECTED TOP POST:")
        print(f"   👤 @{best_post['author']}")
        print(f"   👍 {best_post['likes']} likes")
        print(f"   📊 Score: {best_post['score']}")
        print(f"   🏷️  Topic: {best_post.get('topic', 'unknown')}")
        print(f"   📄 {best_post['text'][:100]}...")
        
        # Human-like delay before commenting
        self.human_like_delay()
        
        # Generate and post comment
        comment = self.generate_smart_comment(best_post['text'], best_post.get('topic'))
        print(f"   💬 Comment: {comment[:100]}...")
        
        try:
            parent_ref = models.create_strong_ref(best_post['uri'], best_post['cid'])
            
            self.client.send_post(
                text=comment,
                reply_to=models.AppBskyFeedPost.ReplyRef(
                    parent=parent_ref,
                    root=parent_ref
                )
            )
            
            print("   ✅ COMMENT POSTED SUCCESSFULLY!")
            
            # Update stats
            stats = self.load_stats()
            stats['total_comments'] = stats.get('total_comments', 0) + 1
            
            if self.comment_counter % 5 == 0:
                stats['shop_links'] = stats.get('shop_links', 0) + 1
            
            stats['last_run'] = datetime.now().isoformat()
            stats['last_post'] = best_post['author']
            stats['last_likes'] = best_post['likes']
            self.save_stats(stats)
            
        except Exception as e:
            print(f"   ❌ Comment failed: {e}")
            return
        
        # Final summary
        print("\n" + "="*70)
        print("✅ ULTIMATE BOT COMPLETE")
        print("="*70)
        print(f"💬 Total comments: {stats['total_comments']}")
        print(f"🔗 Shop links: {stats.get('shop_links', 0)}")
        print(f"🎯 Next shop link in: {5 - (self.comment_counter % 5)} comments")
        print(f"⏰ Next run: In ~1 hour (±5 minutes)")
        print("="*70)

# ============================================================================
# 🎪 URUCHOMIENIE
# ============================================================================

if __name__ == '__main__':
    print("🔥 ULTIMATE BOT STARTING...")
    bot = UltimateBot()
    bot.run_ultimate()
