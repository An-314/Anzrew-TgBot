from telegram import Update
from telegram.ext import CallbackContext


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("主人你好！我是小AnZZnA！")


async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "/start - 机器人的信息\n"
        "/dick - 试试就试试\n"
        "/lu - 记录美好生活\n"
        "/lu_cancel - 取消今日的记录\n"
        "/lu_calendar - 展示本月记录\n"
        "/help - 获取帮助"
    )
    await update.message.reply_text(help_text)
