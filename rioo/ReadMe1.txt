LockSDK    Smart Door Lock Management Software Developer's kit Instructions

To save your time, please read the following instructions carefully!!!!


��Important Notes

1. This interface supports the following development languages: C#��VC��Delphi7��Delphi2000��PB9.0��PB10��VB.net��VB6.0 etc (each language in one folder). Please choose the language demo you commonly use to test and develop. 

2. Interface file is "LockSDK.dll", which will call all kinds of underlying database. Connecting with "LockSDK.dll" will finish the connection. 


3. Please put the "LockSDK_Demo.exe" file into the release package. Then registration, reading Authorization Card etc operations will be processed automatically.

4. When testing, please choose one language folder and open, find out "LockSDK_Demo.exe", double click, choose "5-RF50 Card" lock type, click "SDK Config" to make card.

New card replaces the old card: The later check-in guest card makes the earlier guest card expired automatically. E.g. the check-in time 12:00 guest card could open the door, but after the check-in time 12:05 guest card swipe and open, the 12:00 can��t open anymore. Therefore, if you want to open one room with several guest cards, please make sure the check-in time is the same or set the later cards do not replace the former cads.

If you use several software to issue cards alternately (e.g Demo, Hotel Management System, Door Lock Management System), probable only the last guest card can open the locks. After detecting authorization card or timing card on the lock, the replaced former guest card activates once again. When you meet these problems, please check the time of guest card.

Deadbolt Open: Need to set the GUEST CARD CAN OPEN DB-LOCK function.

Check the check-in time: In order to avoid the door locks can��t be open, default is uncheck the check-in time. If initial this function, need to set the lock time frequently. Check-in time is forced to be current computer time when issued.

5.Lock number format: 1.2.8203; If it is a suite room, there will be a letter after the lock number, e.g.1.2.8203.A.Attention: In the old version of Dlock, lock number format is like 102 or 20105A, or A0203,etc. If there is no lock number, please type in. Further details refer to GHUST ROOM SETTING-ROOM INFORMATION.

6.Because the lock time is a little different from actual time, it is advisable to postpone the expected checkout time by 30mins. E.g. if expected checkout time is 12:00 tomorrow, it would be better to make it as 12:30.

7. Checkin time and checkout time format is 2012-01-01 12:30:00. Please make sure the computer date and time format same as this format and try to make card.   

8. The encoder has to be the one that can make cards successfully via the door lock software. Otherwise, even cards can be made successfully, the card may not be able to open the lock . Sometimes it is because Authorization Card information is wrong. In this case, you can exit the software, put Authorization Card on encoder, open software again, and Authorization Card information will be read automatically. 

9. If Guest Card made by the interface cannot open the lock, the problem can be found out by comparing with Guest Cards made by the door lock management software. When comparing, please pay attention to the difference of lock number and checkin time.

10.Card making records save in the ��cardRecord.ini��. Remark=new means new card, remark=copy means copy card; openBlock=1 means open DBlock,; checkEN=1 means check the check-in time; Single=1 means one time open lock; oldCopyMode =1 means eLock use the old way to copy card. Records can be read by the portable tools.

11. Lock Malfunction Prompt (read unlocking card, take it away and notice how many ��di�� it sounds)

1 di: wrong time
2 di: deadbolt extends
3 di: wrong building number, floor number, or lock number
4 di: card is canceled
5 di: wrong card password
6 di: wrong Authorization Card
7 di: Recovering Card hasn��t been read

��Returned Value Description

