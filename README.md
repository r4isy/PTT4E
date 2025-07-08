# 🎤 PTT4E - Push To Talk For Everything

[![Download PTT4E](https://img.shields.io/static/v1?label=Download&message=PTT4E&color=blue)](https://github.com/r4isy/PTT4E/releases)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)


A versatile push-to-talk application that works with any input device and any key combination. Perfect for gamers, streamers, and anyone who needs flexible voice activation.

> 📝 Tip: All dependencies are listed in `requirements.txt`


---

## 🇹🇷 Türkçe

### Ne İşe Yarar?

PTT4E, herhangi bir mikrofon ve herhangi bir tuş kombinasyonu ile çalışan esnek bir push-to-talk uygulamasıdır. Oyun oynarken, yayın yaparken veya sesli iletişim kurarken sesinizi istediğiniz tuşla kontrol edebilirsiniz.


### Özellikler

- 🎯 **Esnek Tuş Seçimi**: Mouse tuşları, klavye tuşları, hatta mouse tekerleği bile kullanabilirsiniz
- 🎤 **Mikrofon Seçimi**: Sisteminizdeki herhangi bir mikrofonu seçebilirsiniz
- 🌍 **Çok Dilli Destek**: Türkçe ve İngilizce dil desteği
- 💾 **Ayarları Kaydetme**: Tercihlerinizi kaydedip bir dahaki sefere otomatik yükler
- ⚡ **Hızlı Çıkış**: Ctrl+C ile anında çıkış
- 🔧 **Kolay Kurulum**: Tek dosya, minimum bağımlılık

### Kurulum

1. **Python'u yükleyin** (3.7 veya üzeri)
2. **Uygulamayı başlatın**:
   - **Kolay yol**: `start.bat` dosyasına çift tıklayın
   - **Manuel yol**:
     ```bash
     pip install -r requirements.txt
     python main.py
     ```

> 💡 Eğer `main.py` dosyasını doğrudan çalıştırıyorsanız,  
> `tray-active.ico` ve `tray-deactive.ico` dosyalarının aynı klasörde bulunduğundan emin olun.  
> Bunlar, sistem tepsisinde mikrofon durumu simgeleri için gereklidir.


### Kullanım

1. **Dil seçin**: İlk çalıştırmada Türkçe veya İngilizce seçin
2. **Mikrofon seçin**: Mikrofonunuzun adını (veya bir kısmını) girin
3. **Tuş atayın**: Push-to-talk için kullanmak istediğiniz tuşa basın (klavye veya mouse tuşu)
4. **Kullanmaya başlayın**: Atadığınız tuşa basılı tutarak konuşun. Kenu

> **Ayarları değiştirmek veya tamamen silmek için config.json dosyasını düzenleyebilirsiniz.**

> 🎨 **Tray İkonlarını Kişiselleştirin**  
> `tray-active.ico` ve `tray-deactive.ico` dosyalarını kendi simgelerinizle değiştirerek istediğiniz görünümü kullanabilirsiniz.  
> Dosya adları aynı kalmalı ve `main.py` ile aynı klasörde olmalıdır.

### Gereksinimler

- Windows 10/11
- Python 3.7+
- Mikrofon
- VB-Cable Virtual Audio Device (çıkış için)

### Sorun Giderme

**"Mikrofon bulunamadı" hatası alıyorsanız:**
- Mikrofonunuzun Windows'ta çalıştığından emin olun
- Mikrofon adını doğru yazdığınızdan emin olun

**"Cable Output bulunamadı" hatası alıyorsanız:**
- VB-Cable Virtual Audio Device'ı yükleyin
- Ses ayarlarından çıkış cihazını kontrol edin

---

## 🇺🇸 English

### What Does It Do?

PTT4E is a flexible push-to-talk application that works with any microphone and any key combination. Control your voice with any key you want while gaming, streaming, or communicating.


### Features

- 🎯 **Flexible Key Binding**: Use mouse buttons, keyboard keys, or even mouse wheel
- 🎤 **Microphone Selection**: Choose any microphone on your system
- 🌍 **Multi-language Support**: Turkish and English language support
- 💾 **Settings Persistence**: Save your preferences for next time
- ⚡ **Quick Exit**: Exit instantly with Ctrl+C
- 🔧 **Easy Setup**: Single file, minimal dependencies

### Installation

1. **Install Python** (3.7 or higher)
2. **Run the application**:
   - **Easy way**: Double-click on `start.bat` file
   - **Manual way**: 
     ```bash
     pip install -r requirements.txt
     python main.py
     ```

> 💡 If you're running `main.py` directly (not the .exe),  
> make sure `tray-active.ico` and `tray-deactive.ico` are in the same folder.  
> These are required for tray icon support.


### Usage

1. **Select language**: Choose Turkish or English on first run
2. **Choose microphone**: Enter your microphone name (or part of it)
3. **Bind key**: Press the key you want to use for push-to-talk (keyboard or mouse button)
4. **Start using**: Hold your assigned key to talk

> **To change or delete your settings, edit or remove config.json.**

> 🎨 **Customize Your Tray Icons**  
> Replace `tray-active.ico` and `tray-deactive.ico` with your own icons to personalize your tray experience.  
> Make sure filenames stay the same and icons are in the same folder as `main.py`.

### Requirements

- Windows 10/11
- Python 3.7+
- Microphone
- VB-Cable Virtual Audio Device (for output)

### Troubleshooting

**Getting "Microphone not found" error:**
- Make sure your microphone is working in Windows
- Check that you typed the microphone name correctly

**Getting "Cable Output not found" error:**
- Install VB-Cable Virtual Audio Device
- Check your audio output settings

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements!

## 💗 Contributors

<a href="https://github.com/sansrough">
  <img src="https://github.com/sansrough.png" width="100" />
</a>

## ⚠️ Disclaimer

This application is for educational and personal use. Make sure to comply with your local laws and regulations regarding audio recording and transmission.

---

**Made with ❤️ for the gaming and streaming community** 
