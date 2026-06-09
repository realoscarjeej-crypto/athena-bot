import discord
from discord.ext import commands
from discord.ui import Select, View, Modal, TextInput, Button
import asyncio
import os
import random
from datetime import datetime
from dotenv import load_dotenv

# Try to load .env file (works locally, fails gracefully on Railway)
try:
    load_dotenv()
except:
    pass

# Get token from environment variable
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not TOKEN:
    print("❌ ERROR: DISCORD_BOT_TOKEN not found!")
    print("Make sure to add it in Railway dashboard")
    exit(1)

print("✅ Token loaded successfully")

load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ==================== CONFIGURATION ====================
TICKET_CATEGORY_ID = 1511408914527158315  # Set this to your category ID where tickets will be created
SUPPORT_ROLE_ID = 1511408857438621840     # Set this to your support staff role ID
LOG_CHANNEL_ID = 1511408957615243284      # Set this to a channel for ticket logs

STAFF_ROLE_NAMES = ["Admin", "Moderator", "Support", "Staff", "Owner"]

# ==================== YOUR CRYPTO WALLETS ====================
BTC_ADDRESS = "bc1q3m936r4hnd6gxfpuweyxu6wkj59zxprzf9ekp0"
ETH_ADDRESS = "0xA0d6251283DB03F69906a35A793BB16ca9b5eD4a"
XMR_ADDRESS = "49o37Hwg84LLjsLDYUdfDpF8ARyzLyqGZ1rE8LPnmzQ16SyLefjevst6FjUbjrhVySNP5nwvfxZBGGnLSeW2mcrfPTe96gN"
USDT_ADDRESS = "0xA0d6251283DB03F69906a35A793BB16ca9b5eD4a"

# ==================== PRODUCT DATABASE (RATS) ====================

PRODUCTS = {
    1: {
        "name": "🔰 BASIC RAT",
        "price": "$25",
        "price_crypto": "0.00047 BTC / 0.018 ETH / 0.080 XMR / 25 USDT",
        "features": [
            "✅ Remote desktop viewing (real-time)",
            "✅ File manager (upload/download)",
            "✅ Keylogging with timestamped logs",
            "✅ Webcam capture (single frame)",
            "✅ Persistence mechanism (registry)",
            "✅ Windows Defender bypass (basic)",
            "✅ Client size: ~2.5MB",
            "✅ Stealth level: Low",
            "✅ 1 concurrent connection",
            "✅ 30 days of updates"
        ],
        "delivery": "24-48 hours"
    },
    2: {
        "name": "⚡ ADVANCED RAT",
        "price": "$50",
        "price_crypto": "0.00094 BTC / 0.035 ETH / 0.16 XMR / 50 USDT",
        "features": [
            "✅ Everything in Basic, plus:",
            "✅ Remote shell (CMD/PowerShell)",
            "✅ Password recovery (all browsers)",
            "✅ Cookie stealer",
            "✅ Discord token grabber",
            "✅ Crypto wallet extraction",
            "✅ Microphone recording",
            "✅ Webcam streaming",
            "✅ Clipboard monitoring",
            "✅ FUD crypter included",
            "✅ Client size: ~3.8MB",
            "✅ Stealth level: Medium",
            "✅ 5 concurrent connections",
            "✅ 90 days of updates"
        ],
        "delivery": "12-24 hours"
    },
    3: {
        "name": "👑 ULTIMATE RAT",
        "price": "$300",
        "price_crypto": "0.0056 BTC / 0.21 ETH / 0.96 XMR / 300 USDT",
        "features": [
            "✅ Everything in Basic + Advanced",
            "✅ Polymorphic engine",
            "✅ Kernel-level rootkit",
            "✅ AI-powered evasion",
            "✅ Full ransomware module",
            "✅ Botnet controller",
            "✅ DDOS module",
            "✅ Full source code",
            "✅ Lifetime updates",
            "✅ Private C2 panel"
        ],
        "delivery": "1-5 days"
    }
}

# ==================== ROBLOX LIMITEDS STOCK ====================

