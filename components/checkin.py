import calendar
import datetime
import matplotlib.pyplot as plt
from matplotlib.table import Table
import os
from telegram import Update
from telegram.ext import CallbackContext

from components.checkin_db_handler import (
    record_checkin,
    remove_checkin,
    get_checkins,
)


async def checkin(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    today = datetime.date.today()

    success = record_checkin(user_id, today.isoformat())

    if success:
        await update.message.reply_text("成功🦌了！！！")
    else:
        await update.message.reply_text("今天您已经🦌过了！！！")


async def checkin_cancel(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    today = datetime.date.today()

    # 调用 remove_checkin 函数删除打卡记录
    success = remove_checkin(user_id, today.isoformat())

    if success:
        await update.message.reply_text("你最好没🦌")
    else:
        await update.message.reply_text("恭喜！！没有🦌记录可以删除！")


async def show_calendar(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year

    checkins = get_checkins(user_id, current_year, current_month)

    cal = calendar.monthcalendar(current_year, current_month)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_axis_off()
    table = Table(ax, bbox=[0, 0, 1, 1])

    # 列标题
    col_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    col_width = 1 / 7
    row_height = 1 / (len(cal) + 1)
    for i, label in enumerate(col_labels):
        table.add_cell(
            0, i, col_width, row_height, text=label, loc="center", facecolor="lightgray"
        )

    # 日期
    for row_num, week in enumerate(cal, 1):  # 第 0 行是星期标题
        for col_num, day in enumerate(week):
            if day == 0:
                table.add_cell(row_num, col_num, col_width, row_height, loc="center")
            else:
                if datetime.date(current_year, current_month, day) in checkins:
                    checkin_mark = "✓"
                else:
                    checkin_mark = ""
                cell_text = f"{day}"
                cell = table.add_cell(
                    row_num,
                    col_num,
                    col_width,
                    row_height,
                    text=cell_text,
                    loc="center",
                    facecolor="white",
                )
                if checkin_mark:
                    plt.text(
                        col_num / 7 + 0.5 / 7,
                        1 - (row_num / (len(cal) + 1)) - 0.05,
                        checkin_mark,
                        ha="center",
                        va="center",
                        fontsize=100,
                        color="red",
                    )
    ax.add_table(table)

    image_path = "checkin_calendar.png"
    plt.savefig(image_path, bbox_inches="tight", dpi=150)
    user = update.message.from_user
    username = f"@{user.username}" if user.username else user.first_name
    await update.message.reply_photo(
        photo=open(image_path, "rb"),
        caption=f"{username}，这是您{current_year}年{current_month}月的🦌记录！",
    )
    os.remove(image_path)
