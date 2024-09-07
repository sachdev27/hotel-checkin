#ifndef __DEFINES_H__
#define __DEFINES_H__
   

// ��Ƭ���� 
enum ERROR_TYPE
{
    OPR_OK              =   1,      // �����ɹ�
    NO_CARD			    =   -1,     // û��⵽��Ƭ
    NO_RW_MACHINE	    =   -2,     // û��⵽������
    INVALID_CARD	    =   -3,     // ��Ч��
    CARD_TYPE_ERROR	    =   -4,     // �����ʹ���
    RDWR_ERROR		    =   -5,     // ��д����
    PORT_NOT_OPEN	    =   -6,     // �˿�δ��
    END_OF_DATA_CARD    =   -7,     // ���ݿ�����
    INVALID_PARAMETER   =   -8,     // ��Ч����
    INVALID_OPR		    =   -9,     // ��Ч����
    OTHER_ERROR		    =   -10,    // ��������
    PORT_IN_USED	    =   -11,    // �˿��ѱ�ռ��
    COMM_ERROR		    =   -12,    // ͨѶ����
    ERR_RECOVER_CLIENT  =   -13,    // �ӷ������лָ���Ȩ��ɹ�

    ERR_CLIENT          =   -20,    // �ͻ������
    ERR_LOST            =   -21,    // ����ʧ��
    ERR_TIME_INVALID    =   -22,    // ʱ����Ч
    ERR_TIME_STOPED     =   -23,    // ���Ϳ���������
    ERR_BACK_LOCKED     =   -24,    // ������
    ERR_BUILDING        =   -25,    // ¥���Ŵ���
    ERR_FLOOR           =   -26,    // ¥��Ŵ���
    ERR_ROOM            =   -27,    // ���Ŵ�
    ERR_LOW_BAT         =   -28,    // ��ص�ѹ��
    
    ERR_NOT_REGISTERED  =   -29,    // δע��
    ERR_NO_CLIENT_DATA  =   -30,     // ����Ȩ����Ϣ
    ERR_ROOMS_CNT_OVER  =   -31,    // ���������˿�������
};


// iGuestFlags, ����־������������ö��ѡ�� (�����ڰ汾)
//enum GUEST_FLAGS 
//{
//    OPTION_1			  =   0x20,      // ѡ��1, Ԥ��, ����ʵ�ʶ���
//    OPTION_2			  =   0x10		 // ѡ��2, Ԥ��, ����ʵ�ʶ���
//};


// LockSetting����������ѡ��, һ��LockSetting = LS_MASK (15)����
enum LOCK_SETTING 
{
// �ͷ���־1
    LS_REPLACE_EN       =   0x01,      // ���Ϳ�����ʹ�ܣ���һ���ӱ��Ϳ�����ǰ�淢�ı��Ϳ�
    LS_LEAD_EN          =   0x02,      // ����ʹ�ܣ�ʹ����ˢ��װ����Уʱ����������ǰ��Ҫ��ˢ��������
    LS_VALID_DATE_EN    =   0x04,      // ��Ч��ʹ�ܣ�ʹ�����ܿ���Ӧ������¥������¥�㿨���˷�����Ҫ�����Ч��
    LS_FLOOR_RANGE_EN   =   0x08,      // ���¥�㷶Χ: ʹ����¥�㿨��Ӧ�������¥�㷶Χ, ������¥���б�
    LS_CHANEL_MODE_EN   =   0x10,      // ͨ��ģʽ
	LS_FORBID_TONGUE_ALARM = 0x20,		// ��ֹ��������
    LS_ALL_REPLACE      =   0x40,       // ���ֿ�Ƭ�����������
    LS_FLAG_BYTE2_EN    =   0x80,       // �����ͷ���־�ֽ�2ʹ��

// �ͷ���־2
    LS_LOCK_IMMEDIATE_EN=   0x0100,     // б����������������, ���Ȱ����ɿ�, �������Ե�����
    LS_NO_BACKLOCK_EN   =   0x0200,     // ��λ�����п�Ƭ������ⷴ��
    LS_NO_MUSIC_EN      =   0x0400,     // ȥ�������ŵ�������, ��Ϊһ����
    LS_PROMPT_CLOSE_EN  =   0x0800,     // ��ʾ���͹���
    LS_NO_BLOCK_LIGHT_EN=   0x1000,     // ����ʱ, ��������ʾ
};


