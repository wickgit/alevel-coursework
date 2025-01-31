import tkinter as tk
import multiprocessing

from ciphers.affine import AffineDecrypt, AffineEncrypt
from ciphers.caesar import CaesarDecrypt, CaesarEncrypt
from ciphers.keyword import KeywordDecrypt, KeywordEncrypt
from ciphers.scytale import ScytaleDecrypt, ScytaleEncrypt
from ciphers.vigenere import VigenereEncrypt, VigenereDecrypt
from utilities import SUBTITLE_LABEL_OPTIONS, TITLE_LABEL_OPTIONS


class Application(tk.Tk):
    """Handles swapping between windows"""

    def __init__(self):
        super(Application, self).__init__()
        # set the window title & that it is not resizable.
        self.title("Шифри русофобів")
        self.resizable(0, 0)
        self.frame = None
        # When first opened, display the Main Menu
        self.show_main_menu()

    def show_main_menu(self):
        """ Shows the main menu. Avoids circular imports """
        self.show(MainMenu)

    def show(self, frame_class=None, *args, **kwargs):
        """ Constructs an instance of the class frame_class and shows the resulting frame """
        # remove the old frame if there was one
        if self.frame is not None:
            self.frame.forget()
        # make the new frame and pack it into the window
        self.frame = frame_class(self, *args, **kwargs)
        self.frame.pack()

    def show_existing(self, frame):
        """ Shows a frame which was already created by the show() method"""
        # remove the old frame if there was one
        if self.frame is not None:
            self.frame.forget()
        # pack the new frame into the window
        self.frame = frame
        self.frame.pack()


class MainMenu(tk.Frame):
    def __init__(self, application):
        super().__init__(application)
        self.application = application
        self.next_row = 1
        self.create_widgets()

    def create_subtitle(self, text):
        """Helper function to simplify the creation of subtitles"""
        # make the subtitle
        tk.Label(self, text=text, **SUBTITLE_LABEL_OPTIONS).grid(row=self.next_row, sticky="NW")
        # increment the next_row variable so the next item goes on the next row
        self.next_row += 1

    def create_cipher_entry(self, cipher_name, cipher_encrypt, cipher_decrypt):
        """Helper function to simplify the creation of cipher entries. If there is one shared encrypt and decrypt window, pass None to cipher_decrypt"""
        # add label with the cipher's name
        tk.Label(self, text=cipher_name).grid(row=self.next_row, column=0, sticky="NW")

        if cipher_decrypt is not None:
            # different encrypt and decrypt buttons

            # setup the encrypt button
            def encrypt_command():
                self.application.show(cipher_encrypt)
            encrypt_button = tk.Button(self, text="Зашифрувати", command=encrypt_command)
            encrypt_button.grid(row=self.next_row, column=1, sticky="NESW")

            # setup the decrypt button
            def decrypt_command():
                self.application.show(cipher_decrypt)
            decrypt_button = tk.Button(self, text="Розшифрувати", command=decrypt_command)
            decrypt_button.grid(row=self.next_row, column=2, sticky="NESW")

        # increment the next_row variable so the next item goes on the next row
        self.next_row += 1

    def create_widgets(self):
        """ Setup the widgets for the main menu """
        white_space = ' '
        tk.Label(self, text="Українські Шифри", **TITLE_LABEL_OPTIONS).grid(row=0, sticky="NW")
        self.create_cipher_entry(f"Шифр Цезаря{white_space*6}", CaesarEncrypt, CaesarDecrypt)
        self.create_cipher_entry(f"Афінний шифр{white_space*6}", AffineEncrypt, AffineDecrypt)
        self.create_cipher_entry(f"Keyword шифр{white_space*6}", KeywordEncrypt, KeywordDecrypt)
        self.create_cipher_entry(f"Шифр Віженера{white_space*6}", VigenereEncrypt, VigenereDecrypt)
        self.create_cipher_entry(f"Шифр Скитала{white_space*6}", ScytaleEncrypt, ScytaleDecrypt)


if __name__ == "__main__":
    # Setup multiprocessing if built as an executable
    multiprocessing.freeze_support()
    # Only start the program when this file is run, not when it is imported.
    Application().mainloop()
