import tkinter as tk
from tkinter import colorchooser
import socket
import threading

# 클라이언트 설정
HOST = '192.168.219.108'  # 서버 IP 주소를 입력 (테스트 시 localhost)
PORT = 12345  # 서버와 동일한 포트 사용


# 메시지 수신 스레드
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, message + "\n")
            chat_window.config(state=tk.DISABLED)
            chat_window.see(tk.END)
        except:
            print("An error occurred!")
            client_socket.close()
            break


# 메시지 전송 함수
def send_message():
    message = f"{nickname}: {message_entry.get()}"
    client_socket.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)


# 닉네임 색상 선택
def choose_color():
    global nickname_color
    nickname_color = colorchooser.askcolor(title="Choose your nickname color")[1]
    nickname_label.config(fg=nickname_color)


# GUI 설정
def start_chat():
    global nickname
    nickname = nickname_entry.get()

    if nickname:
        login_window.destroy()

        global chat_window, message_entry

        chat_window = tk.Text(root, width=50, height=20, state=tk.DISABLED)
        chat_window.pack(padx=10, pady=10)

        message_entry = tk.Entry(root, width=40)
        message_entry.pack(side=tk.LEFT, padx=10, pady=10)

        send_button = tk.Button(root, text="Send", command=send_message)
        send_button.pack(side=tk.LEFT, padx=10)

        # 메시지 수신 스레드 시작
        threading.Thread(target=receive_messages).start()


# 클라이언트 GUI 창
root = tk.Tk()
root.title("Chat Application")

# 서버 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 로그인 창
login_window = tk.Toplevel(root)
login_window.title("Login")

nickname_label = tk.Label(login_window, text="Enter your nickname:")
nickname_label.pack(pady=5)

nickname_entry = tk.Entry(login_window, width=30)
nickname_entry.pack(pady=5)

color_button = tk.Button(login_window, text="Choose Color", command=choose_color)
color_button.pack(pady=5)

login_button = tk.Button(login_window, text="Join Chat", command=start_chat)
login_button.pack(pady=10)

root.mainloop()
