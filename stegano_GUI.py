# To install tkinter module please do sudo apt-get install python3-tk
# Python (2021). Subprocess. [online] Available from: https://docs.python.org/3/library/subprocess.html. Accessed: 21 May 2021.
# Gribouillis. (2010). Restart your python program. [online] Available from: https://www.daniweb.com/programming/software-development/code/260268/restart-your-python-program. Accessed: 21 May 2021.
# Codemy.com. (2019). Create Graphical User Interfaces With Python And TKinter. [online] Available from: https://www.youtube.com/watch?v=oq3lJdhnPp8&list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV&index=8. Accessed: 17 May 2021
# Kumar,B. (2020). Tkinter Checkbutton get value. [online] Available from: https://pythonguides.com/python-tkinter-checkbutton/. Accessed: 21 May 2021.
# Python Tkinter Course. (n.d). Hello Tkinter Label. [online] Available from: https://www.python-course.eu/tkinter_labels.php. Accessed: 22 May 2021.
# jfs. (2014). subprocess.check_output return code. [online] Available from: https://stackoverflow.com/questions/23420990/subprocess-check-output-return-code. Accessed: 22 May 2021.
from tkinter import *
import subprocess                    
import numpy 
from PIL import Image
from stegano_Processor_LSB import LSB_encoder, LSB_decoder
import sys
import os


# The below two funcitons will run the c executable in the same directory
def execute_RSA_encryptor():                
    subprocess.run(["./RSA_encryptor"]) 

def execute_RSA_decryptor():
    res = subprocess.run(["./RSA_decryptor"])
    
    if res.returncode == 1:                 # 
        return -1
    else:
        return
    

# This function has the ability to restart the program to reset inputs and GUI messages
def restart_program():                      
    python = sys.executable
    os.execl(python, python, * sys.argv)


# This funtion will be able to check the user input for valid entry
def format_check(in_img):
    if in_img == "":
        print("No image supplied...")
        response_prompt = Label(window, text = "No image supplied...").pack()
        return -1
    
    elif in_img[-4:] != ".png":
        print("Incorrect Image format supplied...")
        response_prompt = Label(window, text = "Incorrect Image format supplied...").pack()
        return -1


# This function ensures messages are entered without exceeding length before encryption
def message_check(in_msg):
    if in_msg == "":
        print("No message supplied...")
        response_prompt = Label(window, text = "No message supplied...").pack()
        return -1
    
    elif len(in_msg) > 214:
        print("Message too long, the maximum length is 214 characters...")
        response_prompt = Label(window, text = "Message too long, the maximum length is 214 characters...").pack()
        return -1


# This function will manipulate the user input img name into "img"-enc.png format for easy recognition
def enc_img_name_manipulation(in_img):

    added_string = "-enc.png"
    out_name = in_img[:-4]
    out_name += added_string
    return out_name


# This fucntion will call the encryptor and encoder within the stegano processor and able output error msg onto the GUI
def LSB_encoding_process(in_img, out_img):
    execute_RSA_encryptor()
    b64_message = open("b64_encoded_output.txt", "r").read()
    response = LSB_encoder(in_img, b64_message, out_img)
    if response == -1:
        response_prompt = Label(window, text = "Error occurred when attempting to open the image... maybe the specified image does not exist in the current directory?").pack()
    
    elif response == -2:
        response_prompt = Label(window, text = "Error occured: please use an image with higher pixel counts for the steganography encoding...").pack()
    
    else:
        response_prompt = Label(window, text = response).pack()
        return


# This fucntion will call the decryptor and decoder within the stegano processor and able output error msg onto the GUI
def LSB_decoding_process(enc_img):
    decoded_value = LSB_decoder(enc_img)
    if decoded_value == -1:
        response_prompt = Label(window, text = "Error occurred when attempting to open the image... maybe the specified image does not exist in the current directory?").pack()
    
    elif decoded_value == -3:
        response_prompt = Label(window, text = "No Hidden Message Found").pack()

    elif decoded_value[-2:] == "==":
        res = execute_RSA_decryptor()
        if res == -1:
            warning_prompt = Label(window, text = "Failed to decrypt RSA, displaying the raw decoded message below: ", fg = "red").pack()
            response_prompt = Label(window, text = decoded_value).pack()
            warning_prompt = Label(window, text = "Please note that the above decoded message was encoded into the image raw without RSA encryption!!!", fg = "red").pack()
        else:
            response = open("decrypted_message.txt", "r").read()
        
            response_prompt = Label(window, text = "MESSAGE:  " + response, fg = "LightSteelBlue4", font = "Helvetica 16 bold italic").pack()
            storage_prompt = Label(window, text = "The RSA decrypted message has been successfully stored within the file decrypted_message.txt", fg = "green", font = "Helvetica 10 italic").pack()
    else:
        response_prompt = Label(window, text = decoded_value).pack()
        warning_prompt = Label(window, text = "Please note that the above decoded message was encoded into the image raw without RSA encryption!!!", fg = "red").pack()

