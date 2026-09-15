# 📱 Telegram Integration Setup

Send scraped domain results directly to Telegram with one click!

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Telegram Bot
1. Open Telegram and search for **@BotFather**
2. Send `/start` then `/newbot`
3. Choose a name (e.g., "DORKER Bot")
4. Choose a username (e.g., "dorker_bot")
5. **Copy the BOT_TOKEN** (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Step 2: Get Your Chat ID
1. Search for **@userinfobot** on Telegram
2. Send it any message
3. It will reply with your User ID (e.g., `123456789`)
4. This is your **CHAT_ID**

### Step 3: Configure Environment
Edit `.env.local` in the admin-panel folder:

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789
```

### Step 4: Test
1. Start dev server: `npm run dev`
2. Go to dashboard (`/dashboard`)
3. Click **"📤 SEND TO TELEGRAM"** button
4. Check Telegram - domains will arrive!

---

## 📊 What Gets Sent

**Format:**
```
📊 DORKER - Domain Results

📅 Date: 2026-09-16
🔗 Total Domains: 42

Domains:
example.com
google.com
stackoverflow.com
...
```

**Features:**
- ✅ Unique domains only (no duplicates)
- ✅ Formatted with date and count
- ✅ One message per send
- ✅ Markdown formatted for readability

---

## 🔧 Advanced Usage

### Send to Group/Channel
1. Add bot to group/channel
2. Get the chat ID (negative number, e.g., `-100123456789`)
3. Set `TELEGRAM_CHAT_ID=-100123456789`

### Error Handling
- ✅ "No domains to send" - No data available
- ✅ "Telegram credentials not configured" - Missing BOT_TOKEN or CHAT_ID
- ✅ "Telegram API error" - Network/bot token issue

### Message Status
- Green success: ✅ Sent X domains to Telegram
- Red error: ❌ Error message shown

---

## 🔐 Security

- ✅ Bot token stored in environment variables
- ✅ Never exposed in source code
- ✅ Never logged in production
- ✅ API endpoint protected by authentication

---

## 📌 Dashboard Integration

**Button Location:** DATA_STREAM LIVE section (next to Download Domains)

**Button States:**
- Normal: `📤 SEND TO TELEGRAM`
- Sending: `⏳ SENDING...` (disabled)
- After send: Shows status message (auto-hide after 5 seconds)

---

## 💡 Tips

1. **Batch Sending**: Send all accumulated domains at once
2. **Scheduled**: Can integrate with cron jobs for daily reports
3. **Multiple Chats**: Change TELEGRAM_CHAT_ID to send to different destinations
4. **Notifications**: Set up Telegram notifications for when domains arrive

---

## ❌ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Telegram credentials not configured" | Fill TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env.local |
| "Telegram API error" | Check bot token is correct, bot is in the chat |
| Message not arriving | Verify CHAT_ID is correct, check Telegram privacy settings |
| Button disabled | Wait for previous send to complete |

---

## 📝 Example .env.local

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://fomkvkjdvhgovpzkucvc.supabase.co
NEXT_PUBLIC_SUPABASE_KEY=eyJhbGc...

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=zxcasdqwe321

# JWT Secret
JWT_SECRET=W397aWrqsp...

# Supabase Service Role
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...

# Telegram Bot Integration
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklmnopQRSTuvwxyz
TELEGRAM_CHAT_ID=987654321
```

---

**Ready to send domains to Telegram? Start now! 🚀**
