import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen


class Watcher(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.restart_bot()

    def restart_bot(self):
        if self.process:
            self.process.terminate()  # 结束当前进程
            self.process.wait()
        self.process = Popen([sys.executable, self.script_name])  # 重新启动 BOT

    def on_any_event(self, event):
        if event.src_path.endswith(".py") and event.event_type in (
            "modified",
            "created",
            "deleted",
        ):
            print(f"Detected changes in {event.src_path}. Restarting bot...")
            self.restart_bot()


if __name__ == "__main__":
    path = "."  # 监控当前目录
    script_name = "bot.py"
    event_handler = Watcher(script_name)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print(f"Monitoring {path} for changes. Press Ctrl+C to exit.")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