// RoomType: ��װ����RoomType������ �ͷ�����
enum ROOM_TYPE 
{
    RT_COMMON_ROOMS     =   0x1,      // ��ͨ�����׼����
    RT_SUITE_ROOMS      =   0x2,      // �׷����С�׼�
    RT_FLOOR_GATE       =   0x4,      // ¥��ͨ������
    RT_BUILDING_GATE    =   0x8,       // ¥��ͨ������
    RT_HOTEL_GATE       =   0x10        // �Ƶ����, ֻҪ�Ǳ�ϵͳ�Ŀ����ܿ�.  �ر�ע��¥���ź�¥��ŵĴ���
};


// cardFlags: ��װ����RoomType������ �ͷ�����
enum CARD_FLAGS 
{
    CF_BACK_LOCK_EN     =   0x01,      // ��������(���ֿ��ſ�)
    CF_CHANNEL_MODE     =   0x02,      // ͨ��ģʽ(���ֿ��ſ�)
    CF_PRIVILEGE_EN     =   0x04,      // ���Դ���Ҫ��Ȩ����(���ֿ��ſ�)
	
    CF_NO_REPLACE       =   0x08,     // ������ǰ��(���Ϳ�)	
	CF_IMPORT_ROOM		=	0x10,     // ���Ϳ����뷿��
	CF_OPEN_ONCE		=	0x20,     // ֻ��һ����(һ���Ա��Ϳ�)
	CF_NEW_CARD			=   0x40,     // DLock���ڰ汾�б�ʾ�¿�����ס�� ���Ʊ��Ϳ�ʱ���㡣
	CF_CHK_CHECKIN_TIME =	0x80,	  // �����סʱ��
	
	
    CF_REPLACE_EN       =   0x40,     // ����ʹ��(Ա����)
    CF_AUTO_LOST_EN     =   0x80,     // �Զ���ʧ��Ƭ(Ա����)

    CF_WHOLE_BUILDING   =   0x40,     // ����¥��Ȩ��(�˷���)
    CF_WHOLE_HOTEL      =   0x80,     // ����ϵͳȨ��(�˷���)

    CF_JUDGE_CHECKIN_TIME = 0x80,     // �ж���סʱ��ʹ��(���Ϳ�)   

    CF_CHANGE_FLAGS     = (0x01 << 16),   // ���������־
    CF_CLEAR_ROOM_INFO  = (0x02 << 16),   // ��տͷ���Ϣ(�������ÿ�)
    CF_FORBID_CARDS     = (0x04 << 16),   // �ⷿ(�������ÿ�)
    CF_SET_ONE_AREA     = (0x08 << 16),   // ��տͷ���Ϣ(�������ÿ�)
    CF_CLR_ONE_AREA     = (0x10 << 16),   // �ⷿ(�������ÿ�)
    CF_SET_ALL_AREA     = (0x20 << 16),   // ��տͷ���Ϣ(�������ÿ�)
    CF_CLR_ALL_AREA     = (0x40 << 16),   // �ⷿ(�������ÿ�)
};





// �ƿ�����
enum MAKE_CARD_TYPE 
{
    CLIENT_CARD         =   0,      // �ͻ������ͺ�
    GUEST_CARD	    	=   1,      // ���Ϳ����ͺ�
    FLOOR_CARD		    =   2,      // ¥�㿨���ͺ�
    BUILDING_CARD	    =   3,      // ¥�������ͺ�
    EMERGENT_CARD	    =   4,      // Ӧ�������ͺ�
    CHIEF_CARD		    =   5,      // �ܡ������ͺ�
    INSTALL_CARD	    =   6,      // ��װ�����ͺ�
    LOST_CARD		    =   7,      // ��ʧ�����ͺ�
    UN_LOST_CARD	    =   8,      // ȡ����ʧ�����ͺ�
    TIME_CARD		    =   9,      // Уʱ�����ͺ�
    DATA_CARD		    =   10,     // ���ݿ����ͺ�
    FACTORY_CARD	    =   11,     // ���������ͺ�
    TIME_STOP_CARD	    =   12,     // ��ֹ�����ͺ�
    UPGRADE_CARD	    =   13, 	// ������
    CHECKOUT_CARD       =   14,     // �˷���
    OFFICE_CARD         =   15,     // �칫��
    MANAGE_CARD         =   16,     // �����(ԭ����)
    STAFF_CARD          =   17,      // Ա����
    LOCK_SETTING_CARD   =   18,     // �������ÿ�
    BACKUP_CARD         =   19,     // �󱸿�
    ELEVATOR_CARD       =   20,     // ���ݿ�
};


