# Anzreww的telegram机器人

## 介绍

这是一个基于python-telegram-bot库的telegram机器人，用于提供一些有趣的功能。

## 功能

- `/start`：开始对话
- `/help`：获取帮助
- `/dick`：生成一个随机的长度
- `/lu`：记录🦌生活
- `/lu_calendar`：查看🦌生活日历

## 使用

使用conda创建虚拟环境并安装依赖：

```bash
conda env create -f environment.yml
conda activate BOT
```

运行机器人：

```bash
python bot.py
```

如果希望机器人运行时可以改动代码并实时更新：

```bash
python auto_reboot.py
```