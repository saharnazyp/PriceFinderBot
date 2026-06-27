"""Telegram bot handler. Uses python-telegram-bot v20+ (async)."""
import logging

from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

from bot.core import handle_query, summary_caption
from config import settings

log = logging.getLogger("telegram")


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋 نام محصولی که دنبالش هستی رو بفرست تا قیمت‌ها رو "
        "از فروشگاه‌های مختلف برات پیدا کنم و توی یک فایل اکسل بدم."
    )


async def on_message(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    msg = await update.message.reply_text("🔍 در حال جستجو... چند لحظه صبر کن.")
    try:
        excel_path, summary, errors = await handle_query(query)
        await update.message.reply_text(summary_caption(query, summary))
        if summary["count"] > 0:
            with open(excel_path, "rb") as f:
                await update.message.reply_document(
                    document=f, filename=excel_path.name)
        if errors:
            log.warning("Scraper errors for '%s': %s", query, errors)
    except Exception as e:  # noqa: BLE001
        log.exception("handle_query failed")
        await update.message.reply_text("خطایی رخ داد. لطفاً دوباره تلاش کن.")
    finally:
        await msg.delete()


def build_app() -> Application:
    app = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    return app


def main():
    logging.basicConfig(level=logging.INFO)
    build_app().run_polling()


if __name__ == "__main__":
    main()
