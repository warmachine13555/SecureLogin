import socket
import threading
import tkinter as tk

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(("81.169.141.81", 8888))
client.connect(("localhost", 7777))

root = tk.Tk()

message_label = tk.Label(root, text="Server message:")
message_label.pack()

message_entry = tk.Entry(root)
message_entry.pack()

def send_message(event=None):
    message = message_entry.get()
    client.send(message.encode())
    message_entry.delete(0, tk.END)  # Clear the input field

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

message_entry.bind("<Return>", send_message)  # Bind Enter key to send_message function

def receive_messages():
    while True:
        message = client.recv(1024).decode()
        message_label.config(text=message)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()
