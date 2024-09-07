import ctypes
from ctypes import c_char_p, c_int, c_short, create_string_buffer
import os

class RIOO:
    """
    RIOO class to interface with the LockSDK.dll. Provides methods to configure the lock,
    create, read, and cancel guest cards, and retrieve card serial numbers.

    Requires the following functions from the DLL:
        - TP_Configuration
        - TP_MakeGuestCard
        - TP_ReadGuestCard
        - TP_CancelCard
        - TP_GetCardSnr
    """

    def __init__(self, dll_path):
        """
        Initializes the RIOO class by loading the LockSDK.dll.

        :param dll_path: Path to the LockSDK.dll file. Default is 'LockSDK.dll'.
        """
        self.dll = ctypes.CDLL(dll_path)

        # Define function signatures for each function we will use from the DLL
        self.dll.TP_Configuration.argtypes = [c_short]
        self.dll.TP_Configuration.restype = c_int

        self.dll.TP_MakeGuestCard.argtypes = [ctypes.POINTER(ctypes.c_char), c_char_p, c_char_p, c_char_p, c_short]
        self.dll.TP_MakeGuestCard.restype = c_int

        self.dll.TP_ReadGuestCard.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char)]
        self.dll.TP_ReadGuestCard.restype = c_int

        self.dll.TP_CancelCard.argtypes = [ctypes.POINTER(ctypes.c_char)]
        self.dll.TP_CancelCard.restype = c_int

        self.dll.TP_GetCardSnr.argtypes = [ctypes.POINTER(ctypes.c_char)]
        self.dll.TP_GetCardSnr.restype = c_int

    def configure_lock(self, lock_type: int) -> int:
        """
        Configures the lock type.

        :param lock_type: Type of the lock (e.g., 5 for RF50 card & 4 for RF57).
        :return: Result code (1 for success, negative for error).
        """
        result = self.dll.TP_Configuration(c_short(lock_type))
        self._check_error(result)
        return result

    def make_guest_card(self, room_no: str, checkin_time: str, checkout_time: str, flags: int = 0) -> int:
        """
        Creates a guest card with the provided room number, check-in, and check-out times.

        :param room_no: Room number as a string (e.g., '001.002.00028') ---   001.005.00503 --> 1st building 5th floor Room No.503.
        :param checkin_time: Check-in time as a string in 'YYYY-MM-DD HH:MM:SS' format.
        :param checkout_time: Check-out time as a string in 'YYYY-MM-DD HH:MM:SS' format.
        :param flags: Guest card options (default is 0).
        :return: Result code (1 for success, negative for error).
        """
        card_snr = self.get_card_snr()
        result = self.dll.TP_MakeGuestCard(card_snr.encode(), room_no.encode(), checkin_time.encode(), checkout_time.encode(), c_short(flags))
        self._check_error(result)
        return result

    def read_guest_card(self) -> str:
        """
        Reads the information of the currently scanned guest card.

        :return: Card details in a formatted string.
        """
        card_snr = create_string_buffer(20)
        room_no = create_string_buffer(20)
        checkin_time = create_string_buffer(30)
        checkout_time = create_string_buffer(30)

        result = self.dll.TP_ReadGuestCard(card_snr, room_no, checkin_time, checkout_time)
        if result == 1:
            return (f"Card Serial Number: {card_snr.value.decode()}\n"
                    f"Room Number: {room_no.value.decode()}\n"
                    f"Check-in Time: {checkin_time.value.decode()}\n"
                    f"Check-out Time: {checkout_time.value.decode()}")
        else:
            self._check_error(result)
        return ""

    def cancel_card(self) -> int:
        """
        Cancels the guest card (returns it).

        :return: Result code (1 for success, negative for error).
        """
        card_snr = create_string_buffer(20)
        result = self.dll.TP_CancelCard(card_snr)
        self._check_error(result)
        return result

    def get_card_snr(self) -> str:
        """
        Retrieves the card's serial number.

        :return: The card's serial number as a string.
        """
        card_snr = create_string_buffer(20)
        result = self.dll.TP_GetCardSnr(card_snr)
        if result == 1:
            print(f"Card Serial Number: {card_snr.value.decode()}")
            return card_snr.value.decode()
        else:
            self._check_error(result)
        return ""

def _check_error(self, code: int):
    """
    Checks for errors in DLL function calls and raises exceptions if necessary.

    :param code: The result code from the DLL function.
    """
    if code < 1:  # OPR_OK (1) is the only success case, others are errors
        errors = {
            -1: "No card detected",
            -2: "No encoder detected",
            -3: "Invalid card",
            -4: "Card type error",
            -5: "Reading or writing error",
            -6: "Port not open",
            -7: "End of data card",
            -8: "Invalid parameter",
            -9: "Invalid operation",
            -10: "Other error",
            -11: "Port is in use",
            -12: "Communication error",
            -20: "Customer code error",
            -29: "Unregistered error",
            -30: "No Authorization Card data",
            -31: "Room number exceeds available card subarea"
        }
        error_message = errors.get(code, f"Unknown error: {code}")
        raise Exception(f"Error Code {code}: {error_message}")


if __name__ == "__main__":
    # Example usage of the RIOO class
    current_dir = os.path.dirname(os.path.realpath(__file__))
    sdk_path = current_dir + "\libs\LockSDK.dll"
    rioo = RIOO(sdk_path)

    # Configuring the lock
    try:
        print("Configuring lock...")
        result = rioo.configure_lock(5)  # 5 is for "RF50 Card"
        if result == 1:
            print("Lock configured successfully.")
    except Exception as e:
        print(f"Error: {e}")

    # Reading a guest card
    try:
        print("Reading guest card...")
        card_details = rioo.read_guest_card()
        print(card_details)
    except Exception as e:
        print(f"Error: {e}")

    # Making a guest card
    try:
        print("Making guest card...")
        result = rioo.make_guest_card("001.002.00028", "2024-09-01 12:00:00", "2024-09-15 12:00:00", 0)
        if result == 1:
            print("Guest card created successfully.")
    except Exception as e:
        print(f"Error: {e}")

    # Reading a guest card
    try:
        print("Reading guest card...")
        card_details = rioo.read_guest_card()
        print(card_details)
    except Exception as e:
        print(f"Error: {e}")

    # # Canceling a guest card
    # try:
    #     print("Canceling guest card...")
    #     result = rioo.cancel_card()
    #     if result == 1:
    #         print("Guest card canceled successfully.")
    # except Exception as e:
    #     print(f"Error: {e}")

    # # Retrieving the card serial number
    # try:
    #     print("Getting card serial number...")
    #     card_snr = rioo.get_card_snr()
    #     print(card_snr)
    # except Exception as e:
    #     print(f"Error: {e}")
