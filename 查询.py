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

DATA_DB = "data.json"    # 录入/查询数据数据库
KEYS_DB = "keys.json"    # 生成密钥数据库

# 初始化数据库文件
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

def query_mode():
    data = load_data(DATA_DB)
    while True:
        print("\n🔍 查询模式（查询写入数据库）")
        key = input("请输入数据 (输入 m 返回菜单): ")

        if key.strip().lower() == "m":
            return

        if key in data:
            result = f"{GREEN}{data[key]}{RESET}"
        else:
            result = f"{GREEN}未找到该数据{RESET}"

        sys.stdout.write(f"\n{SAVE_CURSOR}{CLEAR_LINE}{result}{RESTORE_CURSOR}\n")
        sys.stdout.flush()

def generate_key(index):
    first = f"{random.randint(1, 999):03d}"
    middle = ''.join(random.choices(string.ascii_uppercase, k=4))
    last = f"{index:04d}"
    return first + middle + last

def list_all_keys():
    data = load_data(KEYS_DB)
    pattern = re.compile(r'^\d{3}[A-Z]{4}\d{4}$')  # 密钥格式

    keys = [(k, v) for k, v in data.items() if pattern.match(k)]
    
    if not keys:
        print("📭 没有生成过任何密钥。")
    else:
        print("\n🔑 所有生成的密钥（从密钥数据库）：\n")
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

        choice = input()

        # 加载数据库
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
                for i in range(1, count + 1):
                    current_counter += 1
                    key = generate_key(current_counter)
                    remark = input(f"🔐 生成密钥：{GREEN}{key}{RESET}，请输入备注：")
                    keys_db[key] = remark

                keys_db["__counter__"] = current_counter
                save_data(KEYS_DB, keys_db)
                print(f"\n✅ 共生成 {count} 个密钥并已保存。\n")

            except ValueError:
                print("❌ 无效输入，请输入数字。")

        elif choice == "6":
            list_all_keys()

        else:
            print("❌ 无效选项，请重新输入。")

if __name__ == "__main__":
    main()