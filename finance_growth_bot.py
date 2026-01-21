#!/usr/bin/env python3
"""
SMART FINANCE BOT - OPTIMIZED WITH 20+ HASHTAGS
Działa 3x dziennie, szuka postów przez 20+ hashtagów, dodaje link do sklepu co 5 komentarz
"""

import json
import random
import time
import os
from datetime import datetime
from atproto import Client, models

# Financial sentences
SENTENCES = [
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
    
    # Money Management & Budgeting (25 sentences)
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
    
    # Crisis & Survival Finance (25 sentences)
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
    
    # Mindset & Psychology (25 sentences)
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
    "Your financial future is created by today's small decisions."
]

# Popular finance accounts to follow
FINANCE_ACCOUNTS = [
    "wsj.bsky.social",
    "nytimesbusiness.bsky.social", 
    "bloomberg.bsky.social",
    "theeconomist.bsky.social",
    "cnbc.bsky.social",
    "ft.bsky.social",
    "business.bsky.social",
    "forbes.bsky.social",
    "reuters.bsky.social",
    "ap.bsky.social"
]

# 20+ Finance Hashtags for better search
FINANCE_HASHTAGS = [
    # Podstawowe finanse (6)
    '#personalfinance',
    '#financialfreedom',
    '#moneymanagement',
    '#financialliteracy',
    '#budgeting',
    '#savemoney',
    
    # Długi/kredyty (7)
    '#debtfree',
    '#debtfreejourney',
    '#creditcarddebt',
    '#studentdebt',
    '#debtrelief',
    '#creditscore',
    '#medical',
    '#bills',
    '#creditor',
    '#creditors',
    '#finantial',
    '#creditrepair',
    
    # Kryzys/pomoc (5)
    '#financialcrisis',
    '#moneystruggles',
    '#financialstress',
    '#emergencyfund',
    '#broke',
    
    # Oszczędności/Inwestycje (5)
    '#frugalliving',
    '#investing',
    '#passiveincome',
    '#sidehustle',
    '#financialindependence'
]

