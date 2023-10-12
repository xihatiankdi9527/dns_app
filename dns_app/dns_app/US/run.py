from flask import Flask, request, jsonify
import logging
import socket
import requests

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = int(request.args.get('as_port'))

    logging.info("收到请求: {}，{}，{}，{}，{}".format(hostname, fs_port, number, as_ip, as_port))

    if hostname and fs_port and as_ip and as_port and number:
        # 打开一个UDP端口到AS
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 发送到服务器
        msg = "TYPE=A\nNAME={}".format(hostname)
        client_socket.sendto(msg.encode(), (as_ip, as_port))
        # 接收响应
        modified_message, server_address = client_socket.recvfrom(2048)
        client_socket.close()
        logging.info(modified_message.decode())
        msg_decoded = modified_message.decode()
        splitted = msg_decoded.split('\n')
        name = splitted[1].split('=')[1]
        value = splitted[2].split('=')[1]
        logging.info("来自AS的响应。 name: {} value: {}".format(name, value))
        r = requests.get("http://{}:{}/fibonacci?number={}".format(value, fs_port, number))
        return jsonify(r.json()), 200
    else:
        return jsonify("未提供所需参数"), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
