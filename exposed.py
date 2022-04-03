import numpy as np
import eel

#JS Exposed Functions
def send_data_js(name,value):
    eel.store_result(name,value)

def request_data_js(name):
    eel.send_data_py(name)

#Own Exposed Functions
@eel.expose
def send_message_py(msg):
    print(str(msg))

@eel.expose
def receive_data_py(data):
    return data
