import socket
import os
import time
import threading

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

server_address = '/home/vagrant/work/recursion-stage1/udp_socket_file'
address = '/home/vagrant/work/recursion-stage1/udp_client_socket_file'


def start_client():

  sock.bind(address)

  check_received_message_thread = threading.Thread(target=check_received_message)
  check_received_message_thread.start()

  try:
    input_username = input('ユーザ名を入力: ')
    input_message = input('メッセージを入力: ')

    username_len = len(input_username)

    message_with_userlen = f"{username_len}:{input_message}"

    print('送信メッセージ: {}'.format(message_with_userlen))

    message_encoded = message_with_userlen.encode('utf-8')
    sent = sock.sendto(message_encoded, server_address)

    print('waiting to receive')
    data, server = sock.recvfrom(4096)

    data_decoded = data.decode('utf-8')
    print('received {}'.format(data_decoded))

  finally:
    print('closing socket')
    sock.close()

    try:
      os.unlink(address)
    except FileNotFoundError:
      pass


def check_received_message():
  while True:
    print('check message')
    data, server = sock.recvfrom(4096)

    if data:
      data_decoded = data.decode('utf-8')
      print('received {}'.format(data_decoded))

    time.sleep(10)


if __name__ == "__main__":
  start_client()
