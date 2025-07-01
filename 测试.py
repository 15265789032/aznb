import json
import os

# ANSI颜色代码
GREEN = '\033[92m'
RESET = '\033[0m'

DB_FILE = "data.json"

# 初始化数据库文件
if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump({}, f)

# 载入数据库
def load_data():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

# 保存数据库
def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# 主程序
def main():
    while True:
        data = load_data()

        print("\n🔍 默认查询模式：")
        key = input("请输入要查询的键（直接回车进入菜单）: ")

        query_result = ""
        if key:
            if key in data:
                query_result = f"{GREEN}✅ 查询结果：{key} -> {data[key]}{RESET}"
            else:
                query_result = f"{GREEN}⚠️ 没有找到该键。{RESET}"
        else:
            print("\n📋 功能菜单：[1]录入 [2]删除 [3]查看所有 [4]退出")
            choice = input("请选择功能编号：")

            if choice == "1":
                key = input("请输入键: ")
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

        # 显示查询结果在最后一行
        if query_result:
            print(query_result)

if __name__ == "__main__":
    main()