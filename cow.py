import os
import time

N = 8_000_000


def get_memory(pid):
    rss = 0
    private_dirty = 0
    shared_dirty = 0

    with open(f"/proc/{pid}/smaps_rollup") as f:
        for line in f:
            if line.startswith("Rss:"):
                rss = int(line.split()[1])
            elif line.startswith("Private_Dirty:"):
                private_dirty = int(line.split()[1])
            elif line.startswith("Shared_Dirty:"):
                shared_dirty = int(line.split()[1])

    return rss, private_dirty, shared_dirty


data = [0] * N

print(f"Родитель PID={os.getpid()}")
print(f"Размер списка: {N:,} элементов")

pid = os.fork()

if pid == 0:
    child_pid = os.getpid()

    rss1, private1, shared1 = get_memory(child_pid)

    print("\nРебёнок ДО изменения:")
    print(f"RSS: {rss1} kB")
    print(f"Private_Dirty: {private1} kB")
    print(f"Shared_Dirty: {shared1} kB")

    page_step = 512

    for i in range(0, N, page_step):
        data[i] = 1

    rss2, private2, shared2 = get_memory(child_pid)

    print("\nРебёнок ПОСЛЕ изменения:")
    print(f"RSS: {rss2} kB")
    print(f"Private_Dirty: {private2} kB")
    print(f"Shared_Dirty: {shared2} kB")

    print("\nРазница:")
    print(f"RSS: {rss2 - rss1:+} kB")
    print(f"Private_Dirty: {private2 - private1:+} kB")
    print(f"Shared_Dirty: {shared2 - shared1:+} kB")

    os._exit(0)

else:
    os.waitpid(pid, 0)
