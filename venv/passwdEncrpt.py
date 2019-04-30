#runs on Python 3.6
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
def get_hexdigest(salt, password):
    return bytes(sha256(salt + password).hexdigest(), 'utf-8')

# 2 adds in secret key to generate a more secure password, less guessable.
def make_password(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, service)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return salt+hsh


def password(plaintext, service, length = 10, alphabet = ALPHABET):
    raw_hexdigest = make_password(plaintext, service)

    print(raw_hexdigest)
    #convert hexdigest to decimal
    num = int(raw_hexdigest, 16)

    #what base to convert num into
    num_chars = len(alphabet)

    # build up the new password one char at a time, up to certain length
    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars) #takes two numbers and returns a tuple of qotient and remainder

        chars.append(ALPHABET[idx]) # uses the index returned to match with an index of the alphabet

    return ''.join(chars)


#hexdIG = get_hexdigest('reddit'.encode('utf-8'),'password'.encode('utf-8'))
#print(hexdIG);

EncryptedPass = password('p@ssw0rd'.encode('utf-8'), 'reddit'.encode('utf-8'))
print("For secret Key t0ps3cr3t, service reddit, password = p@ssw0rd:")
print(EncryptedPass)


window = Tk()
window.title('Password Generator')
window.geometry('400x250')

'''
SK_label = Label(text='Secret Key: ')
SK_label.grid(column = 0, row = 0)
skeyEntry =  Entry(window, width = 10)
skeyEntry.grid(column = 1, row = 0)
'''

Serv_Label = Label(text='Web Service: ')
Serv_Label.grid(column = 0, row=1)
servEntry = Entry(window, width=10)
servEntry.grid(column = 1, row =1)

GenPassLabel = Label(text='General Password: ')
GenPassLabel.grid(column = 0, row = 2)
gpEntry = Entry(window, width=10)
gpEntry.grid(column = 1, row = 2)


def clicked():
    SECRET_KEY = skeyEntry.get().encode('utf-8')
    service = servEntry.get().encode('utf-8')
    pswd = gpEntry.get().encode('utf-8')
    EncryptedPass = password(pswd, service)

    messagebox.showinfo('Output', EncryptedPass)


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
