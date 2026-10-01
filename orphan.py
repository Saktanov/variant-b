import os
import time

pid = os.fork()

if pid == 0:
    print(f"Ребёнок: PID={os.getpid()}, PPID={os.getppid()}")
    time.sleep(10)
    print(f"Через 10 секунд: PID={os.getpid()}, PPID={os.getppid()}")
else:
    print(f"Родитель: PID={os.getpid()}")
    print(f"Ребёнок: PID={pid}")
    os._exit(0)
