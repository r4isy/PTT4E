import pyaudio
import keyboard
import json
import os
import threading
import time
from ctypes import windll
from typing import Dict, Any, Optional
import pystray
from PIL import Image
import sys
import webbrowser

class PushToTalk:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.config_file = "config.json"
        self.config = self.load_config()
        self.language = self.config.get('language', 'en')
        self.messages = self.get_messages()
        self.tray_icon = None
        self.tray_thread = None
        self.tray_running = threading.Event()
        self.tray_state = 'deactive'
        self.input_stream = None
        self.output_stream = None
        
    def get_messages(self) -> Dict[str, Dict[str, str]]:
        return {
            'en': {
                'welcome': '🎤 Push To Talk For Everything',
                'language_select': 'Select language / Dil seçin:',
                'en_option': '1. English',
                'tr_option': '2. Türkçe',
                'invalid_choice': 'Invalid choice. Please select 1 or 2.',
                'requirements_warning': '⚠️  IMPORTANT: This application requires VB-Cable Virtual Audio Device to work properly.',
                'requirements_info': 'If you don\'t have VB-Cable installed, please download and install it from:',
                'requirements_url': 'https://vb-audio.com/Cable/',
                'requirements_install_guide': 'After installation, restart this application and your computer.',
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
                'cable_info': '🔈 Cable Out -> ID: {} | Channels: {} | Rate: {}',
                'audio_devices_changed': 'Audio devices changed, reinitializing...',
                'reinitializing_streams': 'Reinitializing audio streams...',
                'failed_reinitialize': 'Failed to reinitialize audio, stopping...',
                'max_retries_reached': 'Maximum retry attempts reached. Stopping audio loop.',
                'input_stream_recovered': 'Input stream recovered successfully.',
                'failed_recover_output': 'Failed to recover output stream: {}',
                'failed_recover_input': 'Failed to recover input stream: {}',
                'unexpected_error': 'Unexpected error in audio loop: {}',
                'failed_reinitialize_audio': 'Failed to reinitialize audio: {}',
                'error_checking_devices': 'Error checking audio devices: {}',
                'github_star_request': 'Would you like to contribute to our project by giving a star on GitHub? (y/n) [default: n]:',
                'github_star_thanks': 'Thank you! Opening GitHub repository...',
                'github_star_declined': 'No problem! Thank you for using PTT4E.'
            },
            'tr': {
                'welcome': '🎤 Her Şey İçin Push To Talk',
                'language_select': 'Dil seçin / Select language:',
                'en_option': '1. English',
                'tr_option': '2. Türkçe',
                'invalid_choice': 'Geçersiz seçim. Lütfen 1 veya 2 seçin.',
                'requirements_warning': '⚠️  ÖNEMLİ: Bu uygulamanın çalışması için VB-Cable Virtual Audio Device gereklidir.',
                'requirements_info': 'VB-Cable yüklü değilse, lütfen şu adresten indirip yükleyin:',
                'requirements_url': 'https://vb-audio.com/Cable/',
                'requirements_install_guide': 'Yüklemeden sonra bu uygulamayı ve bilgisayarınızı yeniden başlatın.',
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
                'cable_info': '🔈 Cable Çıkış -> ID: {} | Kanallar: {} | Hız: {}',
                'audio_devices_changed': 'Ses cihazları değişti, yeniden başlatılıyor...',
                'reinitializing_streams': 'Ses akışları yeniden başlatılıyor...',
                'failed_reinitialize': 'Ses yeniden başlatılamadı, durduruluyor...',
                'max_retries_reached': 'Maksimum yeniden deneme sayısına ulaşıldı. Ses döngüsü durduruluyor.',
                'input_stream_recovered': 'Giriş akışı başarıyla kurtarıldı.',
                'failed_recover_output': 'Çıkış akışı kurtarılamadı: {}',
                'failed_recover_input': 'Giriş akışı kurtarılamadı: {}',
                'unexpected_error': 'Ses döngüsünde beklenmeyen hata: {}',
                'failed_reinitialize_audio': 'Ses yeniden başlatılamadı: {}',
                'error_checking_devices': 'Ses cihazları kontrol edilirken hata: {}',
                'github_star_request': 'GitHub repomuza yıldız vererek katkı sağlamak ister misiniz? (y/n) [varsayılan: n]:',
                'github_star_thanks': 'Teşekkürler! GitHub repository\'si açılıyor...',
                'github_star_declined': 'Sorun değil! PTT4E\'yi kullandığınız için teşekkürler.'
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
            mic_name_lower = mic_name.lower()
            for i, dev in devices:
                if mic_name_lower in dev['name'].lower():
                    return {
                        "index": i,
                        "channels": int(dev['maxInputChannels']),
                        "rate": int(dev['defaultSampleRate']),
                        "name": dev['name']
                    }
        
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
            VK_XBUTTON1 = 0x05
            VK_XBUTTON2 = 0x06 
            VK_MBUTTON = 0x04 
            
            while not event.is_set():
                if windll.user32.GetKeyState(VK_XBUTTON1) & 0x80:
                    print(f"\n{self.messages[self.language]['key_pressed']} mouse4")
                    key_pressed[0] = "mouse4"
                    keyboard.unhook_all() 
                    event.set()
                    break
                elif windll.user32.GetKeyState(VK_XBUTTON2) & 0x80:
                    print(f"\n{self.messages[self.language]['key_pressed']} mouse5")
                    key_pressed[0] = "mouse5"
                    keyboard.unhook_all() 
                    event.set()
                    break
                elif windll.user32.GetKeyState(VK_MBUTTON) & 0x80:
                    print(f"\n{self.messages[self.language]['key_pressed']} mouse3")
                    key_pressed[0] = "mouse3"
                    keyboard.unhook_all() 
                    event.set()
                    break
                time.sleep(0.01)
        
        mouse_thread = threading.Thread(target=on_mouse_event)
        mouse_thread.daemon = True
        mouse_thread.start()
        
        keyboard.hook(on_key_event)
        
        event.wait()
        
        time.sleep(0.1)
        
        return key_pressed[0]
    
    def get_key_state(self, key_name: str) -> bool:
        try:
            if key_name.startswith("mouse"):
                if key_name == "mouse3":
                    return bool(windll.user32.GetKeyState(0x04) & 0x80)
                elif key_name == "mouse4":
                    return bool(windll.user32.GetKeyState(0x05) & 0x80)
                elif key_name == "mouse5":
                    return bool(windll.user32.GetKeyState(0x06) & 0x80) 
                else:
                    return False
            else:
                return keyboard.is_pressed(key_name)
        except:
            return False
    
    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)
    
    def ptt_loop(self, input_stream, output_stream, key_name, CHUNK, input_dev, output_dev):
        max_retries = 3
        retry_count = 0
        device_check_counter = 0
        
        while self.tray_running.is_set():
            try:
                device_check_counter += 1
                if device_check_counter >= 1000:
                    if not self.check_audio_devices(input_dev, output_dev):
                        print(self.messages[self.language]['reinitializing_streams'])
                        new_input, new_output = self.reinitialize_audio(input_dev, output_dev, CHUNK)
                        if new_input and new_output:
                            input_stream = new_input
                            output_stream = new_output
                            self.input_stream = new_input
                            self.output_stream = new_output
                            retry_count = 0 
                        else:
                            print(self.messages[self.language]['failed_reinitialize'])
                            break
                    device_check_counter = 0
                
                data = input_stream.read(CHUNK, exception_on_overflow=False)
                if self.get_key_state(key_name):
                    self.tray_state = 'active'
                    try:
                        output_stream.write(data)
                    except OSError as e:
                        print(f"Output stream error: {e}")
                        try:
                            output_stream.stop_stream()
                            output_stream.close()
                            output_stream = self.p.open(format=pyaudio.paInt16,
                                                       channels=output_dev['channels'],
                                                       rate=output_dev['rate'],
                                                       output=True,
                                                       output_device_index=output_dev['index'],
                                                       frames_per_buffer=CHUNK)
                        except Exception as recover_error:
                            print(self.messages[self.language]['failed_recover_output'].format(recover_error))
                            break
                else:
                    self.tray_state = 'deactive'
                    
            except OSError as e:
                print(f"Audio device error: {e}")
                retry_count += 1
                
                if retry_count >= max_retries:
                    print(self.messages[self.language]['max_retries_reached'])
                    break
                
                try:
                    input_stream.stop_stream()
                    input_stream.close()
                    input_stream = self.p.open(format=pyaudio.paInt16,
                                             channels=input_dev['channels'],
                                             rate=input_dev['rate'],
                                             input=True,
                                             input_device_index=input_dev['index'],
                                             frames_per_buffer=CHUNK)
                    print(self.messages[self.language]['input_stream_recovered'])
                except Exception as recover_error:
                    print(self.messages[self.language]['failed_recover_input'].format(recover_error))
                    break
                    
                time.sleep(1)
                
            except KeyboardInterrupt:
                self.tray_running.clear()
                break
            except Exception as e:
                print(self.messages[self.language]['unexpected_error'].format(e))
                time.sleep(0.1) 

    def tray_icon_worker(self):
        def create_icon(state):
            icon_path = self.resource_path('tray-active.ico') if state == 'active' else self.resource_path('tray-deactive.ico')
            return Image.open(icon_path)

        def on_quit(icon, item):
            self.tray_running.clear()
            icon.stop()

        menu = pystray.Menu(pystray.MenuItem('Quit', on_quit))
        icon = pystray.Icon('PTT4E', create_icon(self.tray_state), 'PTT4E', menu)
        self.tray_icon = icon

        def icon_updater():
            while self.tray_running.is_set():
                icon.icon = create_icon(self.tray_state)
                time.sleep(0.2)

        updater_thread = threading.Thread(target=icon_updater, daemon=True)
        updater_thread.start()
        icon.run()
        updater_thread.join(timeout=1)

    def check_audio_devices(self, input_dev, output_dev):
        try:
            # MIT License (c) 2025 r4isy - official build only
            device_count = self.p.get_device_count()
            input_found = False
            output_found = False
            
            for i in range(device_count):
                dev = self.p.get_device_info_by_index(i)
                if i == input_dev['index'] and dev['maxInputChannels'] > 0:
                    input_found = True
                if i == output_dev['index'] and dev['maxOutputChannels'] > 0:
                    output_found = True
            
            if not input_found or not output_found:
                print(self.messages[self.language]['audio_devices_changed'])
                return False
            return True
        except Exception as e:
            print(self.messages[self.language]['error_checking_devices'].format(e))
            return False
    
    def reinitialize_audio(self, input_dev, output_dev, CHUNK):
        try:
            self.p.terminate()
            self.p = pyaudio.PyAudio()
            
            input_stream = self.p.open(format=pyaudio.paInt16,
                                      channels=input_dev['channels'],
                                      rate=input_dev['rate'],
                                      input=True,
                                      input_device_index=input_dev['index'],
                                      frames_per_buffer=CHUNK)
            
            output_stream = self.p.open(format=pyaudio.paInt16,
                                       channels=output_dev['channels'],
                                       rate=output_dev['rate'],
                                       output=True,
                                       output_device_index=output_dev['index'],
                                       frames_per_buffer=CHUNK)
            
            return input_stream, output_stream
        except Exception as e:
            print(self.messages[self.language]['failed_reinitialize_audio'].format(e))
            return None, None

    def cleanup(self):
        try:
            if self.input_stream:
                self.input_stream.stop_stream()
                self.input_stream.close()
            if self.output_stream:
                self.output_stream.stop_stream()
                self.output_stream.close()
            if self.p:
                self.p.terminate()
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def __del__(self):
        self.cleanup()

    def run(self):
        if 'language' not in self.config:
            self.select_language()
            self.config['language'] = self.language
        
        self.language = self.config['language']
        msg = self.messages[self.language]
        
        print(f"\n{msg['requirements_warning']}")
        print(f"{msg['requirements_info']}")
        print(f"{msg['requirements_url']}")
        print(f"{msg['requirements_install_guide']}")
        print() 
        
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
        
        key_name = self.config.get('key_name')
        if not key_name:
            key_name = self.get_key_press()
            self.config['key_name'] = key_name
        
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
        
        self.ask_github_star()
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        SAMPLE_RATE = min(input_dev['rate'], output_dev['rate'])
        CHANNELS = min(input_dev['channels'], output_dev['channels'])
        
        self.input_stream = self.p.open(format=FORMAT,
                                       channels=CHANNELS,
                                       rate=SAMPLE_RATE,
                                       input=True,
                                       input_device_index=input_dev['index'],
                                       frames_per_buffer=CHUNK)
        
        self.output_stream = self.p.open(format=FORMAT,
                                        channels=CHANNELS,
                                        rate=SAMPLE_RATE,
                                        output=True,
                                        output_device_index=output_dev['index'],
                                        frames_per_buffer=CHUNK)
        
        print(f"\n{msg['starting']}")
        print(f"{msg['press_key_to_talk']}")
        print(f"{msg['exit_instruction']}")

        self.tray_running.set()
        ptt_thread = threading.Thread(target=self.ptt_loop, args=(self.input_stream, self.output_stream, key_name, CHUNK, input_dev, output_dev), daemon=True)
        ptt_thread.start()
        try:
            self.tray_icon_worker()
        except KeyboardInterrupt:
            print(f"\n{msg['stopped']}")
            self.tray_running.clear()
            if self.tray_icon:
                self.tray_icon.stop()
        finally:
            ptt_thread.join(timeout=1)
            self.cleanup()

    def ask_github_star(self):

        if self.config.get('github_star_asked', False):
            return
        
        print(self.messages[self.language]['github_star_request'])
        choice = input('> ').strip().lower()
        
        if not choice:
            choice = 'n'
        
        if choice in ['y', 'yes']:
            print(self.messages[self.language]['github_star_thanks'])
            try:
                webbrowser.open('https://github.com/r4isy/PTT4E')
            except Exception as e:
                print(f"Error opening browser: {e}")
        else:
            print(self.messages[self.language]['github_star_declined'])
        
        self.config['github_star_asked'] = True
        self.save_config()

if __name__ == "__main__":
    app = PushToTalk()
    app.run()

    
