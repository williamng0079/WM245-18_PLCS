# To install tkinter module please do sudo apt-get install python3-tk
# Python (2021). Subprocess. [online] Available from: https://docs.python.org/3/library/subprocess.html. Accessed: 21 May 2021.
# Gribouillis. (2010). Restart your python program. [online] Available from: https://www.daniweb.com/programming/software-development/code/260268/restart-your-python-program. Accessed: 21 May 2021.
# Codemy.com. (2019). Create Graphical User Interfaces With Python And TKinter. [online] Available from: https://www.youtube.com/watch?v=oq3lJdhnPp8&list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV&index=8. Accessed: 17 May 2021
# Kumar,B. (2020). Tkinter Checkbutton get value. [online] Available from: https://pythonguides.com/python-tkinter-checkbutton/. Accessed: 21 May 2021.
# Python Tkinter Course. (n.d). Hello Tkinter Label. [online] Available from: https://www.python-course.eu/tkinter_labels.php. Accessed: 22 May 2021.

# To-do, add instruction message on the top of the GUI.


from tkinter import *
import subprocess                    
import numpy 
from PIL import Image
from stegano_Processor_LSB import LSB_encoder, LSB_decoder
import sys
import os

def execute_RSA_encryptor():                # This will run the c executable in the same directory
    subprocess.run(["./RSA_encryptor"]) 

def execute_RSA_decryptor():
    subprocess.run(["./RSA_decryptor"])

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def format_check(in_img):
    if in_img[-4:] != ".png":
        print("Incorrect Image format supplied...")
        response_prompt = Label(window, text = "Incorrect Image format supplied...").pack()
        
        return -1

def enc_img_name_manipulation(in_img):

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
        return

def LSB_decoding_process(enc_img):
    decoded_value = LSB_decoder(enc_img)
    if decoded_value == -1:
        response_prompt = Label(window, text = "Error occurred during image opening... maybe the specified image does not exist in the current directory?").pack()
    
    elif decoded_value == 1:
        execute_RSA_decryptor()
        response = open("decrypted_message.txt", "r").read()
        
        response_prompt = Label(window, text = "HIDDEN MESSAGE:  " + response, fg = "red", font = "Helvetica 16 bold italic").pack()
    
    else:
        response_prompt = Label(window, text = decoded_value).pack()

def write_input2file(img_name, message):
    file = open("source_image_name.txt", "w")
    file.write(img_name)
    file.close()

    file = open("secret_message.txt","w")
    file.write(message)
    file.close()
    

def button_command(user_input1, user_input2, crypt_mode):
    #processing_prompt = Label(window, text = "Processing Request......").pack()
    img_input = user_input1.get()
    msg_input = user_input2.get()
    if crypt_mode.get() == 0:

        img_value = format_check(img_input)
        if img_value == -1:
            return

        else:
            write_input2file(img_input, msg_input)
            execute_RSA_encryptor()
            out_img = enc_img_name_manipulation(img_input)
            LSB_encoding_process(img_input, out_img)
    
    else:
        
        img_value = format_check(img_input)
        if img_value == -1:
            return
        else:
            write_input2file(img_input, msg_input)
            LSB_decoding_process(img_input)
        
    
    

def reset_button():
    img_var.set('')
    msg_var.set('')

#GUI configurations and layouts
if __name__ == "__main__":   

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
    mode_check = Checkbutton(window, text = "Decrypt Mode", variable = bool_mode1, onvalue=1, offvalue=0).pack()

    bool_mode2 = IntVar()   # place holder for additonal steg algorithm later.
    alg_check = Checkbutton(window, text = "Alternate Algorithm", variable = bool_mode2, onvalue = 1, offvalue = 0).pack()

    crypt_button = Button(window, text = "ENCRYPT/DECRYPT", padx = 75, pady = 40, command = lambda: button_command(src_img, sec_msg, bool_mode1)).pack()

    #reset = Button(window, text = "RESET-ENTRY", padx = 20, pady = 5, command = reset_button).pack()
    restart = Button(window, text = "RESTART", padx = 20, pady = 5, command = restart_program).pack()

    window.mainloop()