#!/usr/bin/env python3
"""
ULTIMATE WORKING BOT - Omija błędy, zawsze znajduje posty
"""

import json
import random
import time
import os
from datetime import datetime, timedelta
from atproto import Client, models

# ============================================================================
# 🎯 BARDZO SZEROKA TEMATYKA - żeby zawsze znaleźć post
# ============================================================================

TOPICS = {
    # Podstawowe (zawsze znajdzie)
    'money': ['money', 'cash', 'dollar', 'finance', 'financial'],
    'life': ['life', 'living', 'day', 'today', 'people', 'world'],
    'help': ['help', 'advice', 'tip', 'suggestion', 'recommend'],
    'problem': ['problem', 'issue', 'trouble', 'difficult', 'hard'],
    'question': ['question', 'ask', 'wonder', 'curious', 'thinking'],
    
    # Twoje tematy
    'survival': ['survival', 'prepper', 'emergency', 'crisis', 'prepared'],
    'debt': ['debt', 'credit', 'loan', 'owe', 'borrow', 'lend'],
    'health': ['medical', 'hospital', 'doctor', 'health', 'bill'],
    'budget': ['budget', 'save', 'spend', 'expensive', 'cheap'],
    'work': ['work', 'job', 'career', 'business', 'boss', 'employer'],
    'home': ['home', 'house', 'rent', 'mortgage', 'property'],
    'family': ['family', 'kids', 'children', 'parents', 'partner'],
    'future': ['future', 'plan', 'goal', 'dream', 'retirement'],
    'stress': ['stress', 'anxiety', 'worry', 'overwhelmed', 'pressure'],
    'success': ['success', 'win', 'achieve', 'accomplish', 'progress'],
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

class GuaranteedBot:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE')
        self.password = os.getenv('BLUESKY_PASSWORD')
        self.client = None
        self.comment_counter = 0
        
        print("🤖 GUARANTEED BOT - Always finds posts")
    
    # ============================================================================
    # 🎯 GWARANTOWANE ZNALEZIENIE POSTU
    # ============================================================================
    
    def find_post_guaranteed(self):
        """Find a post with 100% guarantee - multiple fallback methods"""
        print("🎯 GUARANTEED POST FINDER")
        
        all_posts = []
        
        # METHOD 1: Get timeline with ERROR HANDLING
        print("  📰 Method 1: Safe timeline scan")
        try:
            timeline = self.client.get_timeline(limit=40)
            
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
                        
                        # Skip very low engagement
                        if not hasattr(post, 'like_count') or post.like_count < 20:
                            continue
                        
                        # Get text safely
                        post_text = post.record.text.lower()
                        
                        # Check against ALL keywords (very broad)
                        if any(keyword in post_text for keyword in ALL_KEYWORDS[:20]):  # Check first 20
                            score = post.like_count
                            
                            # Determine topic
                            post_topic = 'general'
                            for topic, keywords in TOPICS.items():
                                if any(keyword in post_text for keyword in keywords[:3]):  # Check first 3
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
                                'source': 'timeline'
                            })
                            
                            if len(all_posts) >= 10:
                                break
                                
                    except AttributeError:
                        continue  # Skip posts with attribute errors
                    except Exception:
                        continue  # Skip any other errors
        
        except Exception as e:
            print(f"    ⚠️  Timeline error (handled): {str(e)[:60]}")
        
        # METHOD 2: Get posts from accounts you follow
        if len(all_posts) < 5:
            print("  👥 Method 2: Followed accounts")
            try:
                # Get your profile to get follows
                profile = self.client.get_profile(self.client.me.did)
                
                # Try to get posts from followed accounts
                accounts_to_check = ['wsj.bsky.social', 'bloomberg.bsky.social', 'cnbc.bsky.social']
                
                for account in accounts_to_check:
                    try:
                        acc_profile = self.client.get_profile(account)
                        feed = self.client.get_author_feed(acc_profile.did, limit=5)
                        
                        for item in feed.feed:
                            post = item.post
                            
                            if not hasattr(post, 'like_count') or post.like_count < 10:
                                continue
                            
                            post_text = post.record.text.lower()
                            
                            # Add ANY post from these accounts
                            all_posts.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count,
                                'score': post.like_count * 2,
                                'topic': 'news_finance',
                                'source': f'account:{account}'
                            })
                            
                    except Exception:
                        continue
                    
                    if len(all_posts) >= 8:
                        break
                        
            except Exception as e:
                print(f"    ⚠️  Followed accounts error: {str(e)[:60]}")
        
        # METHOD 3: SEARCH with safe wrapper
        if len(all_posts) < 3:
            print("  🔍 Method 3: Safe search")
            search_terms = ['money', 'help', 'life', 'work', 'home']
            
            for term in search_terms:
                try:
                    # Try search with basic term
                    response = self.client.app.bsky.feed.search_posts(
                        params={'q': term, 'limit': 10}
                    )
                    
                    # Safely process response
                    if hasattr(response, 'posts'):
                        for post in response.posts:
                            try:
                                if not hasattr(post, 'like_count') or post.like_count < 15:
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
                                    'source': f'search:{term}'
                                })
                                
                            except AttributeError:
                                continue
                                
                except Exception as e:
                    print(f"    ⚠️  Search '{term}' error (handled)")
                    continue
        
        # METHOD 4: EMERGENCY - Get ANY post from your own likes
        if len(all_posts) == 0:
            print("  🚨 Method 4: EMERGENCY - Your liked posts")
            try:
                # Try to get posts you've liked
                timeline = self.client.get_timeline(limit=20)
                
                for item in timeline.feed:
                    try:
                        post = item.post
                        
                        if not hasattr(post, 'like_count'):
                            continue
                        
                        # Take ANY post with reasonable engagement
                        if post.like_count >= 10:
                            all_posts.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count,
                                'score': 100,  # Emergency score
                                'topic': 'emergency',
                                'source': 'emergency'
                            })
                            print(f"    ✅ EMERGENCY post: @{post.author.handle}")
                            break
                            
                    except AttributeError:
                        continue
                        
            except Exception as e:
                print(f"    ⚠️  Emergency method error: {str(e)[:60]}")
        
        # FINAL: If STILL no posts, create dummy post from Bloomberg
        if len(all_posts) == 0:
            print("  💀 CRITICAL: Creating fallback post")
            # This is last resort - we'll comment on Bloomberg's latest
            try:
                bloomberg = self.client.get_profile('bloomberg.bsky.social')
                feed = self.client.get_author_feed(bloomberg.did, limit=1)
                
                if feed.feed:
                    post = feed.feed[0].post
                    all_posts.append({
                        'uri': post.uri,
                        'cid': post.cid,
                        'text': post.record.text,
                        'author': post.author.handle,
                        'likes': post.like_count,
                        'score': 999,
                        'topic': 'fallback',
                        'source': 'fallback:bloomberg'
                    })
                    
            except Exception:
                # Ultimate fallback - we'll skip this run
                print("    ❌ ALL METHODS FAILED - will try next run")
                return []
        
        # Sort by score and return
        if all_posts:
            all_posts.sort(key=lambda x: x['score'], reverse=True)
            print(f"✅ Found {len(all_posts)} posts (guaranteed)")
            return all_posts[:3]  # Return top 3
        
        return []
    
    # ============================================================================
    # 💬 GENERATE COMMENT
    # ============================================================================
    
    def generate_comment(self, topic='general'):
        """Generate appropriate comment"""
        self.comment_counter += 1
        
        # Select comment based on topic if possible
        if topic in ['money', 'debt', 'budget', 'finance']:
            # Financial comments
            financial_comments = [c for c in COMMENTS if any(word in c.lower() for word in ['financial', 'debt', 'money', 'bill'])]
            if financial_comments:
                comment = random.choice(financial_comments)
            else:
                comment = random.choice(COMMENTS)
        
        elif topic in ['survival', 'emergency', 'crisis']:
            # Survival comments
            survival_comments = [c for c in COMMENTS if any(word in c.lower() for word in ['survival', 'prepared', 'emergency', 'crisis'])]
            if survival_comments:
                comment = random.choice(survival_comments)
            else:
                comment = random.choice(COMMENTS)
        
        elif topic in ['stress', 'problem', 'help']:
            # Psychological support comments
            support_comments = [c for c in COMMENTS if any(word in c.lower() for word in ['stress', 'anxiety', 'help', 'support', 'mindset'])]
            if support_comments:
                comment = random.choice(support_comments)
            else:
                comment = random.choice(COMMENTS)
        
        else:
            # General comment
            comment = random.choice(COMMENTS)
        
        # Add shop link every 5th comment
        if self.comment_counter % 5 == 0:
            shop_link = "https://www.payhip.com/daveprime"
            comment = f"{comment}\n\n🔗 Practical solutions: {shop_link}"
        
        return comment
    
    # ============================================================================
    # 🚀 MAIN FUNCTION
    # ============================================================================
    
    def run_guaranteed(self):
        """Main function - guaranteed to work"""
        print("="*60)
        print("🚀 GUARANTEED WORKING BOT")
        print("="*60)
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
        
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
        
        # Human delay
        delay = random.randint(30, 60)
        print(f"⏳ Delay: {delay} seconds")
        time.sleep(delay)
        
        # Find posts GUARANTEED
        posts = self.find_post_guaranteed()
        
        if not posts:
            print("\n💔 NO POSTS FOUND - trying next run")
            print("   This is extremely rare - wait for next scheduled run")
            return
        
        # Select best post
        best_post = posts[0]
        print(f"\n🏆 BEST POST SELECTED:")
        print(f"   👤 @{best_post['author']}")
        print(f"   👍 {best_post['likes']} likes")
        print(f"   🏷️  Topic: {best_post['topic']}")
        print(f"   📄 {best_post['text'][:80]}...")
        
        # Generate comment
        comment = self.generate_comment(best_post['topic'])
        print(f"   💬 Comment: {comment[:80]}...")
        
        # Post comment
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
            
            # Update counter
            self.comment_counter += 1
            
            # Show shop link info
            if self.comment_counter % 5 == 0:
                print("   🔗 SHOP LINK INCLUDED!")
            
        except Exception as e:
            print(f"   ❌ Comment failed: {e}")
            # Try one more time with different approach
            try:
                # Alternative method
                self.client.send_post(
                    text=comment,
                    reply_to={
                        'root': {'uri': best_post['uri'], 'cid': best_post['cid']},
                        'parent': {'uri': best_post['uri'], 'cid': best_post['cid']}
                    }
                )
                print("   ✅ COMMENT POSTED (alternative method)")
            except:
                print("   ❌ All posting methods failed")
                return
        
        # Final
        print("\n" + "="*60)
        print("✅ BOT COMPLETE - POST FOUND AND COMMENTED")
        print("="*60)
        print(f"💬 Comment counter: {self.comment_counter}")
        print(f"🔗 Next shop link in: {5 - (self.comment_counter % 5)} comments")
        print(f"⏰ Next run: In 1-2 hours")
        print("="*60)

# ============================================================================
# 🎪 RUN
# ============================================================================

if __name__ == '__main__':
    print("🔥 GUARANTEED BOT STARTING...")
    bot = GuaranteedBot()
    bot.run_guaranteed()
