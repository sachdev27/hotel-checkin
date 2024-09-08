import subprocess
from datetime import datetime

def call_lock_sdk(method, *args):
    try:
        # Construct the command
        command = ['./LockSDKWrapper.exe', method] + list(args)

        # Call the executable with the arguments
        result = subprocess.run(command, capture_output=True, text=True)

        # Output the result
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage: configure the lock
    call_lock_sdk('configure', '5')  # 5 for RF50 lock type

    # Example usage: make a guest card with current check-in time
    checkout_time = "2024-09-15 12:00:00"

    call_lock_sdk('makeguestcard', '001.002.00028', checkout_time, '0')

    # Example usage: read a guest card
    call_lock_sdk('readguestcard')

    # Example usage: cancel a card
    call_lock_sdk('cancelcard')

    # Example usage: get card serial number
    call_lock_sdk('getcardsnr')
