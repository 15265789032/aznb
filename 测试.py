import threading
import requests
import time
from queue import Queue

# =========================
# 可自定义参数
# =========================
NUM_REQUESTS_PER_SECOND = 1000  # 总请求数/秒
DURATION_SECONDS = 10          # 测试时长
TARGET_URL = "http://127.0.0.1:8000"  # 目标URL
NUM_WORKERS = 10               # 工作线程数

# =========================
# 任务队列
# =========================
task_queue = Queue()
stop_event = threading.Event()

def worker(thread_id):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            _ = task_queue.get(timeout=1)
        except:
            continue
        try:
            response = session.get(TARGET_URL, timeout=5)
            print(f"[Worker-{thread_id}] 状态码: {response.status_code}")
        except Exception as e:
            print(f"[Worker-{thread_id}] 请求失败: {e}")
        finally:
            task_queue.task_done()

def scheduler():
    total_requests = NUM_REQUESTS_PER_SECOND * DURATION_SECONDS
    interval = 1.0 / NUM_REQUESTS_PER_SECOND  # 间隔时间（秒）

    print(f"\n[+] 计划总请求数：{total_requests}")
    print(f"[+] 每次发出间隔：{interval:.6f} 秒")

    next_time = time.perf_counter()

    for i in range(total_requests):
        now = time.perf_counter()
        if now < next_time:
            time.sleep(next_time - now)
        task_queue.put(i)
        next_time += interval

    print("\n[+] 所有请求任务已调度完毕")

def main():
    print(f"\n[!] 正在启动测试：{NUM_REQUESTS_PER_SECOND} req/s, {DURATION_SECONDS} 秒，共 {NUM_REQUESTS_PER_SECOND * DURATION_SECONDS} 个请求\n")

    # 启动 worker 线程
    workers = []
    for i in range(NUM_WORKERS):
        t = threading.Thread(target=worker, args=(i+1,))
        t.daemon = True
        t.start()
        workers.append(t)

    # 启动调度器
    scheduler_thread = threading.Thread(target=scheduler)
    scheduler_thread.start()

    # 等待调度结束
    scheduler_thread.join()

    # 等待任务执行完
    task_queue.join()
    stop_event.set()

    print("\n[✔] 测试完成，所有请求已发送。")

if __name__ == "__main__":
    main()