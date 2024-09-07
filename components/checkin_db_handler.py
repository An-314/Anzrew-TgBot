import sqlite3
import os
import datetime


DB_PATH = os.path.join(os.getcwd(), "data", "checkin.db")


def init_db():
    """
    新建数据库表
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
            checkin_date TEXT,
            count INTEGER DEFAULT 0
        )
        """
    )
    try:
        c.execute("ALTER TABLE checkins ADD COLUMN count INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()


def record_checkin(user_id: int, date: str):
    """
    记录用户打卡，可以累加打卡次数

    Parameters
    ----------
    user_id(int): 用户的 Telegram ID
    date(str): 打卡日期 'YYYY-MM-DD'

    Returns
    -------
    (bool, int) 是否成功打卡，打卡次数
        True, count: 打卡成功，打卡次数
        False, -1: 打卡失败
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()

        # 检查用户是否已经在当天打卡
        c.execute(
            "SELECT count FROM checkins WHERE user_id = ? AND checkin_date = ?",
            (user_id, date),
        )
        result = c.fetchone()

        if result:
            update_count = result[0] + 1
            c.execute(
                "UPDATE checkins SET count = ? WHERE user_id = ? AND checkin_date = ?",
                (update_count, user_id, date),
            )
        else:
            update_count = 1
            c.execute(
                "INSERT INTO checkins (count, user_id, checkin_date) VALUES (?, ?, ?)",
                (update_count, user_id, date),
            )
        conn.commit()
        return True, update_count
    except Exception as e:
        print(f"Error recording checkin: {e}")
        return False, -1
    finally:
        conn.close()


def remove_checkin(user_id: int, date: str):
    """
    删除用户指定日期的打卡记录，撤销一次打卡

    Parameters
    ----------
    user_id: 用户的 Telegram ID
    date(str): 打卡日期 'YYYY-MM-DD'

    Returns
    -------
    (bool, int) 是否成功删除打卡，剩余打卡次数
        True, count: 删除打卡成功，剩余打卡次数
        False, 0: 删除打卡成功，无打卡记录
        False, -1: 删除打卡失败
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()

        # 检查用户当天的打卡记录
        c.execute(
            "SELECT count FROM checkins WHERE user_id = ? AND checkin_date = ?",
            (user_id, date),
        )
        result = c.fetchone()

        if result:
            if result[0] > 1:
                update_count = result[0] - 1
                c.execute(
                    "UPDATE checkins SET count = ? WHERE user_id = ? AND checkin_date = ?",
                    (update_count, user_id, date),
                )
            else:
                update_count = 0
                c.execute(
                    "DELETE FROM checkins WHERE user_id = ? AND checkin_date = ?",
                    (user_id, date),
                )
            conn.commit()
            return True, update_count
        return False, 0
    except Exception as e:
        print(f"Error removing checkin: {e}")
        return False, -1
    finally:
        conn.close()


def get_checkins(user_id: int, year: int, month: int):
    """
    获取用户某月的所有打卡日期和打卡次数

    Parameters
    ----------
    user_id: 用户的 Telegram ID
    year(int): 年份
    month(int): 月份

    Returns
    -------
    [(datetime.date, int)]: 打卡日期和打卡次数元组的列表
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()

        # 获取该用户该月的所有打卡日期和打卡次数
        c.execute(
            """
            SELECT checkin_date, count FROM checkins
            WHERE user_id = ? AND strftime('%Y', checkin_date) = ? AND strftime('%m', checkin_date) = ?
            """,
            (user_id, str(year), str(month).zfill(2)),
        )
        rows = c.fetchall()

        checkin_data = [
            (datetime.datetime.strptime(row[0], "%Y-%m-%d").date(), row[1])
            for row in rows
        ]
        return checkin_data
    except Exception as e:
        print(f"Error fetching checkins: {e}")
        return []
    finally:
        conn.close()