ROBLOX_LIMITEDS = {
    "high": [
        "💎 Sparkle Time Valkyrie – $33,000",
        "💎 1x Bluesteel Fedora – $17,000",
        "💎 Dreamwalker's Dagger – $6,000",
        "1x Poisoned Horns of the Toxic Wasteland – $5,200",
        "1x Silver King of the Night – $1,650",
        "1x The Classic ROBLOX Fedora – $1,540",
        "1x Valkyrie Helm – $1,020"
    ],
    "mid": [
        "1x Silver Emperor of the Night – $740",
        "1x Scissors – $485",
        "1x Gold Emperor of the Night – $495",
        "1x Heart Balloon – $405",
        "1x Green Queen Of the Night – $330",
        "1x Super Super Happy Face – $300"
    ],
    "low": [
        "1x From the Vault: Alpaca Plushie – $240",
        "1x From the Vault: Dozens of Dinosaurs – $165",
        "1x Beast Mode – $165",
        "1x Bubble Trouble – $145",
        "1x ROBLOX Madness Face – $120",
        "1x 8-Bit Royal Crown – $118",
        "1x Captain SteelShanks – $105",
        "1x Bunny Ears – $68",
        "1x 8-Bit HP Bar – $36",
        "1x Pinstripe Fedora – $30",
        "1x Gold Clockwork Headphones – $25"
    ]
}

# ==================== TICKET SYSTEM (BUYING DROPDOWN) ====================

class BuyDropdown(Select):
    """Dropdown menu for purchasing options"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="💰 Buy Robux", description="$5 per 1,000 Robux", emoji="💰", value="buy_robux"),
            discord.SelectOption(label="🎫 Buy Discord Accounts", description="Full access with OG email", emoji="🎫", value="buy_discord"),
            discord.SelectOption(label="💎 Buy ROBLOX Limiteds", description="Any limited from our stock", emoji="💎", value="buy_limited"),
            discord.SelectOption(label="📈 Buy Social Media Followers", description="Instagram, TikTok, Twitch", emoji="📈", value="buy_social"),
            discord.SelectOption(label="🔰 Buy RATs", description="Basic, Advanced, Ultimate", emoji="🔰", value="buy_rat"),
        ]
        super().__init__(placeholder="Select what you want to BUY...", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "buy_robux":
            await interaction.response.send_modal(BuyRobuxModal())
        elif selected == "buy_discord":
            await interaction.response.send_modal(BuyDiscordModal())
        elif selected == "buy_limited":
            await interaction.response.send_modal(BuyLimitedModal())
        elif selected == "buy_social":
            await interaction.response.send_modal(BuySocialModal())
        elif selected == "buy_rat":
            await interaction.response.send_modal(BuyRATModal())


class SellDropdown(Select):
    """Dropdown menu for selling options"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label="💰 Sell ROBLOX Limiteds", description="Cash out your limiteds", emoji="💰", value="sell_limited"),
            discord.SelectOption(label="🎫 Sell Discord Accounts", description="Sell your Discord accounts", emoji="🎫", value="sell_discord"),
            discord.SelectOption(label="❓ Other / Question", description="General inquiry", emoji="❓", value="other"),
        ]
        super().__init__(placeholder="Select what you want to SELL...", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "sell_limited":
            await interaction.response.send_modal(SellLimitedModal())
        elif selected == "sell_discord":
            await interaction.response.send_modal(SellDiscordModal())
        elif selected == "other":
            await interaction.response.send_modal(OtherModal())


class TicketView(View):
    """Main view with both dropdowns"""
    
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BuyDropdown())
        self.add_item(SellDropdown())


# ==================== MODAL FORMS (BUYING) ====================

