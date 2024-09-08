#include <iostream>
#include <string>
#include <ctime>
#include <windows.h>
#include <tchar.h>
#include <sstream>

// Define the functions from LockSDK.dll
extern "C" {
    __declspec(dllimport) int TP_Configuration(short lockType);
    __declspec(dllimport) int TP_MakeGuestCard(char* card_snr, const char* room_no, const char* checkin_time, const char* checkout_time, short iflags);
    __declspec(dllimport) int TP_ReadGuestCard(char* card_snr, char* room_no, char* checkin_time, char* checkout_time);
    __declspec(dllimport) int TP_CancelCard(char* card_snr);
    __declspec(dllimport) int TP_GetCardSnr(char* card_snr);
}

// Helper function to get the current time in "YYYY-MM-DD HH:MM:SS" format
std::string getCurrentTime() {
    time_t now = time(0);
    tm* ltm = localtime(&now);
    char buf[20];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", ltm);
    return std::string(buf);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Please provide method and parameters.\n";
        return 1;
    }

    std::string method = argv[1];

    if (method == "configure") {
        if (argc != 3) {
            std::cout << "Usage: configure <lockType>\n";
            return 1;
        }
        short lockType = std::stoi(argv[2]);
        int result = TP_Configuration(lockType);
        std::cout << "Configuration result: " << result << "\n";
    }
    else if (method == "makeguestcard") {
        if (argc != 4) {
            std::cout << "Usage: makeguestcard <room_no> <checkout_time> <flags>\n";
            return 1;
        }

        char card_snr[20] = { 0 };
        std::string room_no = argv[2];
        std::string checkout_time = argv[3];
        short iflags = std::stoi(argv[4]);

        // Get current time as check-in time
        std::string checkin_time = getCurrentTime();

        int result = TP_MakeGuestCard(card_snr, room_no.c_str(), checkin_time.c_str(), checkout_time.c_str(), iflags);
        std::cout << "Make Guest Card result: " << result << ", Card SNR: " << card_snr << "\n";
    }
    else if (method == "readguestcard") {
        char card_snr[20] = { 0 };
        char room_no[20] = { 0 };
        char checkin_time[30] = { 0 };
        char checkout_time[30] = { 0 };

        int result = TP_ReadGuestCard(card_snr, room_no, checkin_time, checkout_time);
        std::cout << "Read Guest Card result: " << result << "\n";
        if (result == 1) {
            std::cout << "Card SNR: " << card_snr << "\nRoom: " << room_no << "\nCheck-in: " << checkin_time << "\nCheck-out: " << checkout_time << "\n";
        }
    }
    else if (method == "cancelcard") {
        char card_snr[20] = { 0 };
        int result = TP_CancelCard(card_snr);
        std::cout << "Cancel Card result: " << result << "\n";
    }
    else if (method == "getcardsnr") {
        char card_snr[20] = { 0 };
        int result = TP_GetCardSnr(card_snr);
        std::cout << "Get Card SNR result: " << result << ", Card SNR: " << card_snr << "\n";
    }
    else {
        std::cout << "Unknown method.\n";
    }

    return 0;
}