// ��������
enum LOCK_TYPE 
{
    LT_CPU               =   1,      // TM����
    LT_IC       	    =   2,      // �Ӵ�ʽIC����
    LT_256      	    =   3,      // 256����
    LT_T5557    	    =   4,      // T5557����
    LT_MF1  		    =   5,      // MF1����
    LT_MF0      	    =   6       // MF0����
};



// ����ϵͳ��־1( LOCK_INFO.SysFlags[0] )
enum LOCK_SYS_FLAGS0
{
    LSF_LOW_BAT = 1,                // ��ѹ��־
    LSF_BACK_LOCK = 2,          // ������־
    LSF_DOOR_OPENED = 4        // �����ѿ���־
};

// ��Ƭ������Ϣ�ṹ��
struct CARD_INFO{
    char    CardNo[17];             // ����:            �ַ���, 16���ַ�
    int     CardType;               // ������          
    char    BuildingList[30];       // ¥����          
    char    FloorList[30];          // ¥���б� 
    char    RoomList[2000];         // �����б�
    char    RoomMask[13];           // ����������:      �ַ���, 12���ַ�
    char    SDateTime[20];          // ��ʼ����ʱ��:    �ַ���, 19���ַ�, ��ʽ YYYY-MM-DD hh:mm:ss, 
    char    EDateTime[20];          // ��������ʱ��:    �ַ���, 19���ַ�, ��ʽ YYYY-MM-DD hh:mm:ss, 
    char    StartTime1[9];          // ��ʼʱ��1:       �ַ���, 8���ַ�, ��ʽ hh:mm:ss
    char    EndTime1[9];            // ����ʱ��1:       �ַ���, 8���ַ�, ��ʽ hh:mm:ss
    char    StartTime2[9];          // ��ʼʱ��2:       �ַ���, 8���ַ�, ��ʽ hh:mm:ss
    char    EndTime2[9];            // ����ʱ��2:       �ַ���, 8���ַ�, ��ʽ hh:mm:ss
    char    StartTime3[9];          // ��ʼʱ��3:       �ַ���, 8���ַ�, ��ʽ hh:mm:ss
    char    EndTime3[9];            // ����ʱ��3:       �ַ���, 8���ַ�, ��ʽ hh:mm:ss

    int     iCardFlags;             // ��Ƭ�ı�־�ֽ�
    char    LostCardNo[17];          // ��ʧ����:        �ַ���, 16���ַ�

    char    CardClientNo[9];        // ��Ƭ��������Ȩ��:  �ַ���, 8���ַ�  
    char    NewClientNo[4];         // ����Ȩ�루������Ȩ����:   �ַ���, 4���ַ�(HEX��) 
    int     MF1NewSecotr;           // Mifare �µ������ţ�������Ȩ����
    char    NewKeys[13];            // Mifare �µ���Կ�����ڹ�������: �ַ���, 12���ַ�
    int     ReplaceNo;              // ������
    int     NewReplaceNo;           // ��Ȩ���е���������
    int     iRoomCnt;
    int     iAreaCnt;
    char    cAreaList[100];         // �����б�
    int     FacultyNo;              // Ժϵ��
    int     MajorNo;                // רҵ��
    int     ClassNo;                // �༶��
    char    UserName[20];           // ����

    
    int     iForbidCardType;        // ��ֹ��������Ŀ�Ƭ
    char    cForbidDateTime[20];    // �Զ��������, ��ǰʱ�䳬���������, ���Զ����

    char    cRFU1[200];              // Ԥ��
    char    cRFU2[200];              // Ԥ��
    char    cRFU3[200];              // Ԥ��
    char    cRFU4[200];              // Ԥ��

