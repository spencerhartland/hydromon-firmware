class UUIDs:
        # Device Information Service
        DEV_INFO_SERVICE = 0x180A
        
        # DIS - Characterisitcs
        # Manufacturer's Name String
        DIS_MFC_NAME = 0x2A29
        # Model Number String
        DIS_MODEL_NUM = 0x2A24
        # Firmware Revision String
        DIS_FIRMWARE_REV = 0x2A26
        # Software Revision String
        DIS_SOFTWARE_REV = 0x2A28

        # Preferences Service
        PREFERENCES_SERVICE = "3302752a-7beb-4888-b085-e11754996bb2"
        # Prefs Service - Characteristics
        # LCD Standby Message
        PREF_LCD_STANDBY_MESSAGE = "4a91052a-662d-47ca-b0aa-f07027740024"
        # LCD Alert Message
        PREF_LCD_AERT_MESSAGE = "a54cb484-e60e-4d12-8a5a-496d037d98d4"
        # LCD Standby Color
        PREF_LCD_STANDBY_COLOR = "29794ca0-0950-40a9-a415-a51c48e42a65"
        # LCD Alert Color
        PREF_LCD_ALERT_COLOR = "d46d5a24-ea99-4d8b-97f0-3ddeafbaeaa1"
        # LED Standby Color
        PREF_LED_STANDBY_COLOR = "7188af7a-2e34-4601-8b9f-86c870e7fa75"
        # LED Alert Color
        PREF_LED_ALERT_COLOR = "66158896-dc53-49af-8939-b199f967ecb6"
        # Standby Timeout
        PREF_STANDBY_TIMEOUT = "305709aa-36d6-4fa1-a2cc-7a3500bcbacb"
        # Alert Timeout
        PREF_ALERT_TIMEOUT = "8c995b1b-42a6-417d-9c0f-73f1763b8c38"
        # Alert Delay
        PREF_ALERT_DELAY = "18aea917-aab1-470f-8585-56554ecf238e"
        # OLED Max Brightness
        PREF_OLED_MAX_BRIGHTNESS = "944b859f-3a45-4fbd-80c5-186a1c6ec4bf"
        # Sip Size
        PREF_SIP_SIZE = "0795115d-6604-4dad-abb8-21290b91d256"
        
        
        

# Default values for all characteristics
dictionary = {
    # { service: {characteristic, characteristic, ...} }
    # Device Information Service
    UUIDs.DEV_INFO_SERVICE: {
        # {UUID: (vaue, read, write), ...}
        # Manufacturer's Name String
        UUIDs.DIS_MFC_NAME: ("s01101000", True, False),
        # Model Number String
        UUIDs.DIS_MODEL_NUM: ("m00000001", True, False),
        # Firmware Revision String
        UUIDs.DIS_FIRMWARE_REV: ("0.0.0", True, False),
        # Software Revision String
        UUIDs.DIS_SOFTWARE_REV: ("0.0.0", True, False)
    },
    # Preferences Service
    UUIDs.PREFERENCES_SERVICE: {
        # LCD Standby Message
        UUIDs.PREF_LCD_STANDBY_MESSAGE: ("go vegan or die!", True, True),
        # LCD Alert Message
        UUIDs.PREF_LCD_AERT_MESSAGE: ("Have some water!", True, True),
        # LCD Standby Color
        UUIDs.PREF_LCD_STANDBY_COLOR: ("#00ff00", True, True),
        # LCD Alert Color
        UUIDs.PREF_LCD_ALERT_COLOR: ("#ff0000", True, True),
        # LED Standby Color
        UUIDs.PREF_LED_STANDBY_COLOR: ("#00ff00", True, True),
        # LED Alert Color
        UUIDs.PREF_LED_ALERT_COLOR: ("#ff0000", True, True),
        # Standby Timeout
        UUIDs.PREF_STANDBY_TIMEOUT: ("5", True, True),
        # Alert Timeout
        UUIDs.PREF_ALERT_TIMEOUT: ("5", True, True),
        # Alert Delay
        UUIDs.PREF_ALERT_DELAY: ("60", True, True),
        # OLED Max Brightness
        UUIDs.PREF_OLED_MAX_BRIGHTNESS: ("255", True, True),
        # Sip Size
        UUIDs.PREF_SIP_SIZE: ("60", True, True)
    }
}
