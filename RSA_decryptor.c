/* Base64.h header file source author: Sherif, W. (2013). base64.h -- Fast base64 encoding and decoding. [online] Available from: https://github.com/superwills/NibbleAndAHalf. Accessed: 18 May 2021. */
/* The documentation for the openssl version 1.1.1 c library function calls: OpenSSL. (n.d). OpenSSL libraries. [online] Available from: https://www.openssl.org/docs/man1.1.1/man3/ The documentation for the openssl version 1.1.1 c library function calls, all fucntion explainations below are researched from this source. */

/* Prior to running the program, please install openssl dev package using sudo apt-get install libssl-dev */
/* The code can be compiled with "gcc -o RSA_decryptor RSA_decryptor.c -lcrypto  " */
/* Note that the key size is 2048 bits meaning that the total size of encryption will be limited to that minus the padding, alternatively, 4096-bit RSA key can be used but it will greatly slow down the speed of encryption. */
/* Header file "base64.h" is used to convert the encryptped binary into human readable text so it can be encoded later into stegano objects easiler */
/* The source of code reuse: Kusuma, R (2014). RSA Encryption & Decryption Example with OpenSSL in C. [online] Available from: http://hayageek.com/rsa-encryption-decryption-openssl-c/. Accessed: 18 May 2021 */


#include <stdio.h>
#include <string.h>
#include <openssl/pem.h>
#include <openssl/ssl.h>
#include <openssl/rsa.h>
#include <openssl/evp.h>
#include <openssl/bio.h>
#include <openssl/err.h>
#include "base64.h"  

/* Function prototypes */
RSA * makeRSA(char * filename, int keytype);
int private_decryption(unsigned char * encrypted_msg, int msg_len, char * filename, unsigned char * decrypted_msg);
void write_decrypt(char * dec_msg);

/* Program Entry */
int main()
{
    char b64_msg[350] = {};                                             // Storing the max size of 350 b64 encoded message
    char * privkey = "stegano-example-private.pem";                     // Calling the key file name
    unsigned char decoded_msg[4098] = {};                          
    int decrypted_length;                                               // Variable to store the len of the decrypted msg
    int decoded_len;                                                    // Store length of the decoded msg
    unsigned char decrypted_msg[4098] = {};                                     
    
    char * b64_file = "b64_for_decrypt.txt";                            // This section will be able to read the b64_encoded file and extract text within
    FILE * f64 = fopen(b64_file, "rb");
    fgets(b64_msg, 350, f64);
    fclose(f64);
    printf("%s\n",b64_msg);
    
    //decoded_msg[4098] = unbase64(b64_msg, 350, &decoded_len);

    decrypted_length = private_decryption( unbase64(b64_msg, 344, &decoded_len) , 256, privkey, decrypted_msg); // This function takes the required argument and decrypts the binary into text

    if(decrypted_length == -1)                                          // Error check, -1 return means the error occur during the function.
    {
        printf("Error occured during decryption\n");
        return 1;
    }
    
    write_decrypt(decrypted_msg);
    //printf("The decoded message is:  %s\n", decoded_msg);
    printf("The decoded length is:  %d\n", decoded_len);
    printf("The decrypted message is: \n\n%s\n\n", decrypted_msg);

    
    return 0;
    
}

/* Code Reuse: (Kusuma, 2014)*/
// The following function will have the ability to read the private key file stored within the same directory and create a RSA structure 
RSA * makeRSA(char * filename, int keytype)       // RSA pointer return type                      
{
    FILE * fp = fopen(filename,"rb");
 
    if(fp == NULL)                                // Error check
    {   
        printf("Unable to open the public key file needed to encrypt the message\n");
        return NULL;    
    }
    RSA *rsa= RSA_new() ;  // This calls for the function within the rsa.h header, its purpose is to allocate and initialises an RSA structure, it returns a pointer to the initiated structure 
    
    if (keytype)           // This detected the mode selected by the user, if keytype is not null, it will invoke read public key funtion 
    {
        rsa = PEM_read_RSA_PUBKEY(fp, &rsa,NULL, NULL); // This function calls from the pem.h header and will be able to process RSA specific public key using the pointer to the RSA structure 
    }                                                   // Note that the last two arguments are supplied with NULL, this enables the default callback routine which will not prompt user for passphrase 
    else                   // Else, it will use the read private key mode used for decryption
    {
        rsa = PEM_read_RSAPrivateKey(fp, &rsa,NULL, NULL);
    }
    fclose(fp);
    return rsa;
} 

/* Code Reuse: (Kusuma, 2014)*/
/* This funciton is the decryption process*/
int private_decryption(unsigned char * encrypted_msg, int msg_len, char * filename, unsigned char * decrypted_msg)
{
    int padding = RSA_PKCS1_OAEP_PADDING;  // Using the OAEP padding to match the encryption process
    
    int output_size;
    
    RSA *rsa = makeRSA(filename, 0);       // Selected 0 mode will allow makeRSA to invoke private key read. 
    
    output_size = RSA_private_decrypt(msg_len, encrypted_msg, decrypted_msg, rsa, padding); // Decrypting binary
    
    return output_size; 
}

// This funtion will be able to write the decoded message into a text file for it to be read and displayed later by the GUI
void write_decrypt(char * dec_msg)
{
    char * dec_file = "decrypted_message.txt";
    FILE * d = fopen(dec_file, "wb");
    fputs(dec_msg, d);
    fclose(d);
}