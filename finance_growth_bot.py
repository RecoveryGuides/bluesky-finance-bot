#!/usr/bin/env python3
"""
Finance Growth Bot for Bluesky - FIXED VERSION
Creates JSON files even when no posts found
"""

import json
import random
import time
import os
from datetime import datetime
from typing import List, Dict
from atproto import Client, models

# Financial sentences (first 20 for example)
FINANCIAL_SENTENCES = [
    # Debt & Credit (25 sentences)
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

class FinanceGrowthBotFixed:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE', '')
        self.password = os.getenv('BLUESKY_PASSWORD', '')
        self.client = None
        
        # 🔥 NAJPIERW TWORZYMY PLIKI!
        self.create_required_files()
        
        # Counters
        self.comment_counter = 0
        self.commented_posts = self.load_commented_posts()
        
        print(f"🤖 Finance Growth Bot v2.0")
        print(f"📊 {len(FINANCIAL_SENTENCES)} sentences loaded")
    
    def create_required_files(self):
        """Create all required data files"""
        files = {
            'finance_bot_stats.json': {
                'total_comments': 0,
                'comments_today': 0,
                'shop_links_posted': 0,
                'last_reset': datetime.now().isoformat(),
                'created': datetime.now().isoformat(),
                'bot_status': 'active'
            },
            'posted_comments.json': []
        }
        
        for filename, default_data in files.items():
            if not os.path.exists(filename):
                with open(filename, 'w') as f:
                    json.dump(default_data, f, indent=2)
                print(f"📁 Created {filename}")
    
    def load_commented_posts(self):
        """Load posts we've already commented on"""
        try:
            with open('posted_comments.json', 'r') as f:
                comments = json.load(f)
                return set([c.get('post_uri', '') for c in comments if c.get('post_uri')])
        except:
            return set()
    
    def should_add_shop_link(self):
        """Add shop link every 5th comment"""
        self.comment_counter += 1
        return self.comment_counter % 5 == 0
    
    def format_with_shop_link(self, comment):
        """Add shop link to comment"""
        shop_link = "https://www.payhip.com/daveprime"
        ctas = [
            f"\n\n👉 Practical guides: {shop_link}",
            f"\n\n🔗 Templates & scripts: {shop_link}",
        ]
        return comment + random.choice(ctas)
    
    def find_posts_simple(self):
        """Simple post finding for new accounts"""
        print("🔍 Searching for finance posts...")
        
        posts_found = []
        
        if not self.client:
            return posts_found
        
        try:
            # Try searching popular finance hashtags
            hashtags = ['personalfinance', 'debt', 'money', 'budget']
            
            for hashtag in hashtags:
                try:
                    print(f"  Searching #{hashtag}...")
                    results = self.client.app.bsky.feed.search_posts(
                        q=f'#{hashtag}',
                        limit=10
                    )
                    
                    for post in results.posts:
                        # Basic filters
                        if post.uri in self.commented_posts:
                            continue
                        
                        if post.author.did == self.client.me.did:
                            continue
                        
                        if post.like_count < 5:
                            continue
                        
                        # Check if finance-related
                        text = post.record.text.lower()
                        if any(word in text for word in ['debt', 'credit', 'money', 'loan', 'finance']):
                            posts_found.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count
                            })
                            
                            if len(posts_found) >= 3:
                                return posts_found
                                
                except Exception as e:
                    print(f"  ⚠️  Error with #{hashtag}: {e}")
                    continue
        
        except Exception as e:
            print(f"❌ Search error: {e}")
        
        return posts_found
    
    def generate_comment(self):
        """Generate a financial comment"""
        # Pick 1-2 random sentences
        num = random.choice([1, 2])
        sentences = random.sample(FINANCIAL_SENTENCES, num)
        comment = " ".join(sentences)
        
        # Add shop link if it's the 5th comment
        if self.should_add_shop_link():
            comment = self.format_with_shop_link(comment)
            print("🔗 Adding shop link (every 5th comment)")
        
        return comment
    
    def post_comment(self, post_uri, post_cid, comment):
        """Post a comment to Bluesky"""
        try:
            parent_ref = models.create_strong_ref(post_uri, post_cid)
            
            self.client.send_post(
                comment,
                reply_to=models.AppBskyFeedPost.ReplyRef(
                    parent=parent_ref,
                    root=parent_ref
                )
            )
            
            # Save to history
            self.save_comment_history(post_uri, comment)
            
            print(f"💬 Comment posted: {comment[:60]}...")
            return True
            
        except Exception as e:
            print(f"❌ Failed to post comment: {e}")
            return False
    
    def save_comment_history(self, post_uri, comment):
        """Save comment to history file"""
        try:
            with open('posted_comments.json', 'r') as f:
                history = json.load(f)
        except:
            history = []
        
        history.append({
            'post_uri': post_uri,
            'comment': comment[:100],
            'timestamp': datetime.now().isoformat()
        })
        
        with open('posted_comments.json', 'w') as f:
            json.dump(history, f, indent=2)
        
        # Also update stats
        self.update_stats()
    
    def update_stats(self):
        """Update statistics file"""
        try:
            with open('finance_bot_stats.json', 'r') as f:
                stats = json.load(f)
        except:
            stats = {'total_comments': 0, 'comments_today': 0}
        
        stats['total_comments'] = stats.get('total_comments', 0) + 1
        stats['comments_today'] = stats.get('comments_today', 0) + 1
        stats['last_run'] = datetime.now().isoformat()
        
        if self.comment_counter % 5 == 0:
            stats['shop_links_posted'] = stats.get('shop_links_posted', 0) + 1
        
        with open('finance_bot_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
    
    def run(self):
        """Main execution"""
        print("🚀 Starting Finance Bot")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Load stats at start
        try:
            with open('finance_bot_stats.json', 'r') as f:
                stats = json.load(f)
            print(f"📊 Previous comments: {stats.get('total_comments', 0)}")
        except:
            print("📊 No previous stats found")
        
        # Connect to Bluesky
        try:
            self.client = Client()
            self.client.login(self.handle, self.password)
            print(f"✅ Connected as: {self.handle}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            # Still save stats even if connection fails
            self.save_final_stats(0, 0)
            return
        
        # Find posts
        posts = self.find_posts_simple()
        
        if not posts:
            print("🎯 No suitable posts found this time")
            print("💡 Tip: Follow finance accounts and like finance posts")
            self.save_final_stats(0, 0)
            return
        
        print(f"🎯 Found {len(posts)} posts to comment on")
        
        # Comment on posts (with delays)
        comments_made = 0
        
        for i, post in enumerate(posts):
            if i > 0:
                delay = random.randint(60, 120)
                print(f"⏳ Waiting {delay} seconds...")
                time.sleep(delay)
            
            print(f"\n📝 Post {i+1}/{len(posts)}")
            print(f"   👤 @{post['author']}")
            print(f"   👍 {post['likes']} likes")
            
            # Generate and post comment
            comment = self.generate_comment()
            success = self.post_comment(post['uri'], post['cid'], comment)
            
            if success:
                comments_made += 1
            
            if comments_made >= 2:  # Max 2 comments per run for new bot
                print("⏹️ Reached max comments for this run")
                break
        
        # Save final stats
        self.save_final_stats(len(posts), comments_made)
        
        print("\n" + "="*50)
        print("📊 RUN COMPLETE")
        print("="*50)
        print(f"💬 Comments made: {comments_made}")
        print(f"🔗 Shop links: {self.comment_counter // 5}")
        print(f"📁 JSON files updated: ✅")
        print("="*50)
    
    def save_final_stats(self, posts_found, comments_made):
        """Save final statistics"""
        try:
            with open('finance_bot_stats.json', 'r') as f:
                stats = json.load(f)
        except:
            stats = {}
        
        stats['last_run'] = datetime.now().isoformat()
        stats['last_posts_found'] = posts_found
        stats['last_comments_made'] = comments_made
        stats['total_runs'] = stats.get('total_runs', 0) + 1
        
        with open('finance_bot_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"💾 Statistics saved to finance_bot_stats.json")

if __name__ == '__main__':
    # Check credentials
    if not os.getenv('BLUESKY_HANDLE'):
        print("❌ Error: BLUESKY_HANDLE not set")
        # Still create files for testing
        bot = FinanceGrowthBotFixed()
        bot.create_required_files()
        exit(1)
    
    if not os.getenv('BLUESKY_PASSWORD'):
        print("❌ Error: BLUESKY_PASSWORD not set")
        exit(1)
    
    # Run bot
    bot = FinanceGrowthBotFixed()
    bot.run()
    
    # Verify files exist
    print("\n📁 FILE CHECK:")
    for file in ['finance_bot_stats.json', 'posted_comments.json']:
        if os.path.exists(file):
            print(f"  ✅ {file} exists")
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                print(f"     Size: {len(data) if isinstance(data, list) else len(str(data))} chars")
            except:
                print(f"     Could not read {file}")
        else:
            print(f"  ❌ {file} missing!")
