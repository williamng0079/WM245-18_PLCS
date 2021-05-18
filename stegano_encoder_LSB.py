# Implementing LSB (Least-Significant-Bit) Image Steganography
# Notes: 
#   Within each pixel of an image, the LSB technique will be able to replace the least significant bit with the bits of the secret message (Jain, 2020).
#   To display the image, common methods used is the RGB mode(3x8-bit pixel), the pixels will form a 2D array, the LSB method will displaces the last bit of each attribute in a pixel.
#   The program processes as follows, it will collect and store the last bits of each pixel and then split the binary converted message into groups of 8 and replace the last bits in the pixels(Jain, 2020).
#   To demonstrate full understanding of the code, each line will be commented and explained.
#   Source of code reuse and author: Jain, D. 2020. LSB Imgae Steganography Using Python. [online] Available from: https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2 (Accessed 15 May 2021)
 

# The library utilised to perform the encoding tasks are numpy and PIL (pillow).
# I am using Numpy to convert the source image into a numpy array of pixels through steps of checks and calculations.
# The PIL library will provide me with series of well established APIs so that i can interface with the source image.
# Source for all comments explaining funcitonalities of pillow Image module: pillow, n.d. Image Module. [online] Available from: https://pillow.readthedocs.io/en/stable/reference/Image.html
# Source for comments explainations of numpy: NumPy, n.d. API reference. [online] Available from: https://numpy.org/doc/stable/reference/generated/numpy.array.html. 
import numpy 
from PIL import Image       


# The following function will have the ability to encode the b64 message into the source image supplied
def LSB_encoder(src_img, b64_message, out_img): # Taking the in, out image files and the b64 encoded message as function arguments

    im = Image.open(src_img, 'r')               # Open the source image file in the read mode and store the read img into variable img

    bit_list = list(im.getdata())               # This will convert the image into a list of pixel values, note that list converts it into an ordinary sequence rather than internal PIL data type

    array = numpy.array(bit_list)           # This creates an array object with all bits from the pixel list
    
    if im.mode == 'RGB':
        
        n = 3
    
    elif im.mode == 'RGBA':
        
        n = 4
    
    total_pixels = array.size // n              # Here utilises the floor devision operator to divide and round down the array size by the number of bands to obtain the number of pixels in the img

    # This next line will be able convert the input message into binary format needed for later embedding
    # Firstly, it iterates through the secret message and formats them into 8 bits binary, then it joins them together with the null delimiter. Ref: Pieters, M. (2013). https://stackoverflow.com/questions/16926130/convert-to-binary-and-keep-leading-zeros-in-python
    bin_message = ''.join([format(ord(i), "08b") for i in b64_message]) 
    
    min_pixels = len(bin_message)               # This takes the length of the binary data and store it as the minimum pixel required for the encoding to work

    if total_pixels < min_pixels:
       
       print("Error occured: please use an image with higher pixel counts for the steganography encoding...")
    
    else:
        
        count = 0
    
    for p in range(total_pixels):               # Iterating through each pixels of the source img
        
        for q in range(0, 3):                   # Specifying the three 8 bit value (RGB) in each pixel
            
            if count < min_pixels:
                
                array[p][q] = int(bin(array[p][q])[2:9] + bin_message[count], 2)    # Replacing the last bits of each pixel with the arranged bin_message
                
                count += 1                      # increment count to iterate through the loop.

    width, height = im.size                     # Gaining the pixel size of the read img and store within the variables width and height

    array = array.reshape(height, width, n)     # Reconstructing the new encoded image
    
    enc_im = Image.fromarray(array.astype('uint8'), im.mode)    # Crafting the image again with the unsigned 8 bit integer
    enc_im.save(out_img)                                        # Saves the output image into the argument (out_img) passed into the function
    
    print("Image Encoded Successfully")


src_img = "kat.png"
b64_message = "b64_encoded_output.txt"
out_img = "kat-enc.png"

LSB_encoder(src_img, b64_message, out_img)