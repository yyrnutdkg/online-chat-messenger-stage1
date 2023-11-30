import os
import socket
import threading
import time


class ChatClient:
  def __init__(self, server_address, client_address):
    self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    self.server_address = server_address
    self.client_address = client_address
    self.stop_receive_thread_flag = threading.Event()
    self.user_name = input('Please enter your username : ')

  def send_message(self, message):
    encoded_message = f"{len(self.user_name)}:{message}".encode('utf-8')
    print('Send message: {}'.format(encoded_message))
    self.sock.sendto(encoded_message, self.server_address)

  def check_received_message(self):
    while not self.stop_receive_thread_flag.is_set():
      print('Check message...')

      data, server = self.sock.recvfrom(4096)

      if data:
        received_message = data.decode('utf-8')
        print('Received: {}'.format(received_message))

  def start_chat(self):
    print('Chat start...')
    self.sock.bind(self.client_address)
    check_received_message_thread = threading.Thread(target=self.check_received_message)
    check_received_message_thread.start()

    try:
      message = input('Please enter a message : ')
      self.send_message(message)
      time.sleep(10)

    finally:
      self.close()


  def close(self):
    print('Closing socket...')
    self.stop_receive_thread_flag.set()
    self.sock.close()

    try:
      os.unlink(self.client_address)
    except FileNotFoundError:
      pass

if __name__ == "__main__":
  server_address = '/home/vagrant/work/online-chat-messenger-stage1/udp_socket_file'
  client_address = '/home/vagrant/work/online-chat-messenger-stage1/udp_client_socket_file'

  client_chat = ChatClient(server_address, client_address)
  client_chat.start_chat()
