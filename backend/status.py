import psutil


def get_metrics() -> dict:
    cpu_usage = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory()
    ram_total = ram.total / (1024 ** 3)
    ram_used = ram.used / (1024 ** 3)
    ram_free = ram.free / (1024 ** 3)

    return {"CPU": cpu_usage / 100, "RAM": ram_used / ram_total, "FRAM": ram_free / ram_total}

