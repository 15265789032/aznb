import threading
import requests
import time

# 停止标志
stop_event = threading.Event()

def attack(url, rate_per_second):
    interval = 1.0 / rate_per_second  # 请求间隔时间（秒）
    session = requests.Session()

    while not stop_event.is_set():
        start_time = time.time()
        try:
            response = session.get(url, timeout=5)
            print(f"[+] 请求成功: {response.status_code}")
        except Exception as e:
            print(f"[-] 请求失败: {e}")
        
        elapsed = time.time() - start_time
        sleep_time = max(0, interval - elapsed)
        time.sleep(sleep_time)

def start_attack(url, num_threads, rate_per_thread, duration_seconds):
    threads = []

    print(f"[!] 开始压力测试: {num_threads} 个线程，每线程 {rate_per_thread} 次/秒，持续 {duration_seconds} 秒")

    for _ in range(num_threads):
        thread = threading.Thread(target=attack, args=(url, rate_per_thread))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    try:
        time.sleep(duration_seconds)
    finally:
        stop_event.set()
        print("[!] 测试结束，正在停止所有线程...")

    for thread in threads:
        thread.join()

    print("[+] 所有线程已停止")

# 示例：自定义参数
if __name__ == "__main__":
    target_url = input("请输入目标URL（例如 http://127.0.0.1:8000）: ")
    threads = int(input("请输入线程数: "))
    rate = float(input("请输入每线程每秒请求次数: "))
    duration = int(input("请输入测试持续时间（秒）: "))

    start_attack(target_url, threads, rate, duration)