import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Application

from components import init_db
from components import start, help_command
from components import random_num, checkin, checkin_cancel, show_calendar

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量获取 API token
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")


def main():
    print("Starting BOT...")

    # 初始化数据库
    init_db()

    # 创建 Application 对象
    application = Application.builder().token(API_TOKEN).build()

    # 注册命令处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dick", random_num))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lu", checkin))
    application.add_handler(CommandHandler("lu_cancel", checkin_cancel))
    application.add_handler(CommandHandler("lu_calendar", show_calendar))

    # 启动 BOT，使用轮询模式
    application.run_polling()


if __name__ == "__main__":
    main()