class BuyRobuxModal(Modal):
    def __init__(self):
        super().__init__(title="💰 Buy Robux", timeout=300)
        self.amount = TextInput(label="Amount Wanted", placeholder="Example: 10,000 Robux ($50)", required=True, max_length=50)
        self.add_item(self.amount)
        self.payment = TextInput(label="Payment Method", placeholder="Crypto, PayPal, CashApp, Venmo, Zelle, Apple Pay", required=True, max_length=100)
        self.add_item(self.payment)
        self.username = TextInput(label="Roblox Username", placeholder="Your Roblox username for delivery", required=True, max_length=50)
        self.add_item(self.username)
        self.extra = TextInput(label="Additional Info", placeholder="Anything else?", required=False, max_length=500)
        self.add_item(self.extra)
    
    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket(interaction, "💰 BUY ROBUX", {
            "Amount Wanted": self.amount.value,
            "Payment Method": self.payment.value,
            "Roblox Username": self.username.value,
            "Additional Info": self.extra.value or "None"
        })


class BuyDiscordModal(Modal):
    def __init__(self):
        super().__init__(title="🎫 Buy Discord Accounts", timeout=300)
        self.quantity = TextInput(label="Quantity", placeholder="How many accounts?", required=True, max_length=10)
        self.add_item(self.quantity)
        self.payment = TextInput(label="Payment Method", placeholder="Crypto, PayPal, CashApp, Venmo, Zelle, Apple Pay", required=True, max_length=100)
        self.add_item(self.payment)
        self.extra = TextInput(label="Additional Info", placeholder="Any specific requirements?", required=False, max_length=500)
        self.add_item(self.extra)
    
    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket(interaction, "🎫 BUY DISCORD ACCOUNTS", {
            "Quantity": self.quantity.value,
            "Payment Method": self.payment.value,
            "Additional Info": self.extra.value or "None"
        })


class BuyLimitedModal(Modal):
    def __init__(self):
        super().__init__(title="💎 Buy ROBLOX Limiteds", timeout=300)
        self.item = TextInput(label="Limited Wanted", placeholder="Example: Sparkle Time Valkyrie", required=True, max_length=200)
        self.add_item(self.item)
        self.payment = TextInput(label="Payment Method", placeholder="Crypto, PayPal, CashApp, Venmo, Zelle, Apple Pay", required=True, max_length=100)
        self.add_item(self.payment)
        self.username = TextInput(label="Roblox Username", placeholder="Your Roblox username", required=True, max_length=50)
        self.add_item(self.username)
        self.extra = TextInput(label="Additional Info", placeholder="Your offer price?", required=False, max_length=500)
        self.add_item(self.extra)
    
    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket(interaction, "💎 BUY ROBLOX LIMITEDS", {
            "Limited Wanted": self.item.value,
            "Payment Method": self.payment.value,
            "Roblox Username": self.username.value,
            "Additional Info": self.extra.value or "None"
        })


class BuySocialModal(Modal):
    def __init__(self):
        super().__init__(title="📈 Buy Social Media Followers", timeout=300)
        self.platform = TextInput(label="Platform", placeholder="Instagram, TikTok, or Twitch", required=True, max_length=20)
        self.add_item(self.platform)
        self.quantity = TextInput(label="Quantity", placeholder="Example: 1,000 followers", required=True, max_length=50)
        self.add_item(self.quantity)
        self.username = TextInput(label="Username/Link", placeholder="Your social media username", required=True, max_length=200)
        self.add_item(self.username)
        self.payment = TextInput(label="Payment Method", placeholder="Crypto, PayPal, CashApp, etc.", required=True, max_length=100)
        self.add_item(self.payment)
        self.extra = TextInput(label="Additional Info", placeholder="Quality preference?", required=False, max_length=500)
        self.add_item(self.extra)
    
    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket(interaction, "📈 BUY SOCIAL MEDIA FOLLOWERS", {
            "Platform": self.platform.value,
            "Quantity": self.quantity.value,
            "Username/Link": self.username.value,
            "Payment Method": self.payment.value,
            "Additional Info": self.extra.value or "None"
        })


