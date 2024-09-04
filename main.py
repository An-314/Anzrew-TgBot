import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Application

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量获取 API token
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your BOT.")


def main():
    print("Starting BOT...")
    # 创建 Application 对象
    application = Application.builder().token(API_TOKEN).build()
    # 注册命令处理器
    application.add_handler(CommandHandler("start", start))
    # 启动 BOT，使用轮询模式
    application.run_polling()


if __name__ == "__main__":
    main()
