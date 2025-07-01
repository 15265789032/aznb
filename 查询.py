import json
import os
import sys
from cryptography.fernet import Fernet

# ANSI颜色定义
GREEN = '\033[92m'
RESET = '\033[0m'
SAVE_CURSOR = '\033[s'
RESTORE_CURSOR = '\033[u'
CLEAR_LINE = '\033[K'

# 文件路径
KEY_FILE = "secret.key"
ENC_DB_FILE = "data.json.enc"

# ================= 加密功能 =================

# 生成密钥（只会执行一次）
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

# 加载密钥
def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as f:
        return f.read()

# 保存加密后的数据库
def save_encrypted_data(data, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(json.dumps(data).encode())
    with open(ENC_DB_FILE, 'wb') as f:
        f.write(encrypted)

# 加载并解密数据库
def load_encrypted_data(key):
    if not os.path.exists(ENC_DB_FILE):
        return {}
    with open(ENC_DB_FILE, 'rb') as f:
        encrypted = f.read()
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except Exception:
        print("❌ 数据解密失败，密钥错误或文件损坏")
        exit()

# ================= 主程序逻辑 =================

def query_mode(data):
    while True:
        print("\n🔍 查询模式")
        key = input("请输入数据: ")

        if key.strip().lower() == "m":
            return  # 返回主菜单

        if key in data:
            result = f"{GREEN}{data[key]}{RESET}"
        else:
            result = f"{GREEN}未找到该数据{RESET}"

        # 输出到最后一行
        sys.stdout.write(f"\n{SAVE_CURSOR}{CLEAR_LINE}{result}{RESTORE_CURSOR}\n")
        sys.stdout.flush()

def main():
    key = load_key()
    data = load_encrypted_data(key)

    while True:
        query_mode(data)

        print("\n📋 功能菜单：[1]录入 [2]删除 [3]查看所有 [4]退出")
        choice = input()

        if choice == "1":
            k = input("请写入数据 ")
            v = input("请输入你想要系统反馈的内容: ")
            data[k] = v
            save_encrypted_data(data, key)
            print(f"✅ 已保存：{k} -> {v}")

        elif choice == "2":
            k = input("删除数据 ")
            if k in data:
                del data[k]
                save_encrypted_data(data, key)
                print(f"🗑️ 已删除：{k}")
            else:
                print("⚠️ 未找到该数据")

        elif choice == "3":
            if data:
                print("📖 当前数据库内容：")
                for k, v in data.items():
                    print(f"{k} -> {v}")
            else:
                print("📭 数据库为空。")

        elif choice == "4":
            print("👋 已退出程序。")
            break

        else:
            print("❌ 无效选项，请重新输入。")

if __name__ == "__main__":
    main()