class BuyRATModal(Modal):
    def __init__(self):
        super().__init__(title="🔰 Buy RATs", timeout=300)
        self.tier = TextInput(label="Tier", placeholder="Basic ($25), Advanced ($50), or Ultimate ($300)", required=True, max_length=20)
        self.add_item(self.tier)
        self.payment = TextInput(label="Payment Method", placeholder="Crypto only (BTC, ETH, XMR, USDT)", required=True, max_length=100)
        self.add_item(self.payment)
        self.extra = TextInput(label="Additional Info", placeholder="Any customization requests?", required=False, max_length=500)
        self.add_item(self.extra)
    
    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket(interaction, "🔰 BUY RAT", {
            "Tier": self.tier.value,
            "Payment Method": self.payment.value,
            "Additional Info": self.extra.value or "None"
        })


# ==================== MODAL FORMS (SELLING) ====================

class SellLimitedModal(Modal):
    def __init__(self):
        super().__init__(title="💰 Sell Your Limiteds", timeout=300)
        self.item = TextInput(label="Limited You're Selling", placeholder="Example: Poisoned Horns", required=True, max_length=200)
        self.add_item(self.item)
        self.price = TextInput(label="Your Asking Price", placeholder="Example: $500", required=True, max_length=50)
        self.add_item(self.price)
        self.payment = TextInput(label="Preferred Payout Method", placeholder="Crypto, PayPal, etc.", required=True, max_length=100)
        self.add_item(self.payment)
        self.extra = TextInput(label="Additional Info", placeholder="Proof of ownership?", required=False, max_length=500)
        self.add_item(self.extra)
    
    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket(interaction, "💰 SELL LIMITEDS", {
            "Limited Selling": self.item.value,
            "Asking Price": self.price.value,
            "Payout Method": self.payment.value,
            "Additional Info": self.extra.value or "None"
        })


class SellDiscordModal(Modal):
    def __init__(self):
        super().__init__(title="🎫 Sell Discord Accounts", timeout=300)
        self.quantity = TextInput(label="Quantity", placeholder="How many accounts?", required=True, max_length=10)
        self.add_item(self.quantity)
        self.price = TextInput(label="Your Asking Price", placeholder="Total price for all", required=True, max_length=50)
        self.add_item(self.price)
        self.payment = TextInput(label="Preferred Payout Method", placeholder="Crypto, PayPal, etc.", required=True, max_length=100)
        self.add_item(self.payment)
        self.extra = TextInput(label="Additional Info", placeholder="Account details, age, etc.", required=False, max_length=500)
        self.add_item(self.extra)
    
    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket(interaction, "🎫 SELL DISCORD ACCOUNTS", {
            "Quantity": self.quantity.value,
            "Asking Price": self.price.value,
            "Payout Method": self.payment.value,
            "Additional Info": self.extra.value or "None"
        })


class OtherModal(Modal):
    def __init__(self):
        super().__init__(title="❓ General Question", timeout=300)
        self.subject = TextInput(label="Subject", placeholder="What is this regarding?", required=True, max_length=100)
        self.add_item(self.subject)
        self.message = TextInput(label="Message", placeholder="Please provide details...", required=True, max_length=1000, style=discord.TextStyle.paragraph)
        self.add_item(self.message)
    
    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket(interaction, "❓ GENERAL QUESTION", {
            "Subject": self.subject.value,
            "Message": self.message.value
        })


# ==================== TICKET CREATION FUNCTION ====================

