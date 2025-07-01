import json
import os
import sys

# ANSI颜色定义
GREEN = '\033[92m'
RESET = '\033[0m'
SAVE_CURSOR = '\033[s'
RESTORE_CURSOR = '\033[u'
CLEAR_LINE = '\033[K'

DB_FILE = "data.json"

# 初始化数据库文件
if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def query_mode():
    data = load_data()
    while True:
        print("\n🔍 查询模式（输入 m 返回菜单）")
        key = input("请输入要查询的键: ")

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
    while True:
        query_mode()

        print("\n📋 功能菜单：[1]录入 [2]删除 [3]查看所有 [4]退出")
        choice = input()

        data = load_data()

        if choice == "1":
            key = input("请输入键（例如 2）: ")
            value = input("请输入你想要系统反馈的内容: ")
            data[key] = value
            save_data(data)
            print(f"✅ 已保存：{key} -> {value}")

        elif choice == "2":
            key = input("请输入要删除的键: ")
            if key in data:
                del data[key]
                save_data(data)
                print(f"🗑️ 已删除：{key}")
            else:
                print("⚠️ 未找到该键。")

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