import socket
import os
import time
import threading

class ChatServer:
  def __init__(self, server_address):
    self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    self.server_address = server_address
    self.connected_clients = []
    self.message_last_time = {}

  def check_inactive_clients(self):
    while True:
      print('Start check user...')
      current_time = time.time()
      inactive_clients = []

      for client, last_time in self.message_last_time.items():
        if current_time - last_time > 100:
          self.inactive_clients.append(client)

      for del_client in inactive_clients:
        print('Inactive user: {}'.format(del_client))
        self.connected_clients.remove(del_client)
        self.message_last_time.pop(del_client)

      time.sleep(10)

  def start_server(self):
    try:
      os.unlink(self.server_address)
    except FileNotFoundError:
      pass

    print('Starting up on {}'.format(self.server_address))
    self.sock.bind(self.server_address)
    check_user_thread = threading.Thread(target=self.check_inactive_clients)
    check_user_thread.start()

    self.handle_received_message()

  def handle_received_message(self):
    while True:
      print('Waiting to receive message....')
      data, address = self.sock.recvfrom(4096)

      data_decoded = data.decode('utf-8')
      userlen, message = data_decoded.split(':')

      self.connected_clients.append(address)
      self.message_last_time[address] = time.time()

      print('Receicved message: {} from {}'.format(userlen, message))

      if message:
        message_encoded = message.encode('utf-8')
        for client in self.connected_clients:
          self.sock.sendto(message_encoded, client)

if __name__ == "__main__":
  server_address = '/home/vagrant/work/online-chat-messenger-stage1/udp_socket_file'
  chat_server = ChatServer(server_address)
  server_thread = threading.Thread(target=chat_server.start_server)
  server_thread.start()