async def create_ticket(interaction: discord.Interaction, ticket_type: str, fields: dict):
    user = interaction.user
    guild = interaction.guild
    
    ticket_number = len([c for c in guild.channels if c.name.startswith("ticket-")]) + 1
    channel_name = f"ticket-{user.name.lower().replace(' ', '-')[:20]}-{ticket_number}"
    
    category = None
    if TICKET_CATEGORY_ID:
        category = guild.get_channel(TICKET_CATEGORY_ID)
    if not category:
        category = discord.utils.get(guild.categories, name="TICKETS")
        if not category:
            category = await guild.create_category("TICKETS")
    
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True, embed_links=True),
    }
    
    for role_name in STAFF_ROLE_NAMES:
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
    
    if SUPPORT_ROLE_ID:
        support_role = guild.get_role(SUPPORT_ROLE_ID)
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
    
    try:
        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        
        embed = discord.Embed(
            title=f"🎫 {ticket_type}",
            description=f"**Customer:** {user.mention}\n**User ID:** {user.id}\n**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            color=0x2b2d31,
            timestamp=datetime.now()
        )
        
        for field_name, field_value in fields.items():
            embed.add_field(name=field_name, value=field_value, inline=False)
        
        embed.set_footer(text="Athena's Market • A staff member will assist you shortly")
        
        class CloseButton(View):
            def __init__(self):
                super().__init__(timeout=None)
            
            @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket")
            async def close_button(self, button_interaction: discord.Interaction, button: Button):
                await button_interaction.response.send_message("✅ Ticket will be closed in 5 seconds...", delete_after=5)
                await asyncio.sleep(5)
                await channel.delete()
        
        await channel.send(f"{user.mention}", embed=embed, view=CloseButton())
        
        confirm_embed = discord.Embed(
            title="✅ Ticket Created",
            description=f"Your ticket has been created: {channel.mention}\n\nA staff member will assist you shortly.",
            color=0x2ecc71
        )
        await interaction.response.send_message(embed=confirm_embed, ephemeral=True)
        
        if LOG_CHANNEL_ID:
            log_channel = guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                log_embed = discord.Embed(
                    title="🎫 New Ticket",
                    description=f"**User:** {user.mention}\n**Type:** {ticket_type}\n**Channel:** {channel.mention}",
                    color=0x2ecc71,
                    timestamp=datetime.now()
                )
                await log_channel.send(embed=log_embed)
    
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred: {str(e)}\n\nPlease contact staff directly.",
            color=0xe74c3c
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)


# ==================== COMMAND 1: !ticket ====================

@bot.command(name='ticket', aliases=['create'])
async def create_ticket_message(ctx):
    """Send the ticket creation message with buying and selling dropdowns"""
    
    embed = discord.Embed(
        title="🎫 **Athena's Market Support Center**",
        description="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "**Select an option from the dropdown menus below**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        color=0x1a1a1a,
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="🟢 **BUYING**",
        value="```💰 Robux – $5 per 1,000\n🎫 Discord Accounts – Full access + OG email\n💎 ROBLOX Limiteds – Any item from stock\n📈 Social Media Followers – IG, TikTok, Twitch\n🔰 RATs – Basic ($25) • Advanced ($50) • Ultimate ($300)```",
        inline=False
    )
    
    embed.add_field(
        name="🔴 **SELLING**",
        value="```💰 ROBLOX Limiteds – Cash out for good rates\n🎫 Discord Accounts – Sell your accounts\n❓ General Questions – Any other inquiries```",
        inline=False
    )
    
    embed.add_field(
        name="📌 **How It Works**",
        value="1️⃣ Select what you want to buy or sell from the dropdowns\n"
              "2️⃣ Fill out the form with your details\n"
              "3️⃣ A private ticket will be created for you\n"
              "4️⃣ A staff member will assist you shortly",
        inline=False
    )
    
    embed.set_footer(
        text="Athena's Market • Secure & Fast Service • Est. 2022",
        icon_url="https://cdn.discordapp.com/attachments/1511408949427962119/1512908488404242482/static_1.png?ex=6a291914&is=6a27c794&hm=cd8b5ea48916dc94e66c9703dc763275073108760b44a79ad1f1d8d40f50042d"
    )
    
    await ctx.send(embed=embed, view=TicketView())


# ==================== COMMAND 2: !rats ====================

@bot.command(name='rats', aliases=['shop', 'catalog', 'products', 'menu', 'pricing'])
async def show_shop(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="🔥 ATHENA'S MARKET - RAT CATALOG 🔥",
        description="**Premium Remote Access Tools**\n*For authorized security research only*",
        color=0xff0000,
        timestamp=datetime.now()
    )
    
    embed.set_footer(text="DM to purchase | Athena's Market Est. 2022")
    
    for opt_id, product in PRODUCTS.items():
        feature_text = "\n".join(product["features"])
        embed.add_field(
            name=f"{product['name']} – {product['price']}",
            value=f"```diff\n{feature_text}\n```\n📦 Delivery: {product['delivery']}\n💳 Crypto: {product['price_crypto']}",
            inline=False
        )
    
    await ctx.send(embed=embed)


