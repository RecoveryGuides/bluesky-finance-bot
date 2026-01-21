#!/usr/bin/env python3
"""
SPECIALIST FINANCE BOT FOR BLUESKY
Targets US audiences on finance/debt topics
Posts strategic comments to drive traffic to payhip.com/daveprime
"""

import json
import random
import time
import re
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional
from atproto import Client, models

# ============================================================================
# 📊 FINANCIAL SENTENCES DATABASE (100 hand-picked, high-conversion)
# ============================================================================

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

# ============================================================================
# 🌎 USA LOCATION DETECTION & TARGETING
# ============================================================================

USA_KEYWORDS = [
    # Cities
    "NYC", "New York", "LA", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
    "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington DC",
    
    # States
    "California", "Texas", "Florida", "New York", "Pennsylvania", "Illinois",
    "Ohio", "Georgia", "North Carolina", "Michigan", "New Jersey",
    
    # Regions
    "West Coast", "East Coast", "Midwest", "South", "New England",
    "Pacific Northwest", "Southwest", "Rocky Mountains",
    
    # Cultural references
    "dollar", "USD", "401k", "IRA", "Social Security", "Medicare",
    "credit score", "FICO", "IRS", "tax season", "health insurance deductible"
]

def is_usa_account(profile: Dict) -> bool:
    """Detect if an account is likely from USA"""
    if not profile:
        return False
    
    # Check location field
    location = profile.get('location', '').lower()
    description = profile.get('description', '').lower()
    
    # Look for USA indicators
    usa_indicators = ['usa', 'united states', 'us', 'u.s.', 'america']
    
    for indicator in usa_indicators:
        if indicator in location or indicator in description:
            return True
    
    # Check for state abbreviations
    states = ['ca', 'tx', 'fl', 'ny', 'il', 'pa', 'oh', 'ga', 'nc', 'mi', 'nj']
    for state in states:
        if f", {state}" in location or f" {state} " in location:
            return True
    
    # Check for timezone (crude but helpful)
    # Most USA accounts post during USA hours
    
    return False

def contains_finance_keywords(text: str) -> bool:
    """Check if text contains finance-related keywords"""
    finance_keywords = [
        'debt', 'credit', 'money', 'finance', 'budget', 'save', 'invest',
        'loan', 'mortgage', 'bank', 'cash', 'income', 'expense', 'bill',
        'financial', 'crisis', 'emergency', 'debt', 'collection', 'score',
        'interest', 'payment', 'wealth', 'poor', 'rich', 'broke', 'struggle',
        'paycheck', 'rent', 'utilities', 'insurance', 'retirement', '401k',
        'hardship', 'negotiate', 'creditor', 'collector', 'owe', 'borrow'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in finance_keywords)

# ============================================================================
# 🤖 MAIN BOT CLASS
# ============================================================================

