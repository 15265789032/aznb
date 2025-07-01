import requests
import threading
import time

def send_request(url, rate):
    while True:
        for _ in range(rate):
            try:
                response = requests.get(url)
                print(f"[+] 请求成功: {url} 状态码: {response.status_code}")
            except Exception as e:
                print(f"[-] 请求失败: {e}")
        time.sleep(1)  # 每秒发 rate 次请求

def main():
    print("你想使用域名还是 IP？")
    print("1. 域名（例如：https://www.example.com）")
    print("2. IP 地址（例如：http://192.168.1.100）")
    
    choice = input("请输入 1 或 2：").strip()

    if choice == "1":
        url = input("请输入域名地址（例如：https://www.example.com）：").strip()
    elif choice == "2":
        url = input("请输入 IP 地址（例如：http://192.168.1.100）：").strip()
    else:
        print("无效输入，程序退出")
        return

    try:
        threads = int(input("请输入线程数（建议 1~100）："))
        rate = int(input("请输入每个线程每秒访问次数（建议 1~10）："))
    except ValueError:
        print("线程数和访问频率必须是整数")
        return

    print(f"\n开始测试：共 {threads} 个线程，每个线程每秒 {rate} 次请求，共计每秒约 {threads * rate} 次请求\n")

    for _ in range(threads):
        t = threading.Thread(target=send_request, args=(url, rate))
        t.daemon = True  # 后台线程
        t.start()

    # 防止主线程退出
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()