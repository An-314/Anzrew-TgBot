import sqlite3
import os
import datetime


DB_PATH = os.path.join(os.getcwd(), "data", "checkin.db")


def init_db():
    """
    初始化 SQLite 数据库，创建打卡记录表
    """
    # 检查 /data/ 目录是否存在，如果不存在则创建
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))

    # 创建数据库表
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS checkins (
            user_id INTEGER,
            checkin_date TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def record_checkin(user_id: int, date: str):
    """
    记录用户打卡
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()

        # 检查用户是否已经在当天打卡
        c.execute(
            "SELECT * FROM checkins WHERE user_id = ? AND checkin_date = ?",
            (user_id, date),
        )
        result = c.fetchone()

        if result:
            return False  # 已打卡
        else:
            # 插入新的打卡记录
            c.execute(
                "INSERT INTO checkins (user_id, checkin_date) VALUES (?, ?)",
                (user_id, date),
            )
            conn.commit()
            return True  # 打卡成功
    except Exception as e:
        print(f"Error recording checkin: {e}")
        return False
    finally:
        conn.close()


def remove_checkin(user_id: int, date: str):
    """
    删除用户指定日期的打卡记录
    :param user_id: 用户的 Telegram ID
    :param date: 要删除的打卡日期（格式为 'YYYY-MM-DD'）
    :return: 是否成功删除
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()

        # 删除该用户在指定日期的打卡记录
        c.execute(
            "DELETE FROM checkins WHERE user_id = ? AND checkin_date = ?",
            (user_id, date),
        )
        if c.rowcount == 0:
            return False  # 未找到记录
        conn.commit()
        return True  # 删除成功
    except Exception as e:
        print(f"Error removing checkin: {e}")
        return False
    finally:
        conn.close()


def get_checkins(user_id: int, year: int, month: int):
    """
    获取用户某月的所有打卡日期
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()

        # 获取该用户该月的所有打卡日期
        c.execute(
            """
            SELECT checkin_date FROM checkins
            WHERE user_id = ? AND strftime('%Y', checkin_date) = ? AND strftime('%m', checkin_date) = ?
            """,
            (user_id, str(year), str(month).zfill(2)),
        )
        rows = c.fetchall()
        checkin_dates = [
            datetime.datetime.strptime(row[0], "%Y-%m-%d").date() for row in rows
        ]
        return checkin_dates
    except Exception as e:
        print(f"Error recording checkin: {e}")
        return []
    finally:
        conn.close()
