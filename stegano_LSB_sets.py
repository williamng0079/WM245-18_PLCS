# For this tool, the ustilised method is LSB-set 
# LSB set uses a very similar encoding technique as the least significant bit.
# The only difference is the ability to select specific pixels within the image to hide the hidden message utilising established sequences to choose.

# Source of code reuse: Stegano. (n.d.). Using Stegano as a Python module. [online] Available from: https://stegano.readthedocs.io/en/latest/module.html#lsb-method-with-sets.
from stegano import lsbset
from stegano.lsbset import generators

# Code reuse: (Stegano, n.d.)
#This function encodes the message utlising lsbset from the Stegano module
def LSB_sets_encoder(in_img, message, out_img):
    
    set_generator = generators.eratosthenes()
    
    try: 
        encoded_image = lsbset.hide(in_img, message, set_generator)
    except:
        print("Unexpected Error occured during LSB sets encoding, please ensure image name input is correct or size of the image is not big enough...")
        
        return -1

    encoded_image.save(out_img)

    response_enc = "Image Encoded Successfully utilising LSB-SETS, Please See the newly created png file: " + out_img

    return response_enc

# Code reuse: (Stegano, n.d.)
# Decoding function
def LSB_sets_decoder(enc_img):

    set_generator = generators.eratosthenes()
    
    try:
        extracted_message =  lsbset.reveal(enc_img, set_generator)
    except:
        print("Unexpected error: LSB sets decoding failed, image specified may not exist or there is no hidden message?")
        return -1
    
    print("The Hidden message is: " + extracted_message)
    file = open("b64_for_decrypt.txt", "w")         # This writes the decoded b64 into a new file so it can be read by the decryptor later.
    file.write(extracted_message)
    file.close()
    return extracted_message


# Main entry to provide standalong execution
if __name__ == "__main__":                              
    
    print("====== WELCOME TO THE LSB STEGANOGRAPHY TOOL (SETS MODE) ======")
    userinput = input("> SELECT 1 FOR ENCRYPTION MODE \n> SELECT 2 FOR DECRYPTION MODE\n")      #Input prompt
    
    if userinput == "1":
        src_img = input("> Enter the name of the image (.png only) file you would like to be encoded:\n")
        out_img = "encoded-set.png"
        message = input("> Enter the message you would like to be encrypted:\n")
        LSB_sets_encoder(src_img, message, out_img)
        print("> For the encoded file, please see ecnoded-set.png...")
        print("...PROGRAM TERMINATING...")
    
    elif userinput == "2":
        dec_img = input("> Enter the name of the image (.png only) file you would like to be decoded:\n")
        LSB_sets_decoder(dec_img)
        print("...PROGRAM TERMINATING...")
    
    else:
        print("> UNKNOWN INPUT PLEASE ENTER VALID INPUT\n...PROGRAM TERMINATING...")
