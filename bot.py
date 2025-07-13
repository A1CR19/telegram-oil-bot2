from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

from aiohttp import web

# 替换为你自己的 file_id
WELCOME_IMG_ID = "AgACAgUAAxkBAAMFaHNZiJzn1tAn3rcze61gvLf2YBUAAu_MMRsDP5lXvUaRV6ukCLEBAAMCAAN5AAM2BA"
CARD_100_IMG_ID = "AgACAgUAAxkBAAMHaHNcsjxLPznQCfWbm-OsrrlqEjMAAoDEMRvYcJlXAAGRbI7zcn1jAQADAgADeAADNgQ"
CARD_300_IMG_ID = "AgACAgUAAxkBAAMHaHNcsjxLPznQCfWbm-OsrrlqEjMAAoDEMRvYcJlXAAGRbI7zcn1jAQADAgADeAADNgQ"
ORDER_IMG_ID = "AgACAgUAAxkBAAMHaHNcsjxLPznQCfWbm-OsrrlqEjMAAoDEMRvYcJlXAAGRbI7zcn1jAQADAgADeAADNgQ"
CUSTOMER_IMG_ID = "AgACAgUAAxkBAAMGaHNcjZjiMsXTOg09h9Ss90Bg830AAn_EMRvYcJlXKY-YMN3mqOUBAAMCAAN4AAM2BA"

TOKEN = "你的BotToken"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://你的railway地址.up.railway.app" + WEBHOOK_PATH


# /start 欢迎语
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name = user.first_name or user.username or "朋友"

    keyboard = [
        ["🛒 购买油卡 *1 张", "🛒 购买油卡 *3 张"],
        ["📦 查看订单", "💬 联系客服"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    caption = (
        f"👏欢迎 {name} 加入【🅜 石化卡商自助下单系统】\n\n"
        "⚠️ 请确保您的 Telegram 是从 [telegram.org](https://telegram.org) 官网下载\n"
        "❌ 否则可能被篡改地址导致资产丢失！\n\n"
        "📮 示例地址：`jkdlajdlj ajfliejaighidfli`\n"
        "🧩 校验码：前5位 `THTXf` / 后5位 `EHYCQ`\n\n"
        "💬 请点击下方菜单按钮继续操作 👇"
    )

    await update.message.reply_photo(
        photo=WELCOME_IMG_ID,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🛒 购买油卡 *1 张":
        await update.message.reply_photo(
            photo=CARD_100_IMG_ID,
            caption="💳 **中石化油卡 ¥100**\n⚡ 自动发货 | ⏱️ 秒到卡密\n📥 请联系 @your_support_bot 支付后提卡",
            parse_mode="Markdown"
        )

    elif text == "🛒 购买油卡 *3 张":
        await update.message.reply_photo(
            photo=CARD_300_IMG_ID,
            caption="💳 **中石化油卡 ¥300**（3张）\n⚡ 自动发货 | ⏱️ 秒到卡密\n📥 请联系 @your_support_bot 支付后提卡",
            parse_mode="Markdown"
        )

    elif text == "📦 查看订单":
        await update.message.reply_photo(
            photo=ORDER_IMG_ID,
            caption="📦 **订单查询系统**暂未开放\n如需查询请联系 @your_support_bot",
            parse_mode="Markdown"
        )

    elif text == "💬 联系客服":
        await update.message.reply_photo(
            photo=CUSTOMER_IMG_ID,
            caption="👩‍💻 客服 Telegram：@your_support_bot\n我们将尽快为您服务 💬",
            parse_mode="Markdown"
        )

    else:
        await update.message.reply_text("请点击下方菜单按钮选择服务 👇")


async def webhook_handler(request):
    data = await request.json()
    await app.update_queue.put(Update.de_json(data, app.bot))
    return web.Response()

async def on_startup(app):
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.bot.set_webhook(url=WEBHOOK_URL)

def main():
    global app
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # 创建 aiohttp server
    web_app = web.Application()
    web_app.add_routes([web.post(WEBHOOK_PATH, webhook_handler)])
    app.run_web_app(web_app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), on_startup=on_startup)

if __name__ == "__main__":
    main()
