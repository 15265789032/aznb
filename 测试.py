import threading
import requests
import time

stop_event = threading.Event()

def attack(url, rate_per_second, thread_id):
    interval = 1.0 / rate_per_second  # 每个请求之间的间隔
    session = requests.Session()

    while not stop_event.is_set():
        start = time.perf_counter()

        try:
            response = session.get(url, timeout=5)
            print(f"[Thread-{thread_id}] 请求成功: {response.status_code}")
        except Exception as e:
            print(f"[Thread-{thread_id}] 请求失败: {e}")

        # 保持精确节奏
        elapsed = time.perf_counter() - start
        sleep_time = interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

def start_attack(url, num_threads, rate_per_thread, duration_seconds):
    threads = []

    print(f"\n[!] 正在发起压力测试：")
    print(f"   - 目标地址：{url}")
    print(f"   - 线程数：{num_threads}")
    print(f"   - 每线程请求速率：{rate_per_thread} 次/秒")
    print(f"   - 总速率：{num_threads * rate_per_thread} 次/秒")
    print(f"   - 持续时间：{duration_seconds} 秒\n")

    for i in range(num_threads):
        t = threading.Thread(target=attack, args=(url, rate_per_thread, i+1))
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        time.sleep(duration_seconds)
    finally:
        stop_event.set()
        print("\n[!] 正在停止测试...")

    for t in threads:
        t.join()

    print("[+] 所有线程已安全退出。")

# 示例用法
if __name__ == "__main__":
    target_url = input("请输入目标URL（例如 http://127.0.0.1:8000）：").strip()
    num_threads = int(input("请输入线程数：").strip())
    rate = float(input("请输入每线程每秒请求数：").strip())
    duration = int(input("请输入持续时间（秒）：").strip())

    start_attack(target_url, num_threads, rate, duration)