#ifndef __LOCK_SDK_H__
#define __LOCK_SDK_H__
   

// Card Errors 
enum ERROR_TYPE
{
    OPR_OK              =   1,      // Operation successful
    NO_CARD			    =   -1,     // No card detected
    NO_RW_MACHINE	    =   -2,     // No card reader detected
    INVALID_CARD	    =   -3,     // Invalid card
    CARD_TYPE_ERROR	    =   -4,     // Card type error
    RDWR_ERROR		    =   -5,     // Read/write error
    PORT_NOT_OPEN	    =   -6,     // Port not open
    END_OF_DATA_CARD    =   -7,     // End of data card
    INVALID_PARAMETER   =   -8,     // Invalid parameter
    INVALID_OPR		    =   -9,     // Invalid operation
    OTHER_ERROR		    =   -10,    // Other error
    PORT_IN_USED	    =   -11,    // Port is in use
    COMM_ERROR		    =   -12,    // Communication error    
    ERR_CLIENT          =   -20,    // Client code error    
    ERR_NOT_REGISTERED  =   -29,    // Not registered
    ERR_NO_CLIENT_DATA  =   -30,    // No authorized card information
    ERR_ROOMS_CNT_OVER  =   -31,    // Room count exceeds available sectors
}; 


#ifdef __cplusplus
	extern "C" { 
#endif

/*=============================================================================
Function Name:                   TP_Configuration
;
Functionality: Initialize dynamic library configuration, completing door lock type selection/card reader connection
Input: lock_type -- Type of door lock (card type used): 4-RF57 door lock; 5-RF50 door lock
Output: None
Return value: Error type
=============================================================================*/
int __stdcall TP_Configuration(int lock_type);

/*=============================================================================
Function Name:                   TP_MakeGuestCard
;
Functionality: Create a guest card
Input: room_no         --  Room lock number:  String, e.g., "001.002.00003.A", "208", etc.
        checkin_time    --  Check-in time:  Date and time in string format "YYYY-MM-DD hh:mm:ss"
        checkout_time   --  Expected check-out time:  Date and time in string format "YYYY-MM-DD hh:mm:ss"
        iflags          --  Guest card options, generally set to 0. Explanations for various iflags values:
        		      8:  Indicates a duplicate card, does not override the previous card (multiple cards can be issued for one room)
        		      32: Indicates a one-time use card, invalid after one use
        		      128: Indicates checking card check-in time (if the card's check-in time is > current lock time, the card cannot open the door, not recommended)
        		      
        		      if iflags == 0, the previous card is invalidated upon swiping; it's not a one-time use card; check-in time is not verified
   	
Output: card_snr        -- Card number:  String, preallocate at least 20 bytes
Example 1: room_no="001.002.00003.A", checkin_time="2008-06-06 12:30:59", checkout_time="2008-06-07 12:00:00"
           iFlags=8  (Duplicate card)

Example 2: room_no="203", checkin_time="2008-06-06 12:30:59", checkout_time="2008-06-07 12:00:00"
           iFlags=0

Return value: Error type
Note: Room number must be entered as the door lock number!! Format depends on the lock management software. Please check the "Room Settings" interface of the lock management software. If the software does not have a lock number, enter the room number.
=============================================================================*/
int __stdcall TP_MakeGuestCard(char *card_snr, char *room_no, char *checkin_time,char *checkout_time, int iflags);

/*=============================================================================
Function Name:                   TP_ReadGuestCard
;
Functionality: Read guest card information
Input: None.
Output: card_snr        --  Card number:  String, preallocate at least 20 bytes
        room_no         --  Room number:  String, preallocate at least 20 bytes
        checkin_time    --  Check-in time:  Date and time in string format "YYYY-MM-DD hh:mm:ss", preallocate at least 30 bytes
        checkout_time   --  Expected check-out time:  Date and time in string format "YYYY-MM-DD hh:mm:ss", preallocate at least 30 bytes
Return value: Error type
=============================================================================*/
int __stdcall	TP_ReadGuestCard(char *card_snr, char *room_no, char *checkin_time, char *checkout_time);

/*=============================================================================
Function Name:                   TP_CancelCard
;
Functionality: Deactivate/cancel a card
Input: None
Output: card_snr    -- Card number: String, preallocate at least 20 bytes
Return value: Error type
=============================================================================*/
int __stdcall TP_CancelCard(char *card_snr);

/*=============================================================================
Function Name:                   TP_GetCardSnr
;
Functionality: Read the card number (unique serial number of the card)
Input: None
Output: card_snr    --  Card number: String, preallocate at least 20 bytes
Return value: Error type
=============================================================================*/
int __stdcall TP_GetCardSnr(char *card_snr);

/*=============================================================================
Function Name:                   TP_M1Active
Functionality: Activate the card (read card number)
Input: None
Output: card_snr -- Card number, 4 bytes (represented as 8 characters in string form)
Return value: Error type
Description: Card activation
=============================================================================*/
int __stdcall TP_M1Active(char *card_snr);

/*=============================================================================
Function Name:                   TP_M1AuthKey
Functionality: Verify card key
Input: keyA:    Key, six bytes, default card key is "ffffffffffff"
        sector_no: Sector number, 1~40
Return value: Error type
Description: Verify the key of the corresponding sector of the card; must verify before reading/writing
=============================================================================*/
int __stdcall TP_M1AuthKey(char *keyA, UINT sector_no);

/*=============================================================================
Function Name:                   TP_M1SetKeyA
Functionality: Modify Key A
Input: NewKeyA:   New Key A, six bytes, represented as a string (12 characters)
        sector_no: Sector number
Return value: Error type
Description: Modify card Key A. Must use AuthKey to verify the original key first. Call functions in the following sequence:
        TP_M1Active  →  TP_M1AuthKey  →  TP_M1SetKeyA
=============================================================================*/
int __stdcall TP_M1SetKeyA(char *newKeyA, UINT sector_no);

/*=============================================================================
Function Name:                   TP_M1WriteBlock
Functionality: Write data
Input: block_no: Block number (usually sector number * 4 + block number within the sector)
        data: 16-byte data to write, represented as a string (32 characters)
Return value: Error type
Description: Write data to a block. Must verify the key using TP_M1AuthKey first.
        For example, sector 9's writable block numbers include: 9*4, 9*4+1, 9*4+2, i.e., blocks 36, 37, 38. Follow function call order:
        TP_M1Active  →  TP_M1AuthKey  →  TP_M1WriteBlock
=============================================================================*/
int __stdcall TP_M1WriteBlock(UINT block_no, char *data);

/*=============================================================================
Function Name:                   TP_M1ReadBlock
Functionality: Read data
Input: block_no: Block number (usually sector number * 4 + block number within the sector)
Output: data: 16-byte data, represented as a string (32 characters)
Return value: Error type
Description: Read data from a block. Must verify the key using TP_M1AuthKey first. Follow function call order:
        TP_M1Active  →  TP_M1AuthKey  →  TP_M1ReadBlock
=============================================================================*/
int __stdcall TP_M1ReadBlock(UINT block_no, char *data);


#ifdef __cplusplus
   }
#endif

#endif              // __LOCK_SDK_H__