# ==================== COMMAND 3: !option ====================

@bot.command(name='option')
async def select_option(ctx, option: int):
    try:
        await ctx.message.delete()
    except:
        pass
    
    if option not in PRODUCTS:
        await ctx.send("❌ Invalid option. Use `!option 1`, `!option 2`, or `!option 3`", delete_after=5)
        return
    
    product = PRODUCTS[option]
    
    try:
        dm_embed = discord.Embed(
            title=f"📦 {product['name']} – Purchase Information",
            description=f"**Price:** {product['price']}\n**Crypto:** {product['price_crypto']}\n**Delivery:** {product['delivery']}",
            color=0x00ff00
        )
        
        if option == 1:
            amount_btc = "0.00038 BTC"
            amount_eth = "0.0068 ETH"
            amount_xmr = "0.42 XMR"
            amount_usdt = "25 USDT"
        elif option == 2:
            amount_btc = "0.00076 BTC"
            amount_eth = "0.0136 ETH"
            amount_xmr = "0.84 XMR"
            amount_usdt = "50 USDT"
        else:
            amount_btc = "0.0046 BTC"
            amount_eth = "0.082 ETH"
            amount_xmr = "5.05 XMR"
            amount_usdt = "300 USDT"
        
        dm_embed.add_field(
            name="📝 PAYMENT INSTRUCTIONS",
            value=f"```\n1. Send the exact amount to one of these addresses:\n\n"
                  f"   BTC ({amount_btc}): {BTC_ADDRESS}\n"
                  f"   ETH ({amount_eth}): {ETH_ADDRESS}\n"
                  f"   XMR ({amount_xmr}): {XMR_ADDRESS}\n"
                  f"   USDT ({amount_usdt}): {USDT_ADDRESS}\n\n"
                  f"2. DM the server owner with proof of payment\n"
                  f"3. Receive your RAT within {product['delivery']}\n\n"
                  f"⚠️ NO REFUNDS after delivery\n"
                  f"⚠️ EDUCATIONAL PURPOSES ONLY\n```",
            inline=False
        )
        
        await ctx.author.send(embed=dm_embed)
        await ctx.send("📬 Check your DMs!", delete_after=5)
    except:
        await ctx.send("❌ I can't DM you! Please enable DMs.", delete_after=15)


# ==================== COMMAND 4: !disboard ====================

@bot.command(name='disboard', aliases=['selling', 'accounts', 'fkt'])
async def sell_discord_accounts(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="🎫 ATHENA'S MARKET - ACCOUNT SHOP",
        description="selling **@fkt** on discord",
        color=0x5865F2,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="✅ What You Get", value="• Full email access\n• Full Discord account access (OG email)", inline=False)
    embed.add_field(name="📩 How to Purchase", value="Open a ticket or DM me for any other questions", inline=False)
    embed.add_field(name="⚠️ Warranty", value="If anything happens to the account **AFTER seven days**, that's not our problem anymore.", inline=False)
    embed.set_footer(text="First come, first served | Stock limited")
    
    await ctx.send(embed=embed)


# ==================== COMMAND 5: !restock ====================

@bot.command(name='restock', aliases=['limiteds', 'roblox', 'items', 'stock'])
async def sell_limiteds(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="💎 UPDATED LIMITEDS STOCK",
        description="**Items + USD Is Welcomed** | **Can Provide Any Item For The Right Price**",
        color=0x00ff00,
        timestamp=datetime.now()
    )
    
    high_tier = "\n".join(ROBLOX_LIMITEDS["high"])
    mid_tier = "\n".join(ROBLOX_LIMITEDS["mid"])
    low_tier = "\n".join(ROBLOX_LIMITEDS["low"])
    
    embed.add_field(name="🏆 HIGH TIER", value=high_tier, inline=False)
    embed.add_field(name="⭐ MID TIER", value=mid_tier, inline=False)
    embed.add_field(name="🎯 LOW TIER", value=low_tier, inline=False)
    
    embed.add_field(
        name="💳 Payment Methods",
        value="Crypto (No Fee) • PayPal (5% Fee) • Zelle (5% Fee) • CashApp (7% Fee) • Apple Pay (7% Fee) • Venmo (7% Fee)",
        inline=False
    )
    
    embed.add_field(
        name="🔒 Guarantee",
        value="14 Days Money Back Guaranteed In Rare Case Of Removal\nAlso Cashing Out Your Limiteds For Good Rates",
        inline=False
    )
    
    embed.set_footer(text="Open a ticket or DM to purchase | Stock updates daily")
    
    await ctx.send(embed=embed)


