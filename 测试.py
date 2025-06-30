import threading
import requests
import time
from queue import Queue

# =========================
# 任务队列和停止标志
# =========================
task_queue = Queue()
stop_event = threading.Event()

def worker(thread_id, target_url):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            _ = task_queue.get(timeout=1)
        except:
            continue
        try:
            response = session.get(target_url, timeout=5)
            print(f"[线程-{thread_id}] 状态码: {response.status_code}")
        except Exception as e:
            print(f"[线程-{thread_id}] 请求失败: {e}")
        finally:
            task_queue.task_done()

def scheduler(target_url, req_per_sec, duration_sec):
    total_requests = req_per_sec * duration_sec
    interval = 1.0 / req_per_sec  # 每次请求的时间间隔

    print(f"\n[调度器] 计划总请求数: {total_requests}")
    print(f"[调度器] 每请求间隔: {interval:.6f} 秒")

    next_time = time.perf_counter()

    for i in range(total_requests):
        now = time.perf_counter()
        if now < next_time:
            time.sleep(next_time - now)
        task_queue.put(i)
        next_time += interval

    print("\n[调度器] 所有请求任务已调度完毕")

def main():
    print("========== 精确请求压测工具 ==========")
    target_url = input("请输入目标 URL（例如 http://127.0.0.1:8000）：").strip()
    try:
        req_per_sec = int(input("请输入每秒请求数量（如 1000）：").strip())
        duration_sec = int(input("请输入测试持续时间（单位：秒）：").strip())
        num_threads = int(input("请输入使用的线程数（如 10）：").strip())
    except ValueError:
        print("[错误] 参数输入无效，请输入整数。")
        return

    total_req = req_per_sec * duration_sec
    print(f"\n[!] 开始测试：{req_per_sec} 次/秒, 共 {total_req} 次, 使用 {num_threads} 个线程\n")

    # 启动 worker 线程
    workers = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i+1, target_url))
        t.daemon = True
        t.start()
        workers.append(t)

    # 启动调度器
    scheduler_thread = threading.Thread(target=scheduler, args=(target_url, req_per_sec, duration_sec))
    scheduler_thread.start()

    scheduler_thread.join()
    task_queue.join()
    stop_event.set()

    print("\n[✔] 测试完成，所有请求已发送。")

if __name__ == "__main__":
    main()