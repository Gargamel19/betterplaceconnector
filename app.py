from flask import Flask
from flask import request
import socket

app = Flask(__name__)
sock = None

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'fettarmqp'
token = 'oauth:h5j4vm7akv4ekgialq7s8hkkwsy262'
channel = '#fettarmqp'


@app.route('/', methods=['GET'])
def hello_world():
    return "Hello"


@app.route('/donation', methods=['POST'])
def donation():
    json_payload = request.json
    cents = int(json_payload['donation']['amount_in_cents'])
    message = json_payload['donation']['comment']
    name = json_payload['donation']['donor_display_name']
    sock.send(f"PRIVMSG {channel} :!tts {name} spendet {str(cents/100)} euro: {message}\n".encode('utf-8'))
    return "okay"

if __name__ == '__main__':

    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    print("PASS")
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    print("NICK")
    resp = sock.recv(2048).decode('utf-8')
    print(resp)
    sock.send(f"JOIN {channel}\n".encode('utf-8'))
    print("JOIN")
    resp = sock.recv(2048).decode('utf-8')
    print(resp)
    resp = sock.recv(2048).decode('utf-8')
    print(resp)
    print("logged in")

    app.run()
