import socket
import os

class Client:
    def __init__(self, server_address, client_address) -> None:
        # 引数として受け取ったサーバーアドレスを代入
        self.server_address: str = server_address
        # 引数として受け取ったクライアントアドレスを代入
        self.client_address: str = client_address
        # ソケットを定義
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    # 同じクライアントアドレスのファイルがある場合に削除するメソッド
    def remove_file_if_exists(self) -> None:
        try:
            os.unlink(self.client_address)
        except FileNotFoundError:
            pass
    
    # エンコードされたデータを返すメソッド
    def encode_data(self, data: str) -> bytes:
        return data.encode('utf-8')
    
    # デコードされたデータを返すメソッド
    def decode_data(self, data : bytes) -> str:
        return data.decode('utf-8')
    
    # ターミナルに受信データを表示するメソッド
    def display_receive_data(self, data : bytes, server_address) -> None:
        # デコードされた受信データを取得
        data_str: str = self.decode_data(data)

        # 受信したデータのバイト数とサーバーアドレスを表示
        print('\nサーバーアドレス {} から {} バイトのメッセージが送信されました'.format(server_address, len(data)))
        print('サーバー : {}'.format(data_str))

    def display_sent_data(self, data : str) -> None:
        print('\nサーバーにメッセージ「{}」を送信しました'.format(data))

    def sent_data(self) -> None:
        while True:
            # メッセージの入力を求める
            client_message: str = input("\nメッセージを入力してください : ")
            # メッセージをバイト列にエンコード
            client_message_bytes: bytes = self.encode_data(client_message)
            # サーバーにメッセージを送信
            self.sock.sendto(client_message_bytes, self.server_address)

            self.display_sent_data(client_message)

            self.receive_data()

    # サーバーからのデータを受信するメソッド
    def receive_data(self) -> None:
        print('\nサーバーからのメッセージを待ちます')

        # ソケットからのデータを受信
        # 一度に4096バイトまで受信
        # server_addressの型がわからない
        data, server_address = self.sock.recvfrom(4096)
        # 受信したデータをターミナルに表示
        self.display_receive_data(data, server_address)

    # クライアントを起動するメソッド
    def start_client(self) -> None:
        self.remove_file_if_exists()

        # ソケットが起動したことを表示
        print('\nクライアントアドレス {} でソケットが起動しました'.format(self.client_address))

        # 上記で定義したクライアントアドレスをソケットに紐づける
        self.sock.bind(self.client_address)

        self.sent_data()


def main():
    # サーバーのアドレスを定義
    server_address: str = '127.0.0.1'
    # クライアントのアドレスを定義
    client_address: str = '127.0.0.2'

    # クライアントを作成
    client: Client = Client(server_address, client_address)

    # クライアントを起動する
    client.start_client()

main()