from flask import Flask, request, jsonify
import logging
import socket

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)

def fibonacci_calc(b):
    if b < 0:
        logging.info("数字应大于0")
    elif b == 1:
        return 0
    elif b == 2:
        return 1
    else:
        return fibonacci_calc(b - 1) + fibonacci_calc(b - 2)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    if not number:
        return jsonify('未提供数字'), 400

    logging.info("收到Fibonacci序列号的请求: {}".format(number))

    return jsonify(fibonacci_calc(int(number))), 200

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = int(data.get('as_port'))

    logging.info("收到注册请求: {}，{}，{}，{}".format(
        hostname, ip, as_ip, as_port))

    if hostname and ip and as_ip and as_port:
        # 打开一个UDP端口到AS的端口53533
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 发送给服务器
        msg = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(
            hostname, ip)
        client_socket.sendto(msg.encode(), (as_ip, as_port))

        # 接收响应
        modified_message, server_address = client_socket.recvfrom(2048)
        logging.info(modified_message.decode())

        # 关闭套接字
        client_socket.close()
        if modified_message.decode() == 'success':
            return jsonify('成功'), 201
        else:
            return jsonify('失败'), 500
    else:
        return jsonify('未提供参数'), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=9090,
            debug=True)