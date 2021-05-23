# WM245-18_PLCS
A place to track the development progress of the PLCS Assignment

Prior to running the c programs, please install openssl dev package using:
sudo apt-get install libssl-dev
The c codes can be compiled with gcc -o "program" "program".c -lcrypto

Python version: Python 3.8.5
Python libraries required:
    tkinter
       sudo pip3 install tk            
    numpy 
        sudo pip3 install numpy
    PIL
        sudo pip3 install pillow
    stegano
        sudo pip3 install Stegano
    subprocess
    sys
    os


Important Notes:
The maximum character limit for encryption is 214 due to the RSA key chosen, A 2048-bit key can encrypt up to (2048/8) – 42(OAEP padding) = 256 – 42 = 214 bytes (Ohmart, 2011).
Although this program utilises RSA public and private key encryption, note that the public key is not meant to be shared/uploaded in order to prevent impersonation.
In the real use senario, for each different sender and receiver, there should be a fresh key pair for them.
The GUI program has the ability to detected raw message encode and RSA encrypted encode, and is able to display and warn the user respectively.
The source image provided here is called kat.png and it was tested for the operation to create kat-enc.png and encoded.png
The kat-enc.png was created from the complete process of the tool-set
The encoded.png was encoded with raw message that is not RSA encrypted, the message was terminated with == in attempt to bypass the message content checks
The encoded.png was used to test impersonation.


Ohmart, P. (2011). HOW MUCH DATA CAN YOU ENCRYPT WITH RSA KEYS? [online] Available from: https://info.townsendsecurity.com/bid/29195/how-much-data-can-you-encrypt-with-rsa-keys#:~:text=The%20modulus%20size%20is%20the,256%20%E2%80%93%2042%20%3D%20214%20bytes. Accessed: 21 May 2011.