# ==================== COMMAND 6: !social ====================

@bot.command(name='social', aliases=['followers', 'ig', 'tiktok', 'twitch', 'bots'])
async def sell_followers(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="📈 SOCIAL MEDIA GROWTH PACKAGES",
        description="**Botted Followers – Fast & Affordable**",
        color=0xe1306c,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="📸 INSTAGRAM FOLLOWERS", value="```\n• $5 per 1,000 followers\n• Fast delivery (24-48 hours)\n• No password required\n• Drop protection (30 days)\n```", inline=False)
    embed.add_field(name="🎮 TWITCH FOLLOWERS", value="```\n• $10 per 200 followers\n• Instant start\n• Realistic usernames\n• 30-day refill guarantee\n```", inline=False)
    embed.add_field(name="📱 TIKTOK FOLLOWERS – LOW QUALITY", value="```\n• $5 per 1,000 followers\n• 24-48 hour delivery\n• Basic profiles\n• No refill\n```", inline=False)
    embed.add_field(name="📱 TIKTOK FOLLOWERS – HIGH QUALITY", value="```\n• $8 per 1,000 followers\n• 12-24 hour delivery\n• Custom usernames/pfps\n• 30-day refill\n```", inline=False)
    embed.add_field(name="📱 TIKTOK FOLLOWERS – HIGH QUALITY + 30D REFILL", value="```\n• $15 per 1,000 followers\n• 6-12 hour delivery\n• Premium accounts\n• 30-day refill guarantee\n```", inline=False)
    embed.add_field(name="💳 PAYMENT METHODS", value="Crypto • PayPal • CashApp • Venmo • Zelle • Apple Pay", inline=False)
    embed.add_field(name="📩 HOW TO ORDER", value="DM the server owner with your platform, package, and username.", inline=False)
    
    embed.set_footer(text="Athena's Market | Social Media Growth")
    
    await ctx.send(embed=embed)


# ==================== COMMAND 7: !support ====================

@bot.command(name='support', aliases=['buy', 'contact'])
async def contact_support(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="🛒 ATHENA'S MARKET - PRODUCT CATALOG",
        description="**DM the server owner directly** or use `!ticket` to create a support ticket.",
        color=0xff6600,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="🔰 RATs", value="Basic ($25) • Advanced ($50) • Ultimate ($300)", inline=False)
    embed.add_field(name="🎫 Discord Accounts", value="Full access • OG email • 7-day warranty", inline=False)
    embed.add_field(name="💎 ROBLOX Limiteds", value="20+ limited items • $25 to $33,000 • 14-day guarantee", inline=False)
    embed.add_field(name="📈 Social Media", value="Instagram • TikTok • Twitch followers", inline=False)
    embed.add_field(name="💳 Accepted Payments", value="Crypto • PayPal • Zelle • CashApp • Apple Pay • Venmo", inline=False)
    
    embed.set_footer(text="Athena's Market | Professional • Discreet • Reliable | Est. 2022")
    
    await ctx.send(embed=embed)


# ==================== COMMAND 8: !payments ====================

