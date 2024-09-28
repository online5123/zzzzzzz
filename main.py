import socket
import threading
import tkinter as tk


class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("채팅 클라이언트")

        self.chat_box = tk.Text(master, state='disabled')
        self.chat_box.pack(padx=10, pady=10)

        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 5555))

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = self.entry.get()
        self.client_socket.send(message.encode('utf-8'))
        self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_box.config(state='normal')
                    self.chat_box.insert(tk.END, message + '\n')
                    self.chat_box.config(state='disabled')
                    self.chat_box.yview(tk.END)
            except:
                print("서버와의 연결이 끊어졌습니다.")
                break


if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
