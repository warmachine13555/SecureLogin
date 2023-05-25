import socket
import threading
import tkinter as tk

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(("81.169.141.81", 8888))
client.connect(("localhost", 7777))

root = tk.Tk()
root.geometry("400x300")  # Set the initial window size to 400x300 pixels
root.resizable(True, True)  # Allow both width and height resizing
root.title("OnlineBanking")  # Set the window title to "OnlineBanking"

frame = tk.Frame(root)
frame.pack(pady=50)  # Add padding at the top

message_label = tk.Label(frame)
message_label.pack()

message_entry = tk.Entry(root)
message_entry.pack(anchor='center')  # Align the text input field to the center

def send_message(event=None):
    message = message_entry.get()
    client.send(message.encode())
    message_entry.delete(0, tk.END)  # Clear the input field

message_entry.bind("<Return>", send_message)  # Bind Enter key to send_message function

message_queue = []  # New variable to store received messages

def receive_messages():
    while True:
        message = client.recv(1024).decode()
        message_queue.append(message)  # Store received messages

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

def update_message_label():
    if message_queue:
        message_label.config(text=message_queue.pop(0))  # Display the next message

    root.after(100, update_message_label)  # Schedule the update every 100ms

root.after(100, update_message_label)  # Start the update process

root.mainloop()
