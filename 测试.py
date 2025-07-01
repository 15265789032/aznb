import json
import os

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

# 主功能循环
def main():
    while True:
        print("\n请选择操作：")
        print("1. 录入数据")
        print("2. 删除数据")
        print("3. 查询数据")
        print("4. 查看所有数据")
        print("5. 退出")
        choice = input("输入选项 (1/2/3/4/5): ")

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
            key = input("请输入要查询的键: ")
            if key in data:
                print(f"🔍 查询结果：{key} -> {data[key]}")
            else:
                print("⚠️ 没有找到这个键。")

        elif choice == "4":
            if data:
                print("📖 当前数据库内容：")
                for k, v in data.items():
                    print(f"{k} -> {v}")
            else:
                print("📭 数据库为空。")

        elif choice == "5":
            print("👋 退出程序。")
            break

        else:
            print("❌ 无效选项，请重新输入。")

if __name__ == "__main__":
    main()