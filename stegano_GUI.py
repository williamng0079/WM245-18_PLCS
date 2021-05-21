# To install tkinter module please do sudo apt-get install python3-tk

from tkinter import *

def write_input2file(user_input1, user_input2):
    file = open("source_image_name.txt", "w")
    entry1 = user_input1.get()
    file.write(entry1)
    file.close()

    file = open("secret_message_test.txt","w")
    entry2 = user_input2.get()
    file.write(entry2)
    file.close()


#GUI configurations and layouts
window = Tk(className = ' Steganography Toolset ')
window.geometry("700x500")



img_prompt = Label(window, text = "Image File:").pack()


src_img = Entry(window, width = 15)
src_img.pack()

msg_prompt = Label(window, text = "Please Enter Secret Message (Encrytion mode only):").pack()


sec_msg = Entry(window, width = 50)
sec_msg.pack()

bool_mode = IntVar()
mode_check = Checkbutton(window, text = "Decrypt Mode", variable = bool_mode).pack()

bool_mode = IntVar()
alg_check = Checkbutton(window, text = "Alternate Algorithm", variable = bool_mode).pack()

crypt_button = Button(window, text = "ENCRYPT/DECRYPT", padx = 75, pady = 40, command = lambda: write_input2file(src_img, sec_msg)).pack()



window.mainloop()