# This function writes user entry to files so the encryption/decryption programs can read the content, this is done to acheive easier way of interfacing between tools
def write_input2file(img_nname, message):
    #file = open("source_image_name.txt", "w")
    #file.write(img_name)
    #file.close()
    if message == "":
        return
    else:
        file = open("secret_message.txt","w")
        file.write(message)
        file.close()
    

# The function that execute after the button press
def button_command(user_input1, user_input2, crypt_mode):
    #processing_prompt = Label(window, text = "Processing Request......").pack()
    img_input = user_input1.get()
    msg_input = user_input2.get()
    if crypt_mode.get() == 0:

        img_value = format_check(img_input)
        if img_value == -1:
            return
        
        else:
            msg_check_value = message_check(msg_input)
            write_input2file(img_input, msg_input)
            if msg_check_value == -1:
                return
            
            else:
                out_img = enc_img_name_manipulation(img_input)
                LSB_encoding_process(img_input, out_img)
    
    else:
        
        img_value = format_check(img_input)
        if img_value == -1:
            return
        
        else:
            write_input2file(img_input, msg_input)
            LSB_decoding_process(img_input)


# This function displays welcome message and brief program description
def welcome():
    welcome_prompt = Label(window, text = "WELCOME TO THE STEGANOGRAPHY TOOLSET!!!", fg = "steel blue", font = "Helvetica 25 bold").pack()
    
    instruction_prompt1 = Label(window, text = "This tool will take an image file and can perform the following two actions: ", font = "Helvetica 15 bold ").pack()
    instruction_prompt2 = Label(window, text = "1. Encrypt and encode the secret message into the image file entered below", font = "Helvetica 15 ").pack()
    instruction_prompt3 = Label(window, text = "2. Decode and decrypted the secret message hidden in the image file when decrypt mode is selected", font = "Helvetica 15 ").pack()
    instruction_prompt4 = Label(window, text = "IMPORTANT NOTICE",fg = "orange red", font = "Helvetica 18 bold").pack()
    instruction_prompt5 = Label(window, text = "1. The image file has to be in png format", font = "Helvetica 15 bold").pack()
    instruction_prompt6 = Label(window, text = "2. The maximum character length entered in the secret message box cannot exceed 214", font = "Helvetica 15 bold").pack()
    instruction_prompt7 = Label(window, text = "3. Please stretch the window if the message cannot be fully viewed", font = "Helvetica 15 bold").pack()

# This will reset user entries, but not used due to restarting funtion being able to handle it too
def reset_button():
    img_var.set('')
    msg_var.set('')


#GUI configurations and layouts, the program entry point
if __name__ == "__main__":   
    window = Tk(className = ' Steganography Toolset ')
    window.geometry("1000x650")

    welcome()

    img_prompt = Label(window, text = "Image File:").pack()

    img_var = StringVar()
    src_img = Entry(window, width = 15, textvariable = img_var)
    src_img.pack()

    msg_prompt = Label(window, text = "Please Enter Secret Message (For encrytion mode only):").pack()

    msg_var = StringVar()
    sec_msg = Entry(window, width = 65, textvariable = msg_var)
    sec_msg.pack(ipady = 10)


    bool_mode1 = IntVar()
    mode_check = Checkbutton(window, text = "Decryption Mode", variable = bool_mode1, onvalue=1, offvalue=0).pack()

    bool_mode2 = IntVar()   # place holder for additonal steg algorithm later.
    alg_check = Checkbutton(window, text = "Alternate STEG Mode (placeholder)", variable = bool_mode2, onvalue = 1, offvalue = 0).pack()


    crypt_button = Button(window, text = "ENCRYPT/DECRYPT", padx = 75, pady = 40, command = lambda: button_command(src_img, sec_msg, bool_mode1)).pack()

    #reset = Button(window, text = "RESET-ENTRY", padx = 20, pady = 5, command = reset_button).pack()
    restart = Button(window, text = "RESTART", padx = 20, pady = 5, command = restart_program).pack()

    window.mainloop()
    