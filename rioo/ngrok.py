import subprocess


def start_ngrok():
    try:
        # Start ngrok without opening a window
        subprocess.Popen(['ngrok.exe', 'http','--domain=equipped-escargot-brightly.ngrok-free.app' , '80'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE, 
                                        creationflags=subprocess.CREATE_NO_WINDOW)
    except: 
        print("Error starting Ngrok")
    return