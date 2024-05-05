import socket
import os
from faker import Faker

class Server:
    def __init__(self, server_address) -> None:
        self.server_address: str = server_address
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.fake: Faker = Faker('jp-JP')

    # 同じサーバーアドレスのファイルがある場合に削除するメソッド
    def remove_file_if_exists(self) -> None:
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass

    # 偽アドレスを返すメソッド
    def get_fake_address(self) -> str:
        return self.fake.address()
    
    # エンコードされたデータを返すメソッド
    def encode_data(self, data: str) -> bytes:
        return data.encode('utf-8')
    
    # デコードされたデータを返すメソッド
    def decode_data(self, data : bytes) -> str:
        return data.decode('utf-8')
    
    # ターミナルに受信データを表示するメソッド
    def display_receive_data(self, data : bytes, client_address) -> None:
        data_str: str = self.decode_data(data)

        print('\nクライアントアドレス {} から {} バイトのメッセージが送信されました'.format(client_address, len(data)))
        print('クライアント : {}'.format(data_str))

    # クライアントに送信したデータを表示するメソッド
    def display_sent_data(self, data : str) -> None:
        print('\nクライアントに偽アドレス「{}」を送信しました'.format(data))

    # クライアントにデータを送信するメソッド
    def sent_data(self, client_address) -> None:
        fake_address: str = self.get_fake_address()
        fake_address_bytes : bytes = self.encode_data(fake_address)

        try:
            self.sock.sendto(fake_address_bytes, client_address)
            self.display_sent_data(fake_address)
        except Exception as e:
            print("エラーが発生しました : ", e)

    # クライアントからのデータを受信するメソッド
    def receive_data(self) -> None:
        while True:
            print('\nクライアントからのメッセージを待ちます')

            data, client_address = self.sock.recvfrom(4096)

            self.display_receive_data(data, client_address)
            self.sent_data(client_address)

    # サーバーを起動するメソッド
    def start_server(self) -> None:
        self.remove_file_if_exists()

        print('\nサーバーアドレス {} でソケットが起動しました'.format(self.server_address))

        self.sock.bind(self.server_address)

        self.receive_data()


def main():
    server_address: str = '127.0.0.1'

    server: Server = Server(server_address)

    server.start_server()

main()