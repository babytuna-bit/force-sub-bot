import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

async def cek_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await cek_member(user_id, context):
        await update.message.reply_text("✅ Selamat datang! Kamu sudah join channel.")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID.strip('@')}")],
            [InlineKeyboardButton("✅ Sudah Join", callback_data="cek_join")]
        ]
        await update.message.reply_text(
            "⚠️ Join channel dulu sebelum pakai bot ini!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await cek_member(user_id, context):
        await update.message.reply_text("✅ Silakan gunakan bot!")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID.strip('@')}")],
            [InlineKeyboardButton("✅ Sudah Join", callback_data="cek_join")]
        ]
        await update.message.reply_text(
            "❌ Kamu belum join channel!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def callback_cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if await cek_member(query.from_user.id, context):
        await query.answer("✅ Verified!")
        await query.edit_message_text("✅ Kamu sudah join! Silakan gunakan bot.")
    else:
        await query.answer("❌ Belum join!", show_alert=True)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(callback_cek, pattern="cek_join"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("Bot jalan...")
app.run_polling()
