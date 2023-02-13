import tkinter as tk

# Set up the GUI with a toggle switch button
app = tk.Tk()
app.title("ESL Email Helper")

running = False

def toggle_service():
    global running
    if running:
        stop_service()
    else:
        start_service()

def start_service():
    global running
    running = True
    handle_incoming_emails()

def stop_service():
    global running
    running = False

toggle_button = tk.Button(text="Start/Stop Service", command=toggle_service)
toggle_button.pack()

app.mainloop()
