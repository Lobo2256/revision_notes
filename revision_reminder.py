import smtplib
from email.mime.text import MIMEText
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Email configuration
SENDER_EMAIL = "49166@farnborough.ac.uk"
SENDER_PASSWORD = "fhle viaq zsea xoik"
RECEIVER_EMAIL = "49166@farnborough.ac.uk"  

# Reads lines from notes.txt, removing empty lines and extra spaces
def load_notes():
    notes = []
    with open("notes.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip() # removes empty spaces and new lines
            if line != "":
                notes.append(line)
    return notes

    

# Send email with a single note
def send_email(note):
    msg = MIMEText(note)
    msg["Subject"] = "Your Revision Reminder"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"Sent: {note}")
    except Exception as e:
        print("Email failed:", e) # Print error if sending fails


# Starts sending notes one by one every hour
def start_sending():
    global running
    if running:
        return  # Prevents starting multiple loops

    running = True
    notes = load_notes()  # Get all revision notes from file

    def run():
        index = 0
        while running and index < len(notes):   # Loop through notes while "running"
            send_email(notes[index])            # Send current note
            index += 1                          # Move to next
            time.sleep(3600)                    # Wait 1 hour (3600 sec)

        if index >= len(notes):
            # Show message when all notes are sent
            messagebox.showinfo("Done", "All notes have been sent.")

    # Run the sending loop in the background (so GUI doesn't freeze)
    threading.Thread(target=run, daemon=True).start()
    status_label.config(text="Status: Running")  # Update GUI

# Stop sending emails
def stop_sending():
    global running
    running = False
    status_label.config(text="Status: Stopped")

# Set up GUI
running = False
root = tk.Tk()
root.title("Revision Reminder App")

tk.Label(root, text="Revision Reminder App", font=("Arial", 16)).pack(pady=10)

start_btn = tk.Button(root, text="Start Sending", command=start_sending)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop", command=stop_sending)
stop_btn.pack(pady=5)

status_label = tk.Label(root, text="Status: Stopped", fg="blue")
status_label.pack(pady=10)



root.mainloop()