@bot.command(name='payments', aliases=['payment', 'pay', 'crypto', 'methods'])
async def show_payments(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="💳 ACCEPTED PAYMENT METHODS",
        description="Athena's Market – Safe & Secure Transactions",
        color=0x2ecc71,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="₿ CRYPTOCURRENCY (No Fee)", value="• Bitcoin (BTC)\n• Ethereum (ETH)\n• Monero (XMR)\n• Tether (USDT)", inline=False)
    embed.add_field(name="💸 DIGITAL WALLETS", value="• PayPal (5% Fee)\n• CashApp (7% Fee)\n• Venmo (7% Fee)\n• Zelle (5% Fee)\n• Apple Pay (7% Fee)", inline=False)
    embed.add_field(name="📌 HOW TO PAY", value="1️⃣ DM the server owner or open a ticket\n2️⃣ Confirm the total price\n3️⃣ Send payment\n4️⃣ Send proof\n5️⃣ Receive your product", inline=False)
    
    embed.set_footer(text="Athena's Market | Est. 2022")
    
    await ctx.send(embed=embed)


# ==================== COMMAND 9: !rules ====================

@bot.command(name='rules', aliases=['serverrules', 'conduct'])
async def show_rules(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="📏 SERVER RULES",
        description="Violations = warnings → mutes → kicks → bans",
        color=0xffaa00,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="1️⃣ Be Respectful", value="• No harassment, hate speech, or doxxing", inline=False)
    embed.add_field(name="2️⃣ No Scamming", value="• No fake vouches • No impersonating staff • Scammers will be publicly listed", inline=False)
    embed.add_field(name="3️⃣ No Spam", value="• No excessive @mentions • No unsolicited DMs", inline=False)
    embed.add_field(name="⚠️ Enforcement", value="• 1st: Warning • 2nd: 7-day mute • 3rd: Kick • Severe: Immediate ban", inline=False)
    
    embed.set_footer(text="Athena's Market | Updated: June 2026")
    
    await ctx.send(embed=embed)


# ==================== COMMAND 10: !tos ====================

@bot.command(name='tos', aliases=['terms', 'policy', 'legal'])
async def show_tos(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="📜 TERMS OF SERVICE",
        description="By purchasing from this server, you agree to these Terms.",
        color=0xff4444,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="💎 Digital Goods Policy", value="• All sales are final\n• Refunds only if seller fails to deliver within 48 hours", inline=False)
    embed.add_field(name="💰 Refund Policy", value="• RATs: No refunds\n• Discord Accounts: 7-day warranty\n• ROBLOX Limiteds: 14-day guarantee", inline=False)
    embed.add_field(name="⚠️ Disclaimers", value="• RATs are for educational purposes only\n• Use at your own risk", inline=False)
    
    embed.set_footer(text="Athena's Market | Last updated: June 2026")
    
    await ctx.send(embed=embed)


# ==================== COMMAND 11: !about ====================

@bot.command(name='about', aliases=['info', 'faq'])
async def show_about(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="🦉 ATHENA'S MARKET",
        description="Safe & Trusted Market Since 2022",
        color=0x00aaff,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="👤 Who We Are", value="Premium digital goods marketplace since 2022 with hundreds of satisfied customers.", inline=False)
    embed.add_field(name="✅ Why Us?", value="• Safe – No logs, no tracking\n• Trusted – 4+ years verified sales\n• Fast – Delivery within 24 hours\n• Warranty – Guarantees on all products", inline=False)
    embed.add_field(name="📦 What We Offer", value="• RATs ($25-$300)\n• Discord Accounts\n• ROBLOX Limiteds ($25-$33,000)\n• Social Media Followers", inline=False)
    
    embed.set_footer(text="Athena's Market | Professional • Discreet • Reliable")
    
    await ctx.send(embed=embed)


# ==================== RUN THE BOT ====================
# ================= RUN THE BOT =================

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: DISCORD_BOT_TOKEN not found!")
        print("Make sure to add it in Railway dashboard or .env file")
    else:
        print(f"✅ Athena's Market Bot starting...")
        print(f"✅ Commands loaded: !ticket, !rats, !option, !disboard, !restock, !social, !support, !payments, !rules, !tos, !about")
        print(f"✅ Ticket system with 2 dropdowns (Buying + Selling)")
        bot.run(TOKEN)