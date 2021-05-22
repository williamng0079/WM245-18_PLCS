# WM245-18_PLCS
A place to track the development progress of the PLCS Assignment

Prior to running the program, please install openssl dev package using:
sudo apt-get install libssl-dev

Python version: Python 3.8.5
Python libraries required:

tkinter
subprocess                    
numpy 
PIL
sys
os


The c codes can be compiled with gcc -o "program" "program".c -lcrypto

Utilising the encryptor provided, the character limit is 214.
A 2048-bit key can encrypt up to (2048/8) – 42(OAEP padding) = 256 – 42 = 214 bytes (Ohmart, 2011).
Ohmart, P. (2011). HOW MUCH DATA CAN YOU ENCRYPT WITH RSA KEYS? [online] Available from: https://info.townsendsecurity.com/bid/29195/how-much-data-can-you-encrypt-with-rsa-keys#:~:text=The%20modulus%20size%20is%20the,256%20%E2%80%93%2042%20%3D%20214%20bytes. Accessed: 21 May 2011.
