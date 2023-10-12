from socket import *

server_port = 53533

# 创建套接字
server_socket = socket(AF_INET, SOCK_DGRAM)
# 绑定端口
server_socket.bind(('', server_port))
mappings = {}

# 现在开始监听
print('服务器准备接收消息...')
while True:
    # 接收消息
    message, client_address = server_socket.recvfrom(2048)
    msg_decoded = message.decode()
    print("收到消息: " + msg_decoded)
    
    if 'VALUE' in msg_decoded:  # 注册请求
        print("处理注册请求")  # 注册
        splitted = msg_decoded.split('\n')
        name = splitted[1].split('=')[1]
        value = splitted[2].split('=')[1]
        mappings[name] = value
        print("名称: {} 值: {}".format(name, value))
        server_socket.sendto("success".encode(), client_address)
    else:  # 查询请求
        print("处理查询请求")
        splitted = msg_decoded.split('\n')
        name = splitted[1].split('=')[1]
        print("名称: {}".format(name))
        if name in mappings:
            response = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(
                name,
                mappings[name]
            )
            server_socket.sendto(response.encode(), client_address)