class FinanceGrowthBot:
    def __init__(self):
        self.handle = os.getenv('BLUESKY_HANDLE', '')
        self.password = os.getenv('BLUESKY_PASSWORD', '')
        self.client = None
        
        # Counters
        self.comment_counter = 0
        self.shop_link_counter = 0  # Every 5th comment includes shop link
        self.commented_posts = set()  # Avoid commenting same post twice
        
        # Performance tracking
        self.stats_file = 'finance_bot_stats.json'
        self.comments_file = 'posted_comments.json'
        
        # Settings
        self.max_comments_per_day = 25
        self.min_post_likes = 100  # Only engage with popular posts
        self.max_comments_per_hour = 3
        self.min_time_between_comments = 300  # 5 minutes
        
        print(f"🤖 Finance Growth Bot initialized")
        print(f"📊 {len(FINANCIAL_SENTENCES)} financial sentences loaded")
    
    # ============================================================================
    # 🔗 SHOP LINK MANAGEMENT
    # ============================================================================
    
    def should_add_shop_link(self) -> bool:
        """Every 5th comment includes the shop link"""
        self.comment_counter += 1
        return self.comment_counter % 5 == 0
    
    def format_with_shop_link(self, comment: str) -> str:
        """Add shop link to comment"""
        shop_link = "https://www.payhip.com/daveprime"
        
        # Different CTAs for variety
        ctas = [
            f"\n\n👉 For actionable templates and scripts: {shop_link}",
            f"\n\n🔗 Step-by-step guides available: {shop_link}",
            f"\n\n📘 Detailed worksheets and scripts: {shop_link}",
            f"\n\n💡 Want the exact templates? {shop_link}",
            f"\n\n🎯 Get the complete toolkit: {shop_link}"
        ]
        
        return comment + random.choice(ctas)
    
    # ============================================================================
    # 🎯 POST SELECTION STRATEGY
    # ============================================================================
    
    def find_target_posts(self, limit: int = 50) -> List[Dict]:
        """Find popular finance-related posts from US accounts"""
        print("🔍 Searching for target posts...")
        
        try:
            # Get timeline - looking for popular posts
            timeline = self.client.get_timeline(limit=100)
            target_posts = []
            
            for item in timeline.feed:
                post = item.post
                
                # Skip own posts
                if post.author.did == self.client.me.did:
                    continue
                
                # Check if already commented
                if post.uri in self.commented_posts:
                    continue
                
                # Check post popularity
                if post.like_count < self.min_post_likes:
                    continue
                
                # Get post text
                post_text = post.record.text if hasattr(post.record, 'text') else ""
                
                # Check for finance keywords
                if not contains_finance_keywords(post_text):
                    continue
                
                # Get author profile
                try:
                    profile = self.client.get_profile(post.author.did)
                    
                    # Check if USA account
                    if is_usa_account(profile):
                        target_posts.append({
                            'uri': post.uri,
                            'cid': post.cid,
                            'text': post_text,
                            'author': post.author.handle,
                            'likes': post.like_count,
                            'replies': post.reply_count,
                            'reposts': post.repost_count,
                            'author_did': post.author.did
                        })
                        
                        if len(target_posts) >= limit:
                            break
                            
                except Exception as e:
                    continue
            
            print(f"🎯 Found {len(target_posts)} target posts")
            return target_posts
            
        except Exception as e:
            print(f"❌ Error finding target posts: {e}")
            return []
    
    # ============================================================================
    # 💬 COMMENT STRATEGY
    # ============================================================================
    
    def generate_comment(self, post_text: str) -> str:
        """Generate relevant financial comment"""
        
        # Analyze post to make relevant comment
        if any(word in post_text.lower() for word in ['debt', 'owe', 'collection']):
            category = 'debt'
        elif any(word in post_text.lower() for word in ['budget', 'save', 'spend']):
            category = 'budget'
        elif any(word in post_text.lower() for word in ['crisis', 'emergency', 'hardship']):
            category = 'crisis'
        else:
            category = 'general'
        
        # Select sentences from appropriate category
        if category == 'debt':
            sentences = FINANCIAL_SENTENCES[:25]
        elif category == 'budget':
            sentences = FINANCIAL_SENTENCES[25:50]
        elif category == 'crisis':
            sentences = FINANCIAL_SENTENCES[50:75]
        else:
            sentences = FINANCIAL_SENTENCES
        
        # Pick 1-2 sentences
        num_sentences = random.choice([1, 1, 2])  # Mostly 1, sometimes 2
        selected = random.sample(sentences, num_sentences)
        comment = " ".join(selected)
        
        # Add shop link if it's the 5th comment
        if self.should_add_shop_link():
            comment = self.format_with_shop_link(comment)
            print("🔗 Adding shop link (every 5th comment)")
        
        return comment
    
    def post_comment(self, post_uri: str, post_cid: str, comment: str) -> bool:
        """Post comment to a post"""
        try:
            # Create reply
            parent_ref = models.create_strong_ref(post_uri, post_cid)
            
            self.client.send_post(
                comment,
                reply_to=models.AppBskyFeedPost.ReplyRef(
                    parent=parent_ref,
                    root=parent_ref
                )
            )
            
            # Mark as commented
            self.commented_posts.add(post_uri)
            self.save_comment(post_uri, comment)
            
            print(f"💬 Commented on post")
            print(f"   Text: {comment[:80]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to comment: {e}")
            return False
    
    # ============================================================================
    # 📊 STATS & TRACKING
    # ============================================================================
    
    def load_stats(self):
        """Load bot statistics"""
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except:
            return {
                'total_comments': 0,
                'comments_today': 0,
                'last_reset': datetime.now().isoformat(),
                'shop_links_posted': 0
            }
    
    def save_stats(self, stats: Dict):
        """Save bot statistics"""
        # Reset daily counter if new day
        last_reset = datetime.fromisoformat(stats['last_reset'])
        if datetime.now().date() > last_reset.date():
            stats['comments_today'] = 0
            stats['last_reset'] = datetime.now().isoformat()
        
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def load_commented_posts(self):
        """Load previously commented posts"""
        try:
            with open(self.comments_file, 'r') as f:
                comments = json.load(f)
                return set([c['post_uri'] for c in comments])
        except:
            return set()
    
    def save_comment(self, post_uri: str, comment: str):
        """Save comment to history"""
        try:
            with open(self.comments_file, 'r') as f:
                comments = json.load(f)
        except:
            comments = []
        
        comments.append({
            'post_uri': post_uri,
            'comment': comment,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 1000 comments
        if len(comments) > 1000:
            comments = comments[-1000:]
        
        with open(self.comments_file, 'w') as f:
            json.dump(comments, f, indent=2)
    
    # ============================================================================
    # 🚀 MAIN EXECUTION
    # ============================================================================
    
    def run(self):
        """Main bot execution"""
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
        
        # Load previous data
        self.commented_posts = self.load_commented_posts()
        stats = self.load_stats()
        
        print(f"📊 Previously commented: {len(self.commented_posts)} posts")
        print(f"📊 Comments today: {stats['comments_today']}/{self.max_comments_per_day}")
        
        # Check daily limit
        if stats['comments_today'] >= self.max_comments_per_day:
            print("⏹️ Daily comment limit reached")
            return
        
        # Find target posts
        target_posts = self.find_target_posts(limit=10)
        
        if not target_posts:
            print("🎯 No suitable posts found")
            return
        
        # Sort by engagement (likes + replies + reposts)
        target_posts.sort(key=lambda x: x['likes'] + x['replies']*2 + x['reposts']*3, reverse=True)
        
        # Take top 3 most engaging posts
        top_posts = target_posts[:3]
        
        print(f"🎯 Engaging with {len(top_posts)} top posts")
        
        # Comment on each post
        comments_posted = 0
        
        for i, post in enumerate(top_posts):
            # Check daily limit
            if stats['comments_today'] >= self.max_comments_per_day:
                print("⏹️ Daily limit reached")
                break
            
            # Rate limiting
            if i > 0:
                delay = random.randint(self.min_time_between_comments, 
                                     self.min_time_between_comments * 2)
                print(f"⏳ Waiting {delay//60} minutes before next comment...")
                time.sleep(delay)
            
            print(f"\n📝 Post {i+1}/{len(top_posts)}")
            print(f"   👤 @{post['author']}")
            print(f"   👍 {post['likes']} likes, 💬 {post['replies']} replies")
            print(f"   📝 {post['text'][:100]}...")
            
            # Generate comment
            comment = self.generate_comment(post['text'])
            
            # Post comment
            success = self.post_comment(post['uri'], post['cid'], comment)
            
            if success:
                comments_posted += 1
                stats['comments_today'] += 1
                stats['total_comments'] = stats.get('total_comments', 0) + 1
                
                # Update shop link counter
                if self.comment_counter % 5 == 0:
                    stats['shop_links_posted'] = stats.get('shop_links_posted', 0) + 1
        
        # Save stats
        self.save_stats(stats)
        
        # Summary
        print("\n" + "="*50)
        print("📊 BOT SUMMARY")
        print("="*50)
        print(f"💬 Comments posted: {comments_posted}")
        print(f"📅 Comments today: {stats['comments_today']}/{self.max_comments_per_day}")
        print(f"🔗 Shop links posted: {stats.get('shop_links_posted', 0)}")
        print(f"🎯 Next shop link at comment #{5 - (self.comment_counter % 5)}")
        print("="*50)

# ============================================================================
# 🎪 MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    # Check environment
    if not os.getenv('BLUESKY_HANDLE') or not os.getenv('BLUESKY_PASSWORD'):
        print("❌ Missing Bluesky credentials")
        print("Set BLUESKY_HANDLE and BLUESKY_PASSWORD environment variables")
        exit(1)
    
    # Run bot
    bot = FinanceGrowthBot()
    bot.run()
