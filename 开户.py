data = [
    {"phone": "13800138000", "id_card": "110101199001011234", "desc": "示例用户1"},
    {"phone": "13900139000", "id_card": "110101199002022345", "desc": "示例用户2"},
]

# 密钥列表
valid_keys = {"aznb", "aznb666"}

def query_by_phone(phone_number):
    for item in data:
        if item["phone"] == phone_number:
            return item
    return None

def add_entry():
    print("进入录入模式，请输入新用户信息：")
    phone = input("请输入手机号：").strip()
    if len(phone) < 5:
        print("手机号格式不正确，录入失败。")
        return
    if query_by_phone(phone):
        print("❌ 该手机号已存在，录入失败。")
        return

    id_card = input("请输入身份证号：").strip()
    if len(id_card) < 5:
        print("身份证号格式不正确，录入失败。")
        return

    desc = input("请输入备注：").strip()

    new_item = {"phone": phone, "id_card": id_card, "desc": desc}
    data.append(new_item)
    print("✅ 新用户信息录入成功！")

def main():
    # 密钥验证
    print("🔐 请输入密钥进入系统")
    key = input("密钥：").strip()
    if key not in valid_keys:
        print("❌ 密钥错误，拒绝访问！")
        return
    
    print("✅ 密钥验证成功，欢迎使用系统！")
    
    while True:
        cmd = input("\n请输入指令（输入手机号查询，输入 'add' 录入，输入 'exit' 退出）：").strip().lower()
        if cmd == "exit":
            print("程序退出。")
            break
        elif cmd == "add":
            add_entry()
        else:
            result = query_by_phone(cmd)
            if result:
                print("查询结果：")
                for k, v in result.items():
                    if v is not None:
                        print(f"{k}: {v}")
            else:
                print("未找到对应数据。")

if __name__ == "__main__":
    main()