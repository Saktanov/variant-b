import os
import sys
import time

if len(sys.argv) < 3:
    print("Использование: python3 runner.py N команда [аргументы]")
    sys.exit(1)

n = int(sys.argv[1])
command = sys.argv[2:]
children = []

for i in range(n):
    start = time.time()

    pid = os.fork()

    if pid == 0:
        os.execvp(command[0], command)
    else:
        children.append((pid, start))

for pid, start in children:
    _, status = os.waitpid(pid, 0)
    end = time.time()

    if os.WIFEXITED(status):
        code = os.WEXITSTATUS(status)
    else:
        code = -1

    print(
        f"PID={pid}, "
        f"код возврата={code}, "
        f"время работы={end - start:.3f} сек."
    )
