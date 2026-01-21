#!/usr/bin/env python3
"""
FINANCE GROWTH BOT - SIMPLE VERSION
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

class SimpleFinanceBot:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE')
        self.password = os.getenv('BLUESKY_PASSWORD')
        self.client = None
        self.comment_count = 0
        
        # Create files
        self.create_files()
        
        print("🤖 Simple Finance Bot started")
    
    def create_files(self):
        """Create data files"""
        if not os.path.exists('bot_stats.json'):
            data = {
                'total_comments': 0,
                'shop_links': 0,
                'created': datetime.now().isoformat()
            }
            with open('bot_stats.json', 'w') as f:
                json.dump(data, f, indent=2)
        
        if not os.path.exists('comments_history.json'):
            with open('comments_history.json', 'w') as f:
                json.dump([], f)
    
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
    
    def save_comment(self, post_uri, comment):
        """Save comment to history"""
        try:
            with open('comments_history.json', 'r') as f:
                history = json.load(f)
        except:
            history = []
        
        history.append({
            'post_uri': post_uri,
            'comment': comment[:150],
            'time': datetime.now().isoformat()
        })
        
        with open('comments_history.json', 'w') as f:
            json.dump(history, f)
    
    def find_posts(self):
        """Find finance posts"""
        print("🔍 Looking for finance posts...")
        
        posts = []
        
        try:
            # Get timeline
            timeline = self.client.get_timeline(limit=40)
            
            for item in timeline.feed:
                post = item.post
                
                # Skip if too few likes
                if post.like_count < 15:
                    continue
                
                # Check if finance related
                text = post.record.text.lower()
                keywords = ['debt', 'credit', 'money', 'finance', 'budget', 'loan']
                
                if any(keyword in text for keyword in keywords):
                    posts.append({
                        'uri': post.uri,
                        'cid': post.cid,
                        'text': post.record.text,
                        'author': post.author.handle,
                        'likes': post.like_count
                    })
                    
                    if len(posts) >= 5:
                        break
        
        except Exception as e:
            print(f"Error finding posts: {e}")
        
        return posts
    
    def generate_comment(self):
        """Generate a comment"""
        self.comment_count += 1
        
        # Get random sentence
        sentence = random.choice(SENTENCES)
        
        # Add shop link every 5th comment
        if self.comment_count % 5 == 0:
            shop_link = "https://www.payhip.com/daveprime"
            sentence = f"{sentence}\n\n👉 Practical guides: {shop_link}"
        
        return sentence
    
    def post_comment(self, post_uri, post_cid, comment):
        """Post comment to Bluesky"""
        try:
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
            print(f"Error posting comment: {e}")
            return False
    
    def run(self):
        """Main function"""
        print("🚀 Starting bot...")
        
        # Check credentials
        if not self.handle or not self.password:
            print("❌ Missing credentials")
            return
        
        # Connect to Bluesky
        try:
            self.client = Client()
            self.client.login(self.handle, self.password)
            print(f"✅ Connected as: {self.handle}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return
        
        # Find posts
        posts = self.find_posts()
        
        if not posts:
            print("🎯 No suitable posts found")
            print("💡 Follow finance accounts and like finance posts")
            return
        
        print(f"🎯 Found {len(posts)} posts")
        
        # Comment on posts
        stats = self.load_stats()
        posted = 0
        
        for i, post in enumerate(posts[:3]):  # Max 3 comments
            print(f"\n📝 Post {i+1}")
            print(f"   👤 @{post['author']} ({post['likes']} likes)")
            print(f"   📄 {post['text'][:80]}...")
            
            # Generate comment
            comment = self.generate_comment()
            print(f"   💬 Comment: {comment[:80]}...")
            
            # Post comment
            success = self.post_comment(post['uri'], post['cid'], comment)
            
            if success:
                posted += 1
                stats['total_comments'] += 1
                
                # Save comment
                self.save_comment(post['uri'], comment)
                
                # Check if shop link was added
                if self.comment_count % 5 == 0:
                    stats['shop_links'] += 1
                    print("   🔗 Added shop link!")
            
            # Wait between comments
            if i < len(posts[:3]) - 1:
                delay = random.randint(120, 180)
                print(f"   ⏳ Waiting {delay} seconds...")
                time.sleep(delay)
        
        # Save final stats
        stats['last_run'] = datetime.now().isoformat()
        self.save_stats(stats)
        
        # Summary
        print("\n" + "="*50)
        print("✅ BOT FINISHED")
        print("="*50)
        print(f"💬 Comments posted: {posted}")
        print(f"📊 Total comments: {stats['total_comments']}")
        print(f"🔗 Shop links: {stats['shop_links']}")
        print(f"🎯 Next shop link in: {5 - (self.comment_count % 5)} comments")
        print("="*50)

# Run bot
if __name__ == '__main__':
    bot = SimpleFinanceBot()
    bot.run()
