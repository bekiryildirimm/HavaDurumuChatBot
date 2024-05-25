from PIL import Image, ImageTk
import tkinter as tk
import os
import asyncio
import winsdk.windows.devices.geolocation as wdg
import speech_recognition as sr
import google.generativeai as genai
import emoji
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
class ChatBot():
    def __init__(self, name):
        print("-----", name, "Başlatılıyor-----")
        self.name = name
        self.mesaj=""
        self.generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
        }
        self.safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },]
        self.history=[
  {
    "role": "user",
    "parts": ["Sen kullanıcılara güncel hava durumu bilgileri, çevresel etkinlikler ve iklim değişikliği hakkında bilgi sunan bir asistansın"]
  }]
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            entry.delete("1.0", tk.END)
            entry.insert("1.0", "Dinleniyor")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio,language='tr')
            print("me --> ", self.text)
        except:
            print("me -->  ERROR")
        return self.text

    def model_start(self):
        genai.configure(api_key="AIzaSyDVBfSjtqdfYYTN7h428cIQlKcKKC78ovI")
        self.model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=self.generation_config,
                              safety_settings=self.safety_settings)

        self.convo = self.model.start_chat(history=[

            {
                "role": "user",
                "parts": ["you are an assistant for weather and enviroment information"]
            },
            {
                "role": "model",
                "parts": [
                    "Understood! I'm Gemini, your friendly assistant for all things weather and environment-related. How can I assist you today? \n\nWould you like to know the current weather conditions somewhere, the forecast for the next few days, or perhaps some environmental data like air quality or pollen levels? Just let me know!"]
            },
            {
                "role": "user",
                "parts": [
                    "merhaba senin adın ChatBot,"
                    " öncelikle kendini tanit ve enlem=37.01000000,boylam=37.3000000000 olan konum neresidir ve o konum hava durumu bilgileri nedir bunlari açikla, vereceğin cevap kullanıcıyı karşılamak için olacak ilk mesajındır, bu isteği kullanıcı yapmadı, ve kullanıcının bu istekten haberi yok vereceğin cevap kullanıcının göreceği ilk mesajdır o yüzden senden bir istek yapılmamış gibi kendi başına cevap veriyormuşsun gibi cevap ver"]
            },
            {
                "role": "model",
                "parts": [
                    "Merhaba! Ben ChatBot, hava durumu ve çevre bilgileri konusunda yardımcı olmak için buradayım. \n\nKonumunuza bakılırsa, şu an Gaziantep'tesiniz gibi görünüyor.  Gaziantep için hava durumu şu anda oldukça güzel, güneşli ve sıcak bir gün sizi bekliyor. Güneş kreminizi ve şapkanızı yanınıza almayı unutmayın! \n\nGaziantep için geçerli hava durumu bilgileri:\n\n Hava Durumu: Parçalı bulutlu\n Sıcaklık: 17°C\n Rüzgar Hızı: 11 km/sa\n Nem Oranı: %52\n Görünürlük: 10 km\n\nBu bilgiler en son bir saat önce alınmıştır ve değişkenlik gösterebilir. "]
            },
        ])
        return self.convo

       # convo=self.model_start()
    def gemini(self,text):
        self.convo.send_message(text)
        self.convo.last.text
        mesajs=self.convo.last.text.replace("*", "")
        print(mesajs)
        return self.convo.last.text
def contains_emoji(text):
    return any(emoji.is_emoji(char) for char in text)
