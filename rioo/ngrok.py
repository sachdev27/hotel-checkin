import subprocess


def start_ngrok():
    try:
        # Start ngrok without opening a window
        subprocess.Popen(['ngrok.exe', 'http','--domain=<Domain>' , '80'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE, 
                                        creationflags=subprocess.CREATE_NO_WINDOW)
    except: 
        print("Error starting Ngrok")
    return
