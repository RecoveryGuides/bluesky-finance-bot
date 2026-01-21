#!/usr/bin/env python3
"""
SPECIALIST FINANCE BOT FOR BLUESKY - STARTER VERSION
Simplified for new accounts
"""

import json
import random
import time
import re
from datetime import datetime, timedelta
import os
from typing import List, Dict
from atproto import Client, models

# Financial sentences (same as before - 100 sentences)
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

class FinanceGrowthBotStarter:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE', '')
        self.password = os.getenv('BLUESKY_PASSWORD', '')
        self.client = None
        
        # Create data files
        self.create_data_files()
        
        # Counters
        self.comment_counter = 0
        self.commented_posts = set()
        
        print(f"🤖 Finance Growth Bot (Starter Edition)")
        print(f"📊 {len(FINANCIAL_SENTENCES)} financial sentences loaded")
    
    def create_data_files(self):
        """Create necessary data files"""
        if not os.path.exists('finance_bot_stats.json'):
            with open('finance_bot_stats.json', 'w') as f:
                json.dump({
                    'total_comments': 0,
                    'comments_today': 0,
                    'last_reset': datetime.now().isoformat(),
                    'shop_links_posted': 0
                }, f)
        
        if not os.path.exists('posted_comments.json'):
            with open('posted_comments.json', 'w') as f:
                json.dump([], f)
    
    def should_add_shop_link(self):
        """Every 5th comment includes shop link"""
        self.comment_counter += 1
        return self.comment_counter % 5 == 0
    
    def format_with_shop_link(self, comment):
        """Add shop link to comment"""
        shop_link = "https://www.payhip.com/daveprime"
        ctas = [
            f"\n\n👉 For actionable templates: {shop_link}",
            f"\n\n🔗 Step-by-step guides: {shop_link}",
        ]
        return comment + random.choice(ctas)
    
    def find_simple_targets(self):
        """Simple target finding for new accounts"""
        print("🔍 Searching for finance posts...")
        
        try:
            # Method 1: Search finance hashtags
            hashtags = ['personalfinance', 'debt', 'money', 'budget']
            targets = []
            
            for hashtag in hashtags[:2]:  # Try first 2 hashtags
                try:
                    print(f"  Searching #{hashtag}...")
                    results = self.client.app.bsky.feed.search_posts(
                        q=f'#{hashtag}',
                        limit=15
                    )
                    
                    for post in results.posts:
                        # Skip if already commented
                        if post.uri in self.commented_posts:
                            continue
                        
                        # Skip if very low engagement
                        if post.like_count < 5:
                            continue
                        
                        # Check if finance related
                        post_text = post.record.text.lower()
                        finance_words = ['debt', 'credit', 'money', 'finance', 'budget', 'loan']
                        
                        if any(word in post_text for word in finance_words):
                            targets.append({
                                'uri': post.uri,
                                'cid': post.cid,
                                'text': post.record.text,
                                'author': post.author.handle,
                                'likes': post.like_count
                            })
                            
                            if len(targets) >= 3:  # Get max 3 posts
                                break
                                
                except Exception as e:
                    print(f"  Warning searching #{hashtag}: {e}")
                    continue
            
            return targets
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def generate_comment(self):
        """Generate financial comment"""
        # Pick 1-2 random sentences
        num = random.choice([1, 1, 2])
        sentences = random.sample(FINANCIAL_SENTENCES, num)
        comment = " ".join(sentences)
        
        # Add shop link if 5th comment
        if self.should_add_shop_link():
            comment = self.format_with_shop_link(comment)
            print("🔗 Adding shop link (every 5th comment)")
        
        return comment
    
    def post_comment(self, post_uri, post_cid, comment):
        """Post comment to Bluesky"""
        try:
            parent_ref = models.create_strong_ref(post_uri, post_cid)
            
            self.client.send_post(
                comment,
                reply_to=models.AppBskyFeedPost.ReplyRef(
                    parent=parent_ref,
                    root=parent_ref
                )
            )
            
            print(f"💬 Commented: {comment[:80]}...")
            
            # Save to history
            self.commented_posts.add(post_uri)
            self.save_stats()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to comment: {e}")
            return False
    
    def save_stats(self):
        """Update statistics"""
        try:
            with open('finance_bot_stats.json', 'r') as f:
                stats = json.load(f)
        except:
            stats = {'total_comments': 0, 'comments_today': 0}
        
        stats['total_comments'] = stats.get('total_comments', 0) + 1
        stats['comments_today'] = stats.get('comments_today', 0) + 1
        
        if self.comment_counter % 5 == 0:
            stats['shop_links_posted'] = stats.get('shop_links_posted', 0) + 1
        
        with open('finance_bot_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
    
    def run(self):
        """Main execution"""
        print("🚀 Starting Finance Growth Bot")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Connect to Bluesky
        try:
            self.client = Client()
            self.client.login(self.handle, self.password)
            print(f"✅ Connected as: {self.handle}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return
        
        # Find targets
        targets = self.find_simple_targets()
        
        if not targets:
            print("🎯 No finance posts found right now")
            print("💡 TIP: Follow finance accounts and like finance posts")
            return
        
        print(f"🎯 Found {len(targets)} finance posts")
        
        # Comment on each (with delays)
        for i, post in enumerate(targets):
            if i > 0:
                delay = random.randint(60, 180)  # 1-3 minutes
                print(f"⏳ Waiting {delay} seconds...")
                time.sleep(delay)
            
            print(f"\n📝 Post {i+1}/{len(targets)}")
            print(f"   👤 @{post['author']}")
            print(f"   👍 {post['likes']} likes")
            
            # Generate and post comment
            comment = self.generate_comment()
            success = self.post_comment(post['uri'], post['cid'], comment)
            
            if success and i >= 2:  # Max 3 comments per run
                print("⏹️ Reached max comments for this run")
                break
        
        # Summary
        print("\n" + "="*50)
        print("📊 BOT SUMMARY")
        print("="*50)
        print(f"💬 Comments posted this run: {min(3, len(targets))}")
        print(f"🔗 Shop links posted: {self.comment_counter // 5}")
        print(f"🎯 Next shop link at comment #{5 - (self.comment_counter % 5)}")
        print("="*50)
        print("💡 TIPS FOR BETTER RESULTS:")
        print("1. Follow finance accounts on your Bluesky bot account")
        print("2. Like finance-related posts")
        print("3. Use finance hashtags in your searches")
        print("="*50)

if __name__ == '__main__':
    if not os.getenv('BLUESKY_HANDLE') or not os.getenv('BLUESKY_PASSWORD'):
        print("❌ Missing Bluesky credentials")
        exit(1)
    
    bot = FinanceGrowthBotStarter()
    bot.run()
