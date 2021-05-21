# To install tkinter module please do sudo apt-get install python3-tk
# Python (2021). Subprocess. [online] Available from: https://docs.python.org/3/library/subprocess.html. Accessed: 21 May 2021.

from tkinter import *
import subprocess                    
import numpy 
from PIL import Image
from stegano_Processor_LSB import LSB_encoder, LSB_decoder
import sys
import os


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


def enc_img_name_manipulation(in_img):
    if in_img[-4:] != ".png":
        print("Incorrect Image format supplied...")
        response_prompt = Label(window, text = "Incorrect Image format supplied...").pack()
        
        return -1
    else:    
        added_string = "-enc.png"
        out_name = in_img[:-4]
        out_name += added_string

        return out_name

def LSB_encoding_process(in_img, out_img):
    b64_message = open("b64_encoded_output.txt", "r").read()
    
    
    response = LSB_encoder(in_img, b64_message, out_img)
    if response == -1:
        response_prompt = Label(window, text = "Error occurred during image opening... maybe the specified image does not exist in the current directory?").pack()
    else:
        response_prompt = Label(window, text = response).pack()

def execute_RSA_encryptor():                # This will run the c executable in the same directory
    subprocess.run(["./RSA_encryptor"]) 

def write_input2file(user_input1, user_input2):
    file = open("source_image_name.txt", "w")
    entry1 = user_input1.get()
    file.write(entry1)
    file.close()

    file = open("secret_message.txt","w")
    entry2 = user_input2.get()
    file.write(entry2)
    file.close()
    
    return entry1,entry2

def button_command(user_input1, user_input2):
    entry1, entry2 = write_input2file(user_input1, user_input2)
    execute_RSA_encryptor()
    out_img = enc_img_name_manipulation(entry1)
    if out_img == -1:
        return
    else:
        LSB_encoding_process(entry1, out_img)

def reset_button():
    img_var.set('')
    msg_var.set('')
    
    
#GUI configurations and layouts
window = Tk(className = ' Steganography Toolset ')
window.geometry("700x500")



img_prompt = Label(window, text = "Image File:").pack()

img_var = StringVar()
src_img = Entry(window, width = 15, textvariable = img_var)
src_img.pack()


msg_prompt = Label(window, text = "Please Enter Secret Message (Encrytion mode only):").pack()

msg_var = StringVar()
sec_msg = Entry(window, width = 50, textvariable = msg_var)
sec_msg.pack()

bool_mode1 = IntVar()
mode_check = Checkbutton(window, text = "Decrypt Mode", variable = bool_mode1).pack()

bool_mode2 = IntVar()
alg_check = Checkbutton(window, text = "Alternate Algorithm", variable = bool_mode2).pack()

crypt_button = Button(window, text = "ENCRYPT/DECRYPT", padx = 75, pady = 40, command = lambda: button_command(src_img, sec_msg)).pack()

#reset = Button(window, text = "RESET-ENTRY", padx = 20, pady = 5, command = reset_button).pack()
restart = Button(window, text = "RESTART-AND-RESET", padx = 20, pady = 5, command = restart_program).pack()

window.mainloop()