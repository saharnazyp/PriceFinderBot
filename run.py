"""Entry point. Usage:
    python run.py telegram
    python run.py bale
    python run.py test "شیر کم چرب"
"""
import asyncio
import sys

from dotenv import load_dotenv

load_dotenv()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    mode = sys.argv[1]

    if mode == "telegram":
        from bot.handlers.telegram_bot import main as tg_main
        tg_main()
    elif mode == "bale":
        from bot.handlers.bale_bot import run as bale_run
        asyncio.run(bale_run())
    elif mode == "test":
        query = sys.argv[2] if len(sys.argv) > 2 else "شیر"
        from bot.core import handle_query
        path, summary, errors = asyncio.run(handle_query(query))
        print("Excel:", path)
        print("Summary:", summary)
        print("Errors:", errors)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
