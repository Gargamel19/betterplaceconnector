from flask import Flask
from flask import request
import socket
import os

app = Flask(__name__)

server = os.environ.get("SERVER")
port = int(os.environ.get("PORT_SERVER"))
nickname = os.environ.get("NICKNAME")
token = os.environ.get("TOKEN")
channel = os.environ.get("CHANEL")

sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))
print("logged in")


@app.route('/', methods=['GET'])
def hello_world():
    return "Hello"


@app.route('/donation', methods=['POST'])
def donation():
    json_payload = request.json
    cents = int(json_payload['donation']['amount_in_cents'])
    message = json_payload['donation']['comment']
    name = json_payload['donation']['donor_display_name']
    sock.send(f"PRIVMSG {channel} :[Spende] {name} spendet {str(cents/100)} Euro: {message}\n".encode('utf-8'))
    return "okay"


if __name__ == '__main__':
    app.run()