class OptimizedFinanceBot:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE')
        self.password = os.getenv('BLUESKY_PASSWORD')
        self.client = None
        self.comment_count = 0
        
        # Create files
        self.create_files()
        
        print("🤖 Optimized Finance Bot with 20+ Hashtags")
    
    def create_files(self):
        """Create data files"""
        if not os.path.exists('bot_stats.json'):
            data = {
                'total_comments': 0,
                'shop_links': 0,
                'follows_done': 0,
                'likes_done': 0,
                'total_runs': 0,
                'created': datetime.now().isoformat()
            }
            with open('bot_stats.json', 'w') as f:
                json.dump(data, f, indent=2)
            print("📁 Created bot_stats.json")
        
        if not os.path.exists('comments_history.json'):
            with open('comments_history.json', 'w') as f:
                json.dump([], f)
            print("📁 Created comments_history.json")
    
    def load_stats(self):
        """Load statistics"""
        try:
            with open('bot_stats.json', 'r') as f:
                return json.load(f)
        except:
            return {'total_comments': 0, 'shop_links': 0, 'follows_done': 0}
    
    def save_stats(self, stats):
        """Save statistics"""
        with open('bot_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
    
    def load_commented_posts(self):
        """Load already commented posts"""
        try:
            with open('comments_history.json', 'r') as f:
                history = json.load(f)
            return {item['post_uri'] for item in history if 'post_uri' in item}
        except:
            return set()
    
    def save_comment(self, post_uri, comment):
        """Save comment to history"""
        try:
            with open('comments_history.json', 'r') as f:
                history = json.load(f)
        except:
            history = []
        
        history.append({
            'post_uri': post_uri,
            'comment': comment[:200],
            'timestamp': datetime.now().isoformat(),
            'comment_number': self.comment_count
        })
        
        # Keep only last 100 comments
        if len(history) > 100:
            history = history[-100:]
        
        with open('comments_history.json', 'w') as f:
            json.dump(history, f)
    
    def setup_account(self):
        """Auto-follow finance accounts and like posts (first run only)"""
        print("⚙️  Setting up account...")
        
        stats = self.load_stats()
        
        # Check if we need to follow accounts
        if stats.get('follows_done', 0) < 5:
            print("  👥 Following finance accounts...")
            follows_added = 0
            
            for account in FINANCE_ACCOUNTS[:8]:
                try:
                    profile = self.client.get_profile(account)
                    self.client.follow(profile.did)
                    follows_added += 1
                    print(f"    ✅ Followed @{account}")
                    time.sleep(random.randint(2, 4))
                    
                    if follows_added >= 5:
                        break
                        
                except Exception as e:
                    print(f"    ⚠️  Could not follow @{account}: {str(e)[:50]}")
                    continue
            
            stats['follows_done'] = stats.get('follows_done', 0) + follows_added
        
        # Like some finance posts
        if stats.get('likes_done', 0) < 10:
            print("  ❤️  Liking finance posts...")
            likes_added = 0
            
            try:
                # Search for finance posts to like
                response = self.client.app.bsky.feed.search_posts(
                    params={'q': '#personalfinance OR debt OR money', 'limit': 15}
                )
                
                for post in response.posts:
                    if likes_added >= 8:
                        break
                    
                    if post.author.did == self.client.me.did:
                        continue
                    
                    try:
                        self.client.like(post.uri, post.cid)
                        likes_added += 1
                        print(f"    ✅ Liked post from @{post.author.handle}")
                        time.sleep(random.randint(1, 3))
                    except:
                        continue
                        
            except Exception as e:
                print(f"    ⚠️  Could not like posts: {str(e)[:50]}")
            
            stats['likes_done'] = stats.get('likes_done', 0) + likes_added
        
        self.save_stats(stats)
        print("✅ Account setup complete")
    
    def find_posts_with_multiple_hashtags(self):
        """Find finance posts using 20+ hashtags"""
        print("🔍 Searching with 20+ finance hashtags...")
        
        posts = []
        commented_posts = self.load_commented_posts()
        posts_found_count = 0
        
        # Shuffle hashtags for variety
        hashtags_to_search = random.sample(FINANCE_HASHTAGS, min(12, len(FINANCE_HASHTAGS)))
        
        for hashtag in hashtags_to_search:
            if posts_found_count >= 10:  # Stop when we have enough
                break
            
            try:
                print(f"  🔍 Searching {hashtag}...")
                response = self.client.app.bsky.feed.search_posts(
                    params={'q': hashtag, 'limit': 10}
                )
                
                new_posts_from_hashtag = 0
                
                for post in response.posts:
                    if posts_found_count >= 10:
                        break
                    
                    # Skip if already commented
                    if post.uri in commented_posts:
                        continue
                    
                    # Skip own posts
                    if post.author.did == self.client.me.did:
                        continue
                    
                    # Quality filters
                    if post.like_count < 8:  # Min 8 likes
                        continue
                    
                    # Check if finance related
                    post_text = post.record.text.lower()
                    finance_keywords = [
                        'debt', 'credit', 'money', 'finance', 'budget',
                        'loan', 'owe', 'bill', 'payment', 'collection',
                        'creditor', 'score', 'interest', 'hardship',
                        'crisis', 'emergency', 'save', 'spend', 'cash'
                    ]
                    
                    if any(keyword in post_text for keyword in finance_keywords):
                        # Check if we already have this post
                        post_exists = any(p['uri'] == post.uri for p in posts)
                        if not post_exists:
                            posts.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count,
                                'hashtag': hashtag
                            })
                            
                            posts_found_count += 1
                            new_posts_from_hashtag += 1
                            
                            print(f"    ✅ {hashtag}: @{post.author.handle} ({post.like_count} likes)")
                
                if new_posts_from_hashtag > 0:
                    print(f"    📊 Found {new_posts_from_hashtag} posts from {hashtag}")
                    
            except Exception as e:
                print(f"    ⚠️  Error with {hashtag}: {str(e)[:50]}")
                continue
        
        # If still not enough posts, try timeline
        if len(posts) < 3:
            print("  📰 Checking timeline as backup...")
            try:
                timeline = self.client.get_timeline(limit=30)
                
                for item in timeline.feed:
                    if len(posts) >= 5:
                        break
                    
                    post = item.post
                    
                    if post.uri in commented_posts:
                        continue
                    
                    if post.author.did == self.client.me.did:
                        continue
                    
                    if post.like_count >= 12:
                        text = post.record.text.lower()
                        if any(word in text for word in ['debt', 'money', 'finance', 'credit']):
                            posts.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count,
                                'hashtag': 'timeline'
                            })
                            
                            print(f"    ✅ Timeline: @{post.author.handle} ({post.like_count} likes)")
                            
            except Exception as e:
                print(f"    ⚠️  Timeline error: {str(e)[:50]}")
        
        # Remove any duplicates
        unique_posts = []
        seen_uris = set()
        for post in posts:
            if post['uri'] not in seen_uris:
                seen_uris.add(post['uri'])
                unique_posts.append(post)
        
        print(f"🎯 Found {len(unique_posts)} unique finance posts")
        return unique_posts
    
    def generate_comment(self, post_text=""):
        """Generate relevant financial comment"""
        self.comment_count += 1
        
        # Pick relevant sentence based on post content
        if post_text:
            post_lower = post_text.lower()
            
            if any(word in post_lower for word in ['debt', 'owe', 'collection']):
                relevant = [s for s in SENTENCES if any(w in s.lower() for w in ['debt', 'credit', 'owe'])]
            elif any(word in post_lower for word in ['budget', 'save', 'spend']):
                relevant = [s for s in SENTENCES if any(w in s.lower() for w in ['budget', 'save', 'money'])]
            elif any(word in post_lower for word in ['crisis', 'emergency', 'hardship']):
                relevant = [s for s in SENTENCES if any(w in s.lower() for w in ['crisis', 'emergency'])]
            else:
                relevant = SENTENCES
        else:
            relevant = SENTENCES
        
        if not relevant:
            relevant = SENTENCES
        
        sentence = random.choice(relevant)
        
        # Add shop link every 5th comment
        if self.comment_count % 5 == 0:
            shop_link = "https://www.payhip.com/daveprime"
            ctas = [
                f"\n\n👉 Practical guides: {shop_link}",
                f"\n\n🔗 Templates & scripts: {shop_link}",
                f"\n\n📘 Step-by-step solutions: {shop_link}"
            ]
            sentence = sentence + random.choice(ctas)
        
        return sentence
    
    def post_comment_with_delay(self, post_uri, post_cid, comment):
        """Post comment with human-like delay"""
        try:
            # Random delay before posting (30-90 seconds)
            delay = random.randint(30, 90)
            print(f"    ⏳ Waiting {delay} seconds before posting...")
            time.sleep(delay)
            
            parent_ref = models.create_strong_ref(post_uri, post_cid)
            
            self.client.send_post(
                text=comment,
                reply_to=models.AppBskyFeedPost.ReplyRef(
                    parent=parent_ref,
                    root=parent_ref
                )
            )
            
            return True
            
        except Exception as e:
            print(f"    ❌ Error posting comment: {e}")
            return False
    
    def run(self):
        """Main function"""
        print("="*60)
        print("🚀 OPTIMIZED FINANCE BOT - 20+ HASHTAGS")
        print("="*60)
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check credentials
        if not self.handle or not self.password:
            print("❌ Missing BLUESKY_HANDLE or BLUESKY_PASSWORD")
            return
        
        # Load stats
        stats = self.load_stats()
        print(f"📊 Previous stats: {stats.get('total_comments', 0)} comments, {stats.get('shop_links', 0)} shop links")
        
        # Connect to Bluesky
        print("\n🔗 Connecting to Bluesky...")
        try:
            self.client = Client()
            self.client.login(self.handle, self.password)
            print(f"✅ Connected as: {self.handle}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return
        
        # Auto-setup on first few runs
        if stats.get('total_runs', 0) < 3:
            self.setup_account()
            time.sleep(5)
        
        # Find posts using multiple hashtags
        print("\n" + "="*60)
        posts = self.find_posts_with_multiple_hashtags()
        
        if not posts:
            print("\n🎯 No finance posts found")
            print("\n💡 The bot will try again in 4 hours")
            stats['total_runs'] = stats.get('total_runs', 0) + 1
            stats['last_run'] = datetime.now().isoformat()
            self.save_stats(stats)
            return
        
        print(f"\n🎯 Ready to engage with {min(3, len(posts))} posts")
        
        # Sort by engagement (likes)
        posts.sort(key=lambda x: x['likes'], reverse=True)
        
        # Decide how many posts to comment on (1-3 randomly)
        max_comments = random.randint(1, 3)
        posts_to_comment = posts[:max_comments]
        
        posted_count = 0
        
        for i, post in enumerate(posts_to_comment):
            print(f"\n📝 Post {i+1}/{len(posts_to_comment)}")
            print(f"   👤 Author: @{post['author']}")
            print(f"   👍 Likes: {post['likes']}")
            print(f"   🏷️  Source: {post['hashtag']}")
            print(f"   📄 Text: {post['text'][:80]}...")
            
            # Generate comment
            comment = self.generate_comment(post['text'])
            print(f"   💬 Our comment: {comment[:80]}...")
            
            # Post comment
            success = self.post_comment_with_delay(post['uri'], post['cid'], comment)
            
            if success:
                posted_count += 1
                stats['total_comments'] = stats.get('total_comments', 0) + 1
                
                # Save comment to history
                self.save_comment(post['uri'], comment)
                
                # Track shop links
                if self.comment_count % 5 == 0:
                    stats['shop_links'] = stats.get('shop_links', 0) + 1
                    print("   🔗 Shop link added!")
            
            # Wait between posts (2-4 minutes if not last post)
            if i < len(posts_to_comment) - 1:
                delay = random.randint(120, 240)
                print(f"   ⏳ Waiting {delay//60} minutes before next post...")
                time.sleep(delay)
        
        # Update and save final stats
        stats['total_runs'] = stats.get('total_runs', 0) + 1
        stats['last_run'] = datetime.now().isoformat()
        stats['last_comments_posted'] = posted_count
        stats['last_posts_found'] = len(posts)
        self.save_stats(stats)
        
        # Summary
        print("\n" + "="*60)
        print("✅ BOT FINISHED SUCCESSFULLY")
        print("="*60)
        print(f"💬 Comments posted this run: {posted_count}")
        print(f"📊 Total comments: {stats['total_comments']}")
        print(f"🔗 Shop links: {stats['shop_links']}")
        print(f"🔄 Total runs: {stats['total_runs']}")
        print(f"🎯 Next shop link in: {5 - (self.comment_count % 5)} comments")
        
        # Hashtag info
        unique_hashtags = set(p['hashtag'] for p in posts[:5])
        print(f"🏷️  Hashtags searched: {len(unique_hashtags)}")
        
        print("\n📁 FILES UPDATED:")
        for filename in ['bot_stats.json', 'comments_history.json']:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"  ✅ {filename} ({size} bytes)")
        
        print("\n⏰ NEXT RUN: In 4 hours")
        print("🔗 SHOP: https://www.payhip.com/daveprime")
        print("="*60)

# Run bot
if __name__ == '__main__':
    bot = OptimizedFinanceBot()
    bot.run()
