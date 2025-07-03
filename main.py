import pyaudio
import keyboard
import json
import os
import threading
import time
from ctypes import windll
from typing import Dict, Any, Optional

class PushToTalk:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.config_file = "config.json"
        self.config = self.load_config()
        self.language = self.config.get('language', 'en')
        self.messages = self.get_messages()
        
    def get_messages(self) -> Dict[str, Dict[str, str]]:
        return {
            'en': {
                'welcome': '🎤 Push To Talk For Everything',
                'language_select': 'Select language / Dil seçin:',
                'en_option': '1. English',
                'tr_option': '2. Türkçe',
                'invalid_choice': 'Invalid choice. Please select 1 or 2.',
                'mic_not_found': 'Microphone not found.',
                'cable_not_found': 'Cable Output not found.',
                'select_mic': 'Enter your microphone name (or part of it):',
                'select_key': 'Press the key you want to use for Push to Talk (keyboard or mouse button):',
                'key_pressed': 'Key pressed:',
                'save_config': 'Save these settings for next time? (y/n): (To change or delete settings later, edit or remove config.json)',
                'config_saved': 'Settings saved!',
                'config_not_saved': 'Settings not saved.',
                'invalid_input': 'Invalid input. Please enter y or n.',
                'starting': 'Starting Push to Talk...',
                'press_key_to_talk': 'Press your key to talk, release to stop.',
                'exit_instruction': 'Press Ctrl+C to exit.',
                'stopped': 'Stopped.',
                'mic_info': '🎙️ Mic -> ID: {} | Channels: {} | Rate: {}',
                'cable_info': '🔈 Cable Out -> ID: {} | Channels: {} | Rate: {}'
            },
            'tr': {
                'welcome': '🎤 Her Şey İçin Push To Talk',
                'language_select': 'Dil seçin / Select language:',
                'en_option': '1. English',
                'tr_option': '2. Türkçe',
                'invalid_choice': 'Geçersiz seçim. Lütfen 1 veya 2 seçin.',
                'mic_not_found': 'Mikrofon bulunamadı.',
                'cable_not_found': 'Cable Output bulunamadı.',
                'select_mic': 'Mikrofonunuzun adını (veya bir kısmını) girin:',
                'select_key': 'Push to Talk için kullanmak istediğiniz tuşa basın (klavye veya mouse tuşu):',
                'key_pressed': 'Basılan tuş:',
                'save_config': 'Bu ayarları bir dahaki sefere kaydetmek istiyor musunuz? (y/n): (Ayarları değiştirmek veya tamamen silmek için config.json dosyasını düzenleyebilirsiniz.)',
                'config_saved': 'Ayarlar kaydedildi!',
                'config_not_saved': 'Ayarlar kaydedilmedi.',
                'invalid_input': 'Geçersiz giriş. Lütfen y veya n girin.',
                'starting': 'Push to Talk başlatılıyor...',
                'press_key_to_talk': 'Konuşmak için tuşunuza basın, bırakınca susun.',
                'exit_instruction': 'Çıkmak için Ctrl+C tuşlayın.',
                'stopped': 'Durduruldu.',
                'mic_info': '🎙️ Mikrofon -> ID: {} | Kanallar: {} | Hız: {}',
                'cable_info': '🔈 Cable Çıkış -> ID: {} | Kanallar: {} | Hız: {}'
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def select_language(self):
        print(self.messages['en']['welcome'])
        print(self.messages['en']['language_select'])
        print(self.messages['en']['en_option'])
        print(self.messages['tr']['tr_option'])
        
        while True:
            choice = input("> ").strip()
            if choice == '1':
                self.language = 'en'
                break
            elif choice == '2':
                self.language = 'tr'
                break
            else:
                print(self.messages[self.language]['invalid_choice'])
    
    def get_input_device(self, mic_name: str = None):
        devices = []
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                devices.append((i, dev))
        
        if not devices:
            raise RuntimeError(self.messages[self.language]['mic_not_found'])
        
        if mic_name:
            # Search for device containing the specified name
            mic_name_lower = mic_name.lower()
            for i, dev in devices:
                if mic_name_lower in dev['name'].lower():
                    return {
                        "index": i,
                        "channels": int(dev['maxInputChannels']),
                        "rate": int(dev['defaultSampleRate']),
                        "name": dev['name']
                    }
        
        # If no match found or no name specified, return first available
        i, dev = devices[0]
        return {
            "index": i,
            "channels": int(dev['maxInputChannels']),
            "rate": int(dev['defaultSampleRate']),
            "name": dev['name']
        }
    
    def get_output_device(self):
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            name = dev['name'].lower()
            if dev['maxOutputChannels'] > 0 and "cable" in name:
                return {
                    "index": i,
                    "channels": int(dev['maxOutputChannels']),
                    "rate": int(dev['defaultSampleRate']),
                    "name": dev['name']
                }
        raise RuntimeError(self.messages[self.language]['cable_not_found'])
    
    def get_key_press(self):
        print(self.messages[self.language]['select_key'])
        print(self.messages[self.language]['exit_instruction'])
        
        key_pressed = [None]
        event = threading.Event()
        
        def on_key_event(e):
            if e.event_type == keyboard.KEY_DOWN:
                key_name = e.name
                print(f"\n{self.messages[self.language]['key_pressed']} {key_name}")
                key_pressed[0] = key_name
                keyboard.unhook_all()
                event.set()
        
        def on_mouse_event():
            # Mouse tuşları için ayrı thread
            VK_XBUTTON1 = 0x05  # Mouse Button 4
            VK_XBUTTON2 = 0x06  # Mouse Button 5
            VK_MBUTTON = 0x04   # Mouse Middle Button
            
            while not event.is_set():
                if windll.user32.GetKeyState(VK_XBUTTON1) & 0x80:
                    print(f"\n{self.messages[self.language]['key_pressed']} mouse4")
                    key_pressed[0] = "mouse4"
                    keyboard.unhook_all()  # Klavye hook'unu da temizle
                    event.set()
                    break
                elif windll.user32.GetKeyState(VK_XBUTTON2) & 0x80:
                    print(f"\n{self.messages[self.language]['key_pressed']} mouse5")
                    key_pressed[0] = "mouse5"
                    keyboard.unhook_all()  # Klavye hook'unu da temizle
                    event.set()
                    break
                elif windll.user32.GetKeyState(VK_MBUTTON) & 0x80:
                    print(f"\n{self.messages[self.language]['key_pressed']} mouse3")
                    key_pressed[0] = "mouse3"
                    keyboard.unhook_all()  # Klavye hook'unu da temizle
                    event.set()
                    break
                time.sleep(0.01)
        
        # Mouse tuşları için thread başlat
        mouse_thread = threading.Thread(target=on_mouse_event)
        mouse_thread.daemon = True
        mouse_thread.start()
        
        # Klavye tuşları için hook
        keyboard.hook(on_key_event)
        
        # Herhangi bir tuş basılana kadar bekle
        event.wait()
        
        # Tuş kalma sorununu önlemek için kısa bekleme
        time.sleep(0.1)
        
        return key_pressed[0]
    
    def get_key_state(self, key_name: str) -> bool:
        try:
            if key_name.startswith("mouse"):
                # Mouse tuşları için
                if key_name == "mouse3":
                    return bool(windll.user32.GetKeyState(0x04) & 0x80)  # Middle button
                elif key_name == "mouse4":
                    return bool(windll.user32.GetKeyState(0x05) & 0x80)  # Button 4
                elif key_name == "mouse5":
                    return bool(windll.user32.GetKeyState(0x06) & 0x80)  # Button 5
                else:
                    return False
            else:
                # Klavye tuşları için
                return keyboard.is_pressed(key_name)
        except:
            return False
    
    def run(self):
        # Language selection
        if 'language' not in self.config:
            self.select_language()
            self.config['language'] = self.language
        
        self.language = self.config['language']
        msg = self.messages[self.language]
        
        # Device selection
        mic_name = self.config.get('microphone_name')
        if not mic_name:
            print(msg['select_mic'])
            mic_name = input("> ").strip()
            if mic_name:
                self.config['microphone_name'] = mic_name
        
        input_dev = self.get_input_device(mic_name)
        output_dev = self.get_output_device()
        
        print(msg['mic_info'].format(input_dev['index'], input_dev['channels'], input_dev['rate']))
        print(msg['cable_info'].format(output_dev['index'], output_dev['channels'], output_dev['rate']))
        
        # Key binding
        key_name = self.config.get('key_name')
        if not key_name:
            key_name = self.get_key_press()
            self.config['key_name'] = key_name
        
        # Save configuration if config.json doesn't exist
        if not os.path.exists(self.config_file):
            while True:
                print(msg['save_config'])
                choice = input('> ').strip().lower()
                if choice in ['y', 'yes']:
                    if self.save_config():
                        print(msg['config_saved'])
                    break
                elif choice in ['n', 'no']:
                    print(msg['config_not_saved'])
                    break
                else:
                    print(msg['invalid_input'])
        
        # Audio setup
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        SAMPLE_RATE = min(input_dev['rate'], output_dev['rate'])
        CHANNELS = min(input_dev['channels'], output_dev['channels'])
        
        input_stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=SAMPLE_RATE,
                                  input=True,
                                  input_device_index=input_dev['index'],
                                  frames_per_buffer=CHUNK)
        
        output_stream = self.p.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=SAMPLE_RATE,
                                   output=True,
                                   output_device_index=output_dev['index'],
                                   frames_per_buffer=CHUNK)
        
        print(f"\n{msg['starting']}")
        print(f"{msg['press_key_to_talk']}")
        print(f"{msg['exit_instruction']}")
        
        try:
            while True:
                data = input_stream.read(CHUNK, exception_on_overflow=False)
                if self.get_key_state(key_name):
                    output_stream.write(data)
        except KeyboardInterrupt:
            print(f"\n{msg['stopped']}")
        finally:
            input_stream.stop_stream()
            input_stream.close()
            output_stream.stop_stream()
            output_stream.close()
            self.p.terminate()

if __name__ == "__main__":
    app = PushToTalk()
    app.run()