# numpy module: sudo pip3 install numpy 
# PIL module: sudo pip3 install pillow
# Implementing LSB (Least-Significant-Bit) Image Steganography
# Notes: 
#   Within each pixel of an image, the LSB technique will be able to replace the least significant bit with the bits of the secret message (Jain, 2020).
#   To display the image, common methods used is the RGB mode(3x8-bit pixel), the pixels will form a 2D array, the LSB method will displaces the last bit of each attribute in a pixel.
#   The program processes as follows, it will collect and store the last bits of each pixel and then split the binary converted message into groups of 8 and replace the last bits in the pixels(Jain, 2020).
#   To demonstrate full understanding of the code, each line will be commented and explained.

# Source of code reuse and author: Jain, D. 2020. LSB Imgae Steganography Using Python. [online] Available from: https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2 (Accessed 15 May 2021).
# Source for all comments explaining funcitonalities of pillow Image module: pillow, n.d. Image Module. [online] Available from: https://pillow.readthedocs.io/en/stable/reference/Image.html
# Source for comments explainations of numpy: NumPy, n.d. API reference. [online] Available from: https://numpy.org/doc/stable/reference/generated/numpy.array.html. 
import numpy 
from PIL import Image       


# Code reuse: (Jain, 2020)
# Encoding function
def LSB_encoder(src_img, b64_message, out_img): # Taking the in, out image files and the b64 encoded message as function arguments

    try:
        im = Image.open(src_img, 'r')                   # Open the source image file in the read mode and store the read img into variable img

    except :
        print("Error occurred during image opening... maybe the specified image does not exist in the current directory?")    # Check for errors when opening img file
        return -1                                       # Return error for later GUI function call

    bit_list = list(im.getdata())                       # This will convert the image into a list of pixel values, note that list converts it into an ordinary sequence rather than internal PIL data type

    array = numpy.array(bit_list)                       # This creates an array object with all bits from the pixel list
    
    if im.mode == 'RGB':                                # Distinguish image mode for later encoding/decoding
        
        n = 3
    
    elif im.mode == 'RGBA':
        
        n = 4
    
    total_pixels = array.size // n                      # Here utilises the floor devision operator to divide and round down the array size by the number of bands to obtain the number of pixels in the img

    # These next lines will be able convert the input message into binary format needed for later embedding
    # Firstly, it iterates through the secret message and formats them into 8 bits binary, then it joins them together with the null delimiter. Ref: Pieters, M. (2013). https://stackoverflow.com/questions/16926130/convert-to-binary-and-keep-leading-zeros-in-python
    
    b64_message += "$KaT"                               # This will add a identifier at the end of the message to determine the end of the message
    bin_message = ''.join([format(ord(i), "08b") for i in b64_message]) # Converting the message into 8 bits binary string, while iterating through each character
    
    min_pixels = len(bin_message)                       # This takes the length of the binary data and store it as the minimum pixel required for the encoding to work

    if total_pixels < min_pixels:
       
       pixel_count_err = "Error occured: please use an image with higher pixel counts for the steganography encoding..."
       print(pixel_count_err)   
       return -2                                        # Return error for later GUI function call

    else:

        count = 0
    
    for p in range(total_pixels):                       # Iterating through each pixel of the source img
        
        for q in range(0, 3):                           # Specifying the three 8 bit value (RGB) in each pixel
            
            if count < min_pixels:
                
                array[p][q] = int(bin(array[p][q])[2:9] + bin_message[count], 2)    # One by one replacing the last bits of each pixel with the arranged bin_message with use of 2D array
                
                count += 1                              # Increment count to iterate through the loop.

    width, height = im.size                             # Gaining the image size of the read img and store within the variables width and height

    array = array.reshape(height, width, n)             # Constructing the encoded img with the new pixel array
    
    enc_im = Image.fromarray(array.astype('uint8'), im.mode)    # Form the image with the unsigned 8 bit integer
    enc_im.save(out_img)                                        # Saves the output image into the argument (out_img) passed into the function
    
    response_enc = "Image Encoded Successfully, Please See the newly created png file: " + out_img
    print(response_enc)
    return response_enc                                 # Return value for GUI calls


# Code reuse: (Jain, 2020)
# Decoding function
def LSB_decoder(src_img):

    # The following will achieve the same effect of opening and storing the image as the encoder function
    try:
        
        im = Image.open(src_img, 'r')
    
    except:

        print("Error occurred during image opening... maybe the specified image does not exist in the current directory?")
        return -1

    bit_list = list(im.getdata())               

    array = numpy.array(bit_list)

    if im.mode == 'RGB':
        n = 3
    elif im.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n


    
    hidden_bits = ""                                    # Create an empty string variable used to store the LSB of the encoded image.
    
    for p in range(total_pixels):                       # Utilising a for loop to iterate throught the pixels
        
        for q in range(0, 3):
            
            hidden_bits += (bin(array[p][q])[2:][-1])   # Populating the binary string

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)] # Sorting the binary in a group of 8 bit

    message = ""
    
    for i in range(len(hidden_bits)):                   
        if message[-4:] == "$KaT":                      # Check if the end identifier is present within the code, using [-4:] to get the last 4 character
            break
        else:
            message += chr(int(hidden_bits[i], 2))      # Converts the bits into integer value and then into character using chr
    
    if "$KaT" in message:
    
        response_dec = "Hidden Message: "+ message[:-4] # Removes the end identifier from the decoded msg
        print (response_dec)    
        file = open("b64_for_decrypt.txt", "w")         # This writes the decoded b64 into a new file so it can be read by the decryptor later.
        file.write(message[:-4])
        file.close()
        return message[:-4]
    else:
        
        response_dec = "No Hidden Message Found"
        print (response_dec)
        
        return -3                                       # For later function calls in the GUI



# Program entry point, this prevents this program being executed when functions within are called by the GUI
# The following also allow the program to run independently to the GUI.
if __name__ == "__main__":                              
    
    print("====== WELCOME TO THE LSB STEGANOGRAPHY TOOL ======")
    userinput = input("> SELECT 1 FOR ENCRYPTION MODE \n> SELECT 2 FOR DECRYPTION MODE\n")      #Input prompt
    
    if userinput == "1":
        src_img = input("> Enter the name of the image (.png only) file you would like to be encoded:\n")
        out_img = "encoded.png"
        message = input("> Enter the message you would like to be encrypted:\n")
        LSB_encoder(src_img, message, out_img)
        print("> For the encoded file, please see ecnoded.png...")
        print("...PROGRAM TERMINATING...")
    
    elif userinput == "2":
        dec_img = input("> Enter the name of the image (.png only) file you would like to be decoded:\n")
        LSB_decoder(dec_img)
        print("...PROGRAM TERMINATING...")
    
    else:
        print("> UNKNOWN INPUT PLEASE ENTER VALID INPUT\n...PROGRAM TERMINATING...")

    
        
    #secret_msg_file = "b64_encoded_output.txt"
    #b64_message = open(secret_msg_file, "r").read()