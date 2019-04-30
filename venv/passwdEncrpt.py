#runs on Python 3.6.5

from hashlib import sha256
from passlib.hash import pbkdf2_sha256
import tkinter
from tkinter import *
from tkinter import messagebox
from py_dotenv import read_dotenv
import os

#define valid password entries
ALPHABET = ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_')

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

SECRET_KEY = os.getenv('SECRET_KEY').encode('utf-8')

# 1 takes two strings and generates a hex represenation of the hash.
def get_hexdigest(plaintext, key):
    return bytes(sha256(plaintext + key).hexdigest(), 'utf-8')  # construtcs SHA256 Hash object and returns


# 2 adds in secret key to generate a more secure password, less guessable.
def make_password(password, service):
    salt = get_hexdigest(SECRET_KEY, service)[:20]          # generates a salt based on secret key and the service being used
    hsh = get_hexdigest(salt, password)                    # get another SHA256 hash object using the former SHA256 object and general password
    return salt+hsh                                         # combine to one large SHA256 hash object


def password(plaintext, service, length = 10, alphabet = ALPHABET):
    raw_hexdigest = make_password(plaintext, service)                       # Get hashed passcode using general password and service used

    # convert hexdigest to decimal
    num = int(raw_hexdigest, 16)

    # set the modulus based on the allowed alphabet size
    num_chars = len(alphabet)

    # build up the new password one char at a time, up to certain length
    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars)                                   #takes two numbers and returns a tuple of qotient and remainder
        chars.append(ALPHABET[idx])                                         # uses the index returned to match with an index of the alphabet

    return ''.join(chars)                                                   # returns new password


#hexdIG = get_hexdigest('reddit'.encode('utf-8'),'password'.encode('utf-8'))
#print(hexdIG);

EncryptedPass = password('p@ssw0rd'.encode('utf-8'), 'reddit'.encode('utf-8'))
print("For secret Key t0ps3cr3t, service reddit, password = p@ssw0rd:")
print(EncryptedPass)


window = Tk()
window.title('Password Generator')
window.geometry('400x250')

Serv_Label = Label(text='Web Service: ')
Serv_Label.grid(column = 0, row=1)
servEntry = Entry(window, width=10)
servEntry.grid(column = 1, row =1)

GenPassLabel = Label(text='General Password: ')
GenPassLabel.grid(column = 0, row = 2)
gpEntry = Entry(window, width=10)
gpEntry.grid(column = 1, row = 2)


def clicked():
    service = servEntry.get().encode('utf-8')
    pswd = gpEntry.get().encode('utf-8')
    EncryptedPass = password(pswd, service)
    messagebox.showinfo('New Password', EncryptedPass)


btn = Button(window, text='Run Program', command=clicked)
btn.grid(column=1, row=3)

window.mainloop()

"""
print("This is your password generator")
print("Please enter your secret key: ")
SECRET_KEY = input().encode("utf-8")

service = input("What service is this password being used for (exclude .com): ").encode('utf-8')
pswd = input("Enter your password key: ").encode('utf-8')

EncryptedPass = password(pswd, service)
print("Generated password is:")
print(EncryptedPass)

"""
