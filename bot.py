import asyncio
import logging
import nest_asyncio  # ✅ 加上这行
nest_asyncio.apply()  # ✅ 再加这行

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


# 启用日志输出
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ✅ 替换为你自己的 Bot Token
BOT_TOKEN = "8053714790:AAGjDeDLUtueXDkeJiYeiY9kvC5nzhjuLzY"

# ✅ 替换为你自己的图片 file_id
WELCOME_IMG_ID = "AgACAgUAAxkBAAMJaHPV1eyQ8z_fVK7Yt3k85VxNgTEAAizGMRsZdaFXfuNLuN-INr8BAAMCAAN5AAM2BA"
CARD_100_IMG_ID = "AgACAgUAAxkBAAMLaHPWCFoVFapOwi94fJRCz4B6ycQAAi7GMRsZdaFXEVNSbNcRChIBAAMCAAN4AAM2BA"
CARD_300_IMG_ID = CARD_100_IMG_ID
ORDER_IMG_ID = "AgACAgUAAxkBAAMKaHPV8I7h3xAl2HiT5-KytQJXhwADLcYxGxl1oVcJZsMDFqMUAQEAAwIAA3gAAzYE"
CUSTOMER_IMG_ID = "AgACAgUAAxkBAAMKaHPV8I7h3xAl2HiT5-KytQJXhwADLcYxGxl1oVcJZsMDFqMUAQEAAwIAA3gAAzYE"

# /start 欢迎命令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.first_name or "朋友"
    keyboard = [
        ["🛒 购买油卡 *1 张", "🛒 购买油卡 *3 张"],
        ["📦 查看订单", "💬 联系客服"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    caption = (
        f"👏 欢迎 {name} 加入【🅜 石化卡商自助下单系统】\n\n"
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

# 用户点击按钮后的响应
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🛒 购买油卡 *1 张":
        await update.message.reply_photo(
            photo=CARD_100_IMG_ID,
            caption="💳 **中石化油卡 ¥100**\n⚡ 自动发货\n📥 请联系 @your_support_bot",
            parse_mode="Markdown"
        )
    elif text == "🛒 购买油卡 *3 张":
        await update.message.reply_photo(
            photo=CARD_300_IMG_ID,
            caption="💳 **中石化油卡 ¥300**（3张）\n⚡ 自动发货\n📥 请联系 @your_support_bot",
            parse_mode="Markdown"
        )
    elif text == "📦 查看订单":
        await update.message.reply_photo(
            photo=ORDER_IMG_ID,
            caption="📦 暂未开放\n联系 @your_support_bot",
            parse_mode="Markdown"
        )
    elif text == "💬 联系客服":
        await update.message.reply_photo(
            photo=CUSTOMER_IMG_ID,
            caption="👩‍💻 @your_support_bot 为您服务",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("请点击下方菜单按钮选择服务 👇")

# 主函数
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot 正在运行...")
    await app.run_polling()

# 启动入口（兼容 IDLE / Jupyter / 特殊控制台）
if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        nest_asyncio.apply()
        loop.create_task(main())
    else:
        loop.run_until_complete(main())
