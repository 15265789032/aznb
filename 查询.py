import json
import os
import sys
import random
import string
import re

# ANSI颜色定义
GREEN = '\033[92m'
RESET = '\033[0m'
SAVE_CURSOR = '\033[s'
RESTORE_CURSOR = '\033[u'
CLEAR_LINE = '\033[K'

DATA_DB = "data.json"
KEYS_DB = "keys.json"

def init_db(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default_data, f)

init_db(DATA_DB, {})
init_db(KEYS_DB, {"__counter__": 0})

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# 查询写入数据，格式统一
def query_mode():
    data = load_data(DATA_DB)
    while True:
        print("\n🔍 查询模式")
        key = input("请输入要查询的数据： ").strip()

        if key.lower() == "m":
            return

        if key in data:
            print(f"{GREEN}✅ 查到结果：{key} -> {data[key]}{RESET}")
        else:
            print(f"{GREEN}❌ 未找到：{key}{RESET}")

# 查询密钥，备注结果用绿色单独一行输出
def query_keys_only():
    keys_db = load_data(KEYS_DB)
    while True:
        print("\n🔍 查询模式")
        key = input("请输入要查询的密钥：").strip()
        if key.lower() == "m":
            break

        if key in keys_db:
            print(f"\n{GREEN}{keys_db[key]}{RESET}")  # 绿色单独一行输出备注
        else:
            print("❌ 未找到该密钥")

def generate_key(index):
    first = f"{random.randint(1, 999):03d}"
    middle = ''.join(random.choices(string.ascii_uppercase, k=4))
    last = f"{index:04d}"
    return first + middle + last

def list_all_keys():
    data = load_data(KEYS_DB)
    pattern = re.compile(r'^\d{3}[A-Z]{4}\d{4}$')

    keys = [(k, v) for k, v in data.items() if pattern.match(k)]

    if not keys:
        print("📭 没有生成过任何密钥。")
    else:
        print("\n🔑 所有生成的密钥：\n")
        for i, (k, v) in enumerate(keys, 1):
            print(f"{i:03d}. {k} -> {v}")
        print(f"\n🧮 共计：{len(keys)} 个密钥。")

def main():
    while True:
        query_mode()

        print("\n📋 功能菜单：")
        print("[1] 录入写入数据")
        print("[2] 删除写入数据")
        print("[3] 查看所有写入数据")
        print("[4] 退出")
        print("[5] 生成密钥")
        print("[6] 列出所有密钥")
        print("[7] 查询密钥")

        choice = input()

        data_db = load_data(DATA_DB)
        keys_db = load_data(KEYS_DB)

        if choice == "1":
            key = input("请写入数据：")
            value = input("请输入你想要系统反馈的内容：")
            data_db[key] = value
            save_data(DATA_DB, data_db)
            print(f"✅ 已保存写入数据：{key} -> {value}")

        elif choice == "2":
            key = input("删除写入数据：")
            if key in data_db:
                del data_db[key]
                save_data(DATA_DB, data_db)
                print(f"🗑️ 已删除写入数据：{key}")
            else:
                print("⚠️ 未找到该写入数据")

        elif choice == "3":
            if data_db:
                print("📖 当前写入数据内容：")
                for k, v in data_db.items():
                    print(f"{k} -> {v}")
            else:
                print("📭 写入数据库为空。")

        elif choice == "4":
            print("👋 已退出程序。")
            break

        elif choice == "5":
            try:
                count = int(input("请输入要生成的密钥数量："))
                if count <= 0:
                    print("❗ 数量必须大于 0")
                    continue

                current_counter = keys_db.get("__counter__", 0)
                print("\n🔐 正在生成密钥，每行一个，便于复制：\n")

                for i in range(1, count + 1):
                    current_counter += 1
                    key = generate_key(current_counter)
                    print(f"{GREEN}{key}{RESET}")
                    remark = input("请输入备注：")
                    keys_db[key] = remark

                keys_db["__counter__"] = current_counter
                save_data(KEYS_DB, keys_db)
                print(f"\n✅ 共生成 {count} 个密钥并已保存。\n")

            except ValueError:
                print("❌ 无效输入，请输入数字。")

        elif choice == "6":
            list_all_keys()

        elif choice == "7":
            query_keys_only()

        else:
            print("❌ 无效选项，请重新输入。")

if __name__ == "__main__":
    main()