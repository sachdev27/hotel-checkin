from datetime import datetime, timedelta
import os
import subprocess

class LockSDKManager:
    """
    Class to manage all interactions with the C# executable for LockSDK operations.
    It wraps all SDK functions like card creation, configuration, reading, cancellation, etc.
    """

    def __init__(self, executable_path):
        """
        Initialize the class with the path to the C# executable.

        :param executable_path: The path to the C# executable (LockSDKWrapper.exe)
        """
        self.executable_path = executable_path

    def _run_command(self, command):
        """
        Runs a command with subprocess and returns the output.

        :param command: List of command arguments to pass to subprocess.
        :return: The output of the subprocess call.
        """
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
                return None
            return result.stdout
        except Exception as e:
            print(f"An error occurred while running the command: {e}")
            return None

    def configure_lock(self, lock_type):
        """
        Configures the lock type.

        :param lock_type: The type of lock (e.g., 5 for RF50 card).
        :return: The result of the configuration.
        """
        print(f"Configuring lock with lock type: {lock_type}")
        command = [self.executable_path, 'configure', str(lock_type)]
        return self._run_command(command)

    def make_guest_card(self, room_no, checkin_time, checkout_time, flags=0):
        """
        Creates a guest card.

        :param room_no: Room number (e.g., "001.002.00028").
        :param checkin_time: Check-in time in 'YYYY-MM-DD HH:MM:SS' format.
        :param checkout_time: Check-out time in 'YYYY-MM-DD HH:MM:SS' format.
        :param flags: Card options (default is 0).
        :return: The result of the guest card creation.
        """
        print(f"Creating guest card for room: {room_no}")
        command = [self.executable_path, 'makeguestcard', room_no, checkin_time, checkout_time, str(flags)]
        return self._run_command(command)

    def read_guest_card(self):
        """
        Reads the details of a guest card.
        :return: The details of the guest card.
        """
        print("Reading guest card details...")
        command = [self.executable_path, 'readguestcard']
        return self._run_command(command)

    def cancel_guest_card(self):
        """
        Cancels the guest card.

        :return: The result of the cancellation.
        """
        print("Cancelling guest card...")
        command = [self.executable_path, 'cancelcard']
        return self._run_command(command)

    def get_card_serial_number(self):
        """
        Retrieves the serial number of a card.

        :return: The serial number of the card.
        """
        print("Retrieving card serial number...")
        command = [self.executable_path, 'getcardsnr']
        return self._run_command(command)



# Example usage
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    sdk_path = current_dir + "\exe\LockSDKWrapper.exe"
    sdk_manager = LockSDKManager(sdk_path)

    # Example: Configure lock
    result = sdk_manager.configure_lock(5)  # RF50 card
    if result:
        print(result)

    # ----------------------------------------------------------------------------
    # Example: Make guest card
    
    # Get current time for check-in
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Set check-out time to 2 days from now
    # Set checkout time to next day 12:05 PM
    tomorrow = datetime.now() + timedelta(days=1)
    checkout_time = tomorrow.replace(hour=12, minute=5, second=0).strftime("%Y-%m-%d %H:%M:%S")
    print(current_time,checkout_time)
    
    result = sdk_manager.make_guest_card("001.002.00028", checkin_time=current_time, checkout_time=checkout_time)
    if result:
        print(result)

    # # Example: Read guest card
    # result = sdk_manager.read_guest_card()
    # if result:
    #     print(result)

    # # Example: Cancel guest card
    # result = sdk_manager.cancel_guest_card()
    # if result:
    #     print(result)

    # # Example: Get card serial number
    # result = sdk_manager.get_card_serial_number()
    # if result:
    #     print(result)
