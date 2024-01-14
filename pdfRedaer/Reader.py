import os
import pyperclip
from pynput import mouse, keyboard
import pyautogui
from PyPDF2 import PdfReader

class Reader:
    def __init__(self, filename: str | os.PathLike):
        self.filename = filename
        file = PdfReader(self.filename)
        self.content = ''
        for i in range(len(file.pages)):
            self.content += file.pages[i].extract_text()


    def selection_text(self, *args):
        pyperclip.copy("")
        pyautogui.hotkey('ctrl', 'c')
        return pyperclip.paste()



string = "Lab_Manual_1_08.pdf"