    int     iRefreshCnt;            // RFU1 Ԥ��, ������ο�Ƭ��Ϣ���ϴβ�ͬ, ��iRefreshCnt�ͻ�䶯, ���򱣳ֲ���
    int     RFU2;                   // Ԥ��
    int     RFU3;                   // Ԥ��
    int     RFU4;                   // Ԥ��   
};

// �������ݽṹ��
struct LOCK_INFO{
    int     Building;               // ¥����
    int     Floor;                  // ¥���
    char    RoomNo[20];             // ����:        �ַ���, 6���ַ�
    char    RoomMask[13];           // ����������:  �ַ���, 12���ַ�
    int     LockSetting;            // ��������ѡ��
    char    ClientPass[9];          // �ͻ���:      �ַ���, 8���ַ�
    char    StopTime[20];           // ��ֹʱ��:    �ַ���, 19���ַ�
    char    LockTime[20];           // ����ʱ��:    �ַ���, 19���ַ�
    int     RecordAddr;             // ���ż�¼��ַ
    char    sysFlags[2];            // ϵͳ��־
    char    TempSn[17];             // �ٿͿ�����:  �ַ���, 16���ַ�
    char    M1Keys[13];             // ��Կ:        �ַ���, 12���ַ�
    int     M1Sector;               // Mifare��ʹ�õ�������
    char    BlackList[40][17];      // ������:      40������, ÿ������16���ַ�
    int     LowBatCnt;              // ��ѹ�󻹿��Կ��ŵĴ���
    int     iForbidCardType;        // Ҫ��ֹ��������Ŀ�Ƭ. ���������Ŀ�Ƭ, ��Ӧ����(��Ƭ���� + 128). 
    char    cForbidDateTime[20];    // �������, ���ڿ�Ƭ�Զ��ָ�����
    char    cAreaList[100];         // ������б�
    char    cReplaceNoList[200];     // ���ֿ�Ƭ��������б�
    char    HardwareVersion[32];    // ����Ӳ���汾��
    char    FirmwareVersion[32];    // �����̼��汾
    char    DateCode[32];           // ���ڴ���

    char    cRFU1[200];              // Ԥ��
    char    cRFU2[200];              // Ԥ��
    char    cRFU3[200];              // Ԥ��
    char    cRFU4[200];              // Ԥ��

    int     RFU1;                   // Ԥ��
    int     RFU2;                   // Ԥ��
    int     RFU3;                   // Ԥ��
    int     RFU4;                   // Ԥ��  
};


// �ͷ����ݽṹ��, ��������������ʹ��
struct ROOM_INFO{
    UINT    Building;               // ¥����
    UINT    Floor;                  // ¥���
    char    RoomNo[30];             // ����:        �ַ���, ���� 001.002.00003
    UINT    RoomType;
    UINT    iAreaNo;                // �����
    UINT    Flags;                  // 
    char    cRFU1[100];             // Ԥ��
    char    cRFU2[100];             // Ԥ��
    UINT    iRFU1;                  // Ԥ��
    UINT    iRFU2;                  // Ԥ��
};



// �ֳֻ���Ϣ�ṹ��
struct HANDSIM_INFO{
	UINT    sn;						// ���к�
	char    hardwareVer[64];		// Ӳ���汾��
	char	firmwareVer[64];		// �̼��汾��
	char	releaseDatetime[20];	// ����ʱ��
	char	deviceDescription[500];	// �豸������Ϣ
	char	opeatorPassword[20];	// �ֳֻ�����Ա����

	UINT	moduleEn;				// ����ʹ����Ϣ, ����(Ҫ��λĳ���ʱ, ��λ)
	UINT    iPara1;					// ���ò���1, Ԥ��
	UINT    iPara2;					// ���ò���1, Ԥ��

    char    cRFU1[100];             // Ԥ��
    char    cRFU2[100];             // Ԥ��
    char    cRFU3[100];             // Ԥ��
    char    cRFU4[100];             // Ԥ��
    UINT    iRFU1;                  // Ԥ��
    UINT    iRFU2;                  // Ԥ��
    UINT    iRFU3;                  // Ԥ��
    UINT    iRFU4;                  // Ԥ��
};


#endif          // __DEFINES_H__