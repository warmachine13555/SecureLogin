import socket
import threading
import tkinter as tk

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(("81.169.141.81", 8888))
client.connect(("localhost", 7777))

root = tk.Tk()
root.geometry("400x300")
root.resizable(True, True)
root.title("OnlineBanking")

frame = tk.Frame(root)
frame.pack(pady=50)

message_label = tk.Label(frame)
message_label.pack()

message_entry = tk.Entry(root)
message_entry.pack(anchor='center')

def send_message(event=None):
    message = message_entry.get()
    client.send(message.encode())
    message_entry.delete(0, tk.END)

message_entry.bind("<Return>", send_message)

message_queue = []

def receive_messages():
    while True:
        message = client.recv(1024).decode()
        message_queue.append(message)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

def update_message_label():
    if message_queue:
        message_label.config(text=message_queue.pop(0))

    root.after(100, update_message_label)

root.after(100, update_message_label)

root.mainloop()
