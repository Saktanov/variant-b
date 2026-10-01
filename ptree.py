import os

processes = {}

for pid in os.listdir("/proc"):
    if not pid.isdigit():
        continue

    pid = int(pid)

    try:
        with open(f"/proc/{pid}/status") as f:
            data = f.read().splitlines()

        info = {}

        for line in data:
            if ":" in line:
                key, value = line.split(":", 1)
                info[key] = value.strip()

        uid = int(info.get("Uid", "0").split()[0])

        if uid != os.getuid():
            continue

        ppid = int(info.get("PPid", "0"))
        state = info.get("State", "?")
        rss = info.get("VmRSS", "0 kB")

        processes[pid] = {
            "ppid": ppid,
            "state": state,
            "rss": rss
        }

    except (FileNotFoundError, PermissionError, ProcessLookupError):
        continue


children = {}

for pid, info in processes.items():
    ppid = info["ppid"]
    children.setdefault(ppid, []).append(pid)

for ppid in children:
    children[ppid].sort()


def print_tree(pid, level=0):
    if pid not in processes:
        return

    info = processes[pid]

    print(
        "  " * level +
        f"PID={pid} "
        f"STATE={info['state']} "
        f"RSS={info['rss']}"
    )

    for child in children.get(pid, []):
        print_tree(child, level + 1)


roots = []

for pid, info in processes.items():
    if info["ppid"] not in processes:
        roots.append(pid)

roots.sort()

for pid in roots:
    print_tree(pid)

