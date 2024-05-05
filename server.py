import socket
import os
from faker import Faker

class Server:
    def __init__(self, server_address) -> None:
        # 引数として受け取ったサーバーアドレスを代入
        self.server_address: str = server_address
        # ソケットを定義
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        # fakerを定義
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
        # デコードされた受信データを取得
        data_str: str = self.decode_data(data)

        # 受信したデータのバイト数とクライアントアドレスを表示
        print('\nクライアントアドレス {} から {} バイトのメッセージが送信されました'.format(client_address, len(data)))
        print('クライアント : {}'.format(data_str))

    # クライアントに送信したデータを表示するメソッド
    def display_sent_data(self, data : str) -> None:
        print('\nクライアントに偽アドレス「{}」を送信しました'.format(data))

    # クライアントにデータを送信するメソッド
    def sent_data(self, client_address) -> None:
        # 偽アドレスを取得
        fake_address: str = self.get_fake_address()
        # 偽アドレスをエンコードしたものを取得
        fake_address_bytes : bytes = self.encode_data(fake_address)
        # クライアントに偽アドレスを返す
        self.sock.sendto(fake_address_bytes, client_address)

        self.display_sent_data(fake_address)

    # クライアントからのデータを受信するメソッド
    def receive_data(self) -> None:
        # データの受信を永遠に待ち続ける
        while True:
            print('\nクライアントからのメッセージを待ちます')

            # ソケットからのデータを受信
            # 一度に4096バイトまで受信
            # client_addressの型がわからない
            data, client_address = self.sock.recvfrom(4096)
            # 受信したデータをターミナルに表示
            self.display_receive_data(data, client_address)

            self.sent_data(client_address)

    # サーバーを起動するメソッド
    def start_server(self) -> None:
        self.remove_file_if_exists()

        # ソケットが起動したことを表示
        print('\nサーバーアドレス {} でソケットが起動しました'.format(self.server_address))

        # 上記で定義したサーバーアドレスをソケットに紐づける
        self.sock.bind(self.server_address)

        self.receive_data()


def main():
    # serverのアドレスを定義
    server_address: str = '127.0.0.1'

    # サーバーを作成
    server: Server = Server(server_address)

    # サーバーを起動する
    server.start_server()

main()

# 用語解説

# ソケット : 電話の受話器のようなもの。ソケットを使用することで、ネットワークの通信のためのプログラムを一から書かなくてもよくなる。
# TCP/UDP : ネットワーク通信のためのプロトコル(約束事、規約)
# エンコード : 
# デコード