enum ERROR_TYPE
{
    OPR_OK              =    1,      // successful operation
    NO_CARD		=   -1,     // no card detected
    NO_RW_MACHINE	=   -2,     // no encoder detected
    INVALID_CARD	=   -3,     // invalid card
    CARD_TYPE_ERROR	=   -4,     // card type error
    RDWR_ERROR		=   -5,     // reading or writing error
    PORT_NOT_OPEN	=   -6,     // port is not open
    END_OF_DATA_CARD    =   -7,     // end of data card
    INVALID_PARAMETER   =   -8,     // invalid parameter
    INVALID_OPR		=   -9,     // invalid operation
    OTHER_ERROR		=   -10,    // other error
    PORT_IN_USED	=   -11,    // port is in use
    COMM_ERROR		=   -12,    // communication error    
    ERR_CLIENT          =   -20,    // customer code error    
    ERR_NOT_REGISTERED  =   -29,    // unregistered
    ERR_NO_CLIENT_DATA  =   -30,     // no Authorization Card data
    ERR_ROOMS_CNT_OVER  =   -31,    // Room number exceeds available card subarea 

��Interface function declaration
/*=============================================================================
Function name��                        TP_Configuration;
Function: Interface Initialization configuration, to choose lock type or encoder connection etc
Input: Lock_type��lock type (i.e. card type) 
Output: N/A
Returned valude: error type
=============================================================================*/
int __stdcall TP_Configuration(int lock_type);

��Interface function declaration
/*=============================================================================
Function name��                        TP_Configuration;
Function: Interface Initialization configuration, to choose lock type or encoder connection etc
Input: Lock_type��lock type (i.e. card type) 
Output: N/A
Returned valude: error type
=============================================================================*/
int __stdcall TP_Configuration(int lock_type);


/*=============================================================================
Function name��                        TP_MakeGuestCard;
Function: to make Guest Card
Input:   room_no         --  room number: character string, i.e. "1.2.8102" etc
        checkin_time    --  checkin time: year-month-day-minute-second character string "YYYY-MM-DD hh:mm:ss"
        checkout_time   -- checkout time: year-month-day-minute-second character string "YYYY-MM-DD hh:mm:ss"
        iflags          --  Guest Card options, refer to Defines>>> GUEST_FLAGS, normally set as 0
                            1: can open deadbolt
                            8: copy Guest Card, cannot block previous Guest Card (several Guest Cards open one room)
                            32: Guest Card opens the lock one time only, will be invalid after unlocking
                            128: check Checkin time ( if checkin time  > lock time, lock cannot be opened)
                            The above values can be combined for different demands.
                            If iflags ==0, new Guest Card blocks Guest Cards made previously; it is not one time Guest Card; Doesnt detect checkin time
Output: card_snr        -- card number: character string, at least pre-distribute 20 bytes 
Example 1: room_no="001.002.00003.A", SDateTime="2008-06-06 12:30:59", EDateTime="2008-06-07 12:00:00"
        iFlags=0

Example 2: room_no="203", SDateTime="2008-06-06 12:30:59", EDateTime="2008-06-07 12:00:00"
        iFlags=0
Returned valude: error type
Remark: door lock needs to be input room number. Please refer to ��Room information�� in door lock management software for more setting details. 
=============================================================================*/
int __stdcall TP_MakeGuestCard(char *card_snr, char *room_no, char *checkin_time,char *checkout_time, int iflags);



/*=============================================================================
Function name:                        TP_ReadGuestCard;
Function: to read Guest Card information
Input: N/A
Output: card_snr        --  card number:       character string, at least pre-distribute 20 bytes
        room_no         --  lock number:     character string, at least pre-distribute 20 bytes
        checkin_time    --  checkin time:  year-month-day-minute-second character string "YYYY-MM-DD hh:mm:ss", at least pre-distribute 30 bytes
        checkout_time   --  checkout time:  year-month-day-minute-second character string "YYYY-MM-DD hh:mm:ss", at least pre-distribute 30 bytes
Returned valude: error type
=============================================================================*/
int __stdcall	TP_ReadGuestCard(char *card_snr,char *room_no, char *checkin_time, char *checkout_time);


/*=============================================================================
Function name:                        TP_CancelCard;
Function: to return card
Input: N/A
Output:
Output: card_snr �Ccard number: character string, at least pre-distribute 20 bytes
Returned valude: error type
=============================================================================*/
int __stdcall TP_CancelCard(char *card_snr);

/*=============================================================================
Function name:                         TP_GetCardSnr;
Function: to read card number (the individual serial number of the card)
Input: N/A
Output: card_snr �Ccard number: character string, at least pre-distribute 20 bytes
Returned valude: error type
=============================================================================*/
int __stdcall TP_GetCardSnr(char *card_snr);




////////////////////// The following functions are to manage membership cards of the hotel ///////////////////////
/*=============================================================================
Function name:                           TP_M1Active 
Function: to activate card (read card number)
Input: N/A
Output: card_snr �Ccard number, 4 bytes (8 character strings)
Returned valude: error type
Description: card activation
=============================================================================*/
int __stdcall TP_M1Active(char *card_snr);

/*=============================================================================
Function name:                 TP_M1AuthKey
Function: to verify card encryption code
Parameter: keyA:	  encryption code, 6 bytes, card default encryption code is "ffffffffffff"
		sector_no: subarea no., 1~40 
Returned valude: error type
Description: verify encryption code of the relative card subarea. Card can be written after verification.
=============================================================================*/
int __stdcall TP_M1AuthKey(char *keyA, UINT sector_no);

/*=============================================================================
Function name:                TP_M1SetKeyA
Function: to change card encryption code A 
Parameter: NewKeyA:	NewKeyA, 6 bytes, 12 charaters
		sector_no:	subarea no.
Returned valude: error type
Description: to change card encryption code A. Please use AuthKey to verify original code first.
=============================================================================*/
int __stdcall TP_M1SetKeyA(char *newKeyA, UINT sector_no);

/*=============================================================================
Function name:                 TP_M1WriteBlock
Function: write data
Parameter: block_no:	block_no (normally subarea*4 + block no in the subarea)
		data:	 to be written 16 bytes (32 characters)
Returned valude: error type
Description: to write a block, please use TP_M1AuthKey to verify encryption code first; e.g. subarea 9 is able to read and write the following block no: 9*4  9*4+1  9*4+2,  i.e. 36  37  38 block
=============================================================================*/
int __stdcall TP_M1WriteBlock(UINT block_no, char *data);

/*=============================================================================
Function name:                 TP_M1ReadBlock
Function: read data
Parameter: block_no:	block_no (normally subarea*4 + block no in the subarea)
Output: data:	16 bytes data, 32 characters
Returned valude: error type
Description: to read a block, please use TP_M1AuthKey to verify encryption code first =============================================================================*/
int __stdcall TP_M1ReadBlock(UINT block_no, char *data);
