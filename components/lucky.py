import numpy as np
from telegram import Update
from telegram.ext import CallbackContext


async def random_num(update: Update, context: CallbackContext) -> None:
    mean = 14
    variance = 2
    random_value = np.random.normal(mean, np.sqrt(variance))

    # 获取用户名，如果用户名不存在则使用 first_name
    username = update.message.from_user.username
    if username:
        mention = f"@{username}"
    else:
        mention = update.message.from_user.first_name

    # 回复消息并 @ 请求的用户
    await update.message.reply_text(f"{mention} 你的唧唧长:{random_value:.4f}cm")
