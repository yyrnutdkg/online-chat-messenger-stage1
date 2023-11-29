import socket
import os
import time
import threading

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server_address = '/home/vagrant/work/recursion-stage1/udp_socket_file'

connected_clients = []
message_last_time = {}

def check_inactive_clients():
  while True:
    print('start check user active!')
    current_time = time.time()
    inactive_clients = []

    for client, last_time in message_last_time.items():
      if current_time - last_time > 100:
        inactive_clients.append(client)

    for del_client in inactive_clients:
      print('非アクティブユーザ: {}'.format(del_client))
      connected_clients.remove(del_client)
      message_last_time.pop(del_client)

    time.sleep(10)



def start_server():
  try:
    os.unlink(server_address)
  except FileNotFoundError:
    pass

  print('starting up on {}'.format(server_address))
  sock.bind(server_address)

  check_user_thread = threading.Thread(target=check_inactive_clients)
  check_user_thread.start()

  while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    connected_clients.append(address)
    message_last_time[address] = time.time()
    print(message_last_time)

    data_str = data.decode('utf-8')
    userlen, message = data_str.split(':')

    print('received {} bytes from {}'.format(userlen, address))

    print('received {}'.format(message))

    if message:
      message_encoded = message.encode('utf-8')
      for client in connected_clients:
        sent = sock.sendto(message_encoded, client)
        print('sent {}  back to {}'.format(message_encoded, address))


if __name__ == "__main__":
    start_server()
