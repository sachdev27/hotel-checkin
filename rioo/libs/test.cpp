#include <iostream>
#include <cstring>
#include "LockSDK.h" // Include the LockSDK header file

// Error handling function to map error codes to messages
void HandleError(int code, const std::string& operation) {
    if (code == OPR_OK) {
        std::cout << operation << " was successful." << std::endl;
        return;
    }

    std::string errorMessage;
    switch (code) {
    case NO_CARD: errorMessage = "Error: No card detected"; break;
    case NO_RW_MACHINE: errorMessage = "Error: No encoder detected"; break;
    case INVALID_CARD: errorMessage = "Error: Invalid card"; break;
    case CARD_TYPE_ERROR: errorMessage = "Error: Card type error"; break;
    case RDWR_ERROR: errorMessage = "Error: Reading or writing error"; break;
    case PORT_NOT_OPEN: errorMessage = "Error: Port not open"; break;
    case END_OF_DATA_CARD: errorMessage = "Error: End of data card"; break;
    case INVALID_PARAMETER: errorMessage = "Error: Invalid parameter"; break;
    case INVALID_OPR: errorMessage = "Error: Invalid operation"; break;
    case OTHER_ERROR: errorMessage = "Error: Other error"; break;
    case PORT_IN_USED: errorMessage = "Error: Port is in use"; break;
    case COMM_ERROR: errorMessage = "Error: Communication error"; break;
    case ERR_CLIENT: errorMessage = "Error: Customer code error"; break;
    case ERR_NOT_REGISTERED: errorMessage = "Error: Unregistered"; break;
    case ERR_NO_CLIENT_DATA: errorMessage = "Error: No Authorization Card data"; break;
    case ERR_ROOMS_CNT_OVER: errorMessage = "Error: Room number exceeds available card subarea"; break;
    default: errorMessage = "Error: Unknown error code (" + std::to_string(code) + ")";
    }

    std::cout << operation << " failed: " << errorMessage << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc == 1) {
        std::cout << "Please provide a method and parameters." << std::endl;
        return 1;
    }

    std::string method = argv[1];

    if (method == "configure") {
        if (argc != 3) {
            std::cout << "Usage: configure <lockType>" << std::endl;
            return 1;
        }
        int lockType = std::stoi(argv[2]);
        int result = TP_Configuration(lockType);
        HandleError(result, "Lock Configuration");
    }
    else if (method == "makeguestcard") {
        if (argc != 6) {
            std::cout << "Usage: makeguestcard <room_no> <checkin_time> <checkout_time> <flags>" << std::endl;
            return 1;
        }

        char card_snr[20] = { 0 };
        char* room_no = argv[2];
        char* checkin_time = argv[3];
        char* checkout_time = argv[4];
        int iflags = std::stoi(argv[5]);

        int result = TP_MakeGuestCard(card_snr, room_no, checkin_time, checkout_time, iflags);
        HandleError(result, "Make Guest Card");
        if (result == OPR_OK) {
            std::cout << "Guest Card Created Successfully! Card SNR: " << card_snr << std::endl;
        }
    }
    else if (method == "readguestcard") {
        char card_snr[20] = { 0 };
        char room_no[20] = { 0 };
        char checkin_time[30] = { 0 };
        char checkout_time[30] = { 0 };

        int result = TP_ReadGuestCard(card_snr, room_no, checkin_time, checkout_time);
        HandleError(result, "Read Guest Card");
        if (result == OPR_OK) {
            std::cout << "Card SNR: " << card_snr << "\nRoom: " << room_no
                << "\nCheck-in: " << checkin_time << "\nCheck-out: " << checkout_time << std::endl;
        }
    }
    else if (method == "cancelcard") {
        char card_snr[20] = { 0 };

        int result = TP_CancelCard(card_snr);
        HandleError(result, "Cancel Guest Card");
        if (result == OPR_OK) {
            std::cout << "Guest card cancelled successfully." << std::endl;
        }
    }
    else if (method == "getcardsnr") {
        char card_snr[20] = { 0 };

        int result = TP_GetCardSnr(card_snr);
        HandleError(result, "Get Card SNR");
        if (result == OPR_OK) {
            std::cout << "Card Serial Number: " << card_snr << std::endl;
        }
    }
    else {
        std::cout << "Unknown method." << std::endl;
    }

    return 0;
}