async def getCoords():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return [pos.coordinate.latitude, pos.coordinate.longitude]
def on_chat_box_focus_in(event):
    if chat_area.get("1.0", tk.END).strip() == "":
        lat, lon = asyncio.run(getCoords())
        chat_area.config(state=tk.NORMAL)  # Sohbet kutusunu düzenlenebilir hale getir
        mesaj = ai.gemini(f"merhaba senin adın chatbot, görevin kullanıcılara güncel hava durumu bilgileri, çevresel etkinlikler ve iklim değişikliği hakkında bilgi sunmaktır, kullanman gereken dil Türkçedir, chatbot öncelikle kendini tanit ve enlem={lat}, boylam={lon} olan konum neresidir ve o konum hava durumu bilgileri nedir bunlari açikla, vereceğin cevap kullanıcıyı karşılamak için olacak ilk mesajındır, bu isteği kullanıcı yapmadı, ve kullanıcının bu istekten haberi yok vereceğin cevap kullanıcının göreceği ilk mesajdır o yüzden senden bir istek yapılmamış gibi kendi başına cevap veriyormuşsun gibi cevap ver, ve cevab verdikten sonra bir sohbet başlayacak cevabını ona göre ver.")
        # chat_area.insert(tk.END, "ChatBot: \n\n")
        chat_area.insert(tk.END, "ChatBot: {}\n\n".format(mesaj)) # Başlangıç mesajını ekle
        chat_area.config(state=tk.DISABLED)
def send_message_with_button():
    entry.delete("1.0", tk.END)
    entry.insert("1.0", "Dinleniyor")
    message = ai.speech_to_text()
    entry.delete("1.0", tk.END)
    entry.insert("1.0", message)

def on_entry_focus_in(event):
    if entry.get("1.0", tk.END).strip() == "Buraya bir istem girin":
        entry.delete("1.0", tk.END)
        entry.config(fg=text_color)

def on_entry_focus_out(event):
    if not entry.get("1.0", tk.END).strip():
        entry.insert("1.0", "Buraya bir istem girin")
        entry.config(fg="gray")

def on_entry_key_press(event):
    if entry.get("1.0", tk.END).strip() == "Buraya bir istem girin":
        entry.delete("1.0", tk.END)
        entry.config(fg=text_color)
def update_button_color(event=None):
    message = entry.get("1.0", tk.END).strip()
    # Eğer mesaj kutusu boşsa
    if not message:
        entry.delete("1.0", tk.END)
        entry.insert("1.0", "Buraya bir istem girin")
        entry.config(fg="gray")
        send_button.config(bg='#D1D5DB')
        return

    send_button.config(bg='#D1D5DB')

def send_message(event=None):
    message = entry.get("1.0", tk.END)
    if message.strip() != "":
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "\nBen: {}\n".format(message))
        mesaj=ai.gemini(message)
        if contains_emoji(mesaj):
            chat_area.tag_config('emoji', font=('Segoe UI Emoji', 12))
            chat_area.insert(tk.END, "ChatBot: {}\n\n".format(mesaj), 'emoji')
        else:
            chat_area.insert(tk.END, "ChatBot: {}\n\n".format(mesaj))


        chat_area.see(tk.END)
        chat_area.config(state=tk.DISABLED)
        entry.delete("1.0", tk.END)
        update_button_color()

ai = ChatBot(name="Gemini")
ai.model_start()
# Ana pencereyi oluştur
root = tk.Tk()
root.title("ChatBot")
root.configure(bg='#333333')
root.resizable(width=False, height=False)
# Metin rengi
text_color = '#FFFFFF'  # Beyaz renk
chat_area = tk.Text(root, wrap=tk.WORD, width=60, height=20, state=tk.DISABLED, bg='#222222', fg=text_color)
chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
chat_area.bind('<FocusIn>', on_chat_box_focus_in)
entry = tk.Text(root, wrap=tk.WORD, width=60, height=2, bg='#222222', fg="gray", bd=1, relief=tk.FLAT)
entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
entry.insert("1.0", "Buraya bir istem girin")
entry.bind('<FocusIn>', on_entry_focus_in)
entry.bind('<FocusOut>', on_entry_focus_out)
entry.bind('<Key>', on_entry_key_press)
entry.bind('<KeyRelease>', update_button_color)


send_button = tk.Button(root, text="Gönder", bg='#D1D5DB', command=send_message, borderwidth=0, highlightthickness=0, relief='flat')
send_button.grid(row=1, column=1, padx=(0, 10), pady=5, sticky="e")
new_button = tk.Button(root, text="Mikrofon", bg='#D1D5DB', command=send_message_with_button, borderwidth=0, highlightthickness=0, relief='flat')
new_button.grid(row=1, column=2, padx=10, pady=5)

root.bind('<Return>', send_message)

on_chat_box_focus_in(None)
root.mainloop()
