/* Base64.h header file source author: Sherif, W. (2013). base64.h -- Fast base64 encoding and decoding. [online] Available from: https://github.com/superwills/NibbleAndAHalf. Accessed: 18 May 2021. */
/* The documentation for the openssl version 1.1.1 c library function calls: OpenSSL. (n.d). OpenSSL libraries. [online] Available from: https://www.openssl.org/docs/man1.1.1/man3/ The documentation for the openssl version 1.1.1 c library function calls, all fucntion explainations below are researched from this source. */
/* The source of code reuse: Kusuma, R (2014). RSA Encryption & Decryption Example with OpenSSL in C. [online] Available from: http://hayageek.com/rsa-encryption-decryption-openssl-c/. Accessed: 18 May 2021 */
/* Prior to running the program, please install openssl dev package using sudo apt-get install libssl-dev */
/* The code can be compiled with "gcc -o RSA_encryptor RSA_encryptor.c -lcrypto  " */
/* Note that the key size is 2048 bits meaning that the total size of encryption will be limited to that minus the padding, alternatively, 4096-bit RSA key can be used but it will greatly slow down the speed of encryption. */
/* Header file "base64.h" is used to convert the encryptped binary into human readable text so it can be encoded later into stegano objects easiler */
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
int public_encryption(unsigned char * msg, int msg_len, char * filename, unsigned char * encrypted_msg);
void write_b64file(char * b64_msg);


/* Program Entry */
int main()
{
    char msg[2048/8] = {};                                              // Storing message withe 2048/8 limit number of chars
    char * pubkey = "stegano-example-public.pem";                       // Calling the key file name
    unsigned char encrypted_msg[4098] = {};                             // Creating a variable later to be used to store the encrypted binary
    int encrypted_length;                                               // Variable to store the len of the binary
    int encoded_len;                                                    // Store length of the encoded msg
    char * encoded_msg;                                                 // Variable for the encoded message

    
    char * secret_file = "secret_message.txt";                          // This section will be able to read a user supplied text file and extract secret message within
    FILE * fsecret = fopen(secret_file, "rb");
    fgets(msg, 256, fsecret);
    fclose(fsecret);
    printf("%s\n",msg);
    
    

    encrypted_length = public_encryption(msg, strlen(msg), pubkey, encrypted_msg); // Calling the encryption function

    if(encrypted_length == -1)                                          // Error check, -1 return means the error occur during the function.
    {
        printf("Error occured during public encryption\n");
        return 1;
    }
    
    encoded_msg = base64(encrypted_msg, encrypted_length, &encoded_len);// This function calls the base64.h header file and is able to process the binary data into human-readable base64 text.

    printf("The encoded message is:  %s\n", encoded_msg);
    printf("The encoded length is:  %d\n", encoded_len);

    write_b64file(encoded_msg);

    //printf("The encryped message is %s\n", encrypted_msg);             // Display encrypted message info for testing 
    //printf("The size of the encrypted message is %d\n", encrypted_length); 

    //FILE * f2 = fopen("RSA_encrypted_msg.bin", "wb");                  // Create a file to store and observe the encrypted binary output, used to test output of the encryption
    //fputs(encrypted_msg, f2);
    //fclose(f2);
    return 0;
    
}

/* Code Reuse: (Kusuma, 2014)*/
// The following function will have the ability to read the public key file stored within the same directory and create a RSA structure 
RSA * makeRSA(char * filename, int keytype)                             // declaring a function with the pointer return type 
{
    FILE * fp = fopen(filename,"rb");
 
    if(fp == NULL)
    {
        printf("Unable to open the public key file needed to encrypt the message\n");
        return NULL;    
    }
    RSA *rsa= RSA_new() ;  // This calls for the function within the rsa.h header, its purpose is to allocate and initialises an RSA structure, it returns a pointer to the initiated structure 
    
    if (keytype)
    {
        rsa = PEM_read_RSA_PUBKEY(fp, &rsa,NULL, NULL); // This function calls from the pem.h header and will be able to process RSA specific public key using the pointer to the RSA structure 
    }                                                   // Note that the last two arguments are supplied with NULL, this enables the default callback routine which will prompt user for passphrase 
    else 
    {
        rsa = PEM_read_RSAPrivateKey(fp, &rsa,NULL, NULL);
    }
    fclose(fp);
    return rsa;
} 

/* Code Reuse: (Kusuma, 2014)*/
// The next function is used to encrypt message with the rsa structure defined previously 
int public_encryption(unsigned char * msg, int msg_len, char * filename, unsigned char * encrypted_msg)
{
    int padding = RSA_PKCS1_OAEP_PADDING;           // Invoke padding to introduce randomness, OAEP is choose 
    
    int output_size;
    
    RSA *rsa = makeRSA(filename, 1);
    
    output_size = RSA_public_encrypt(msg_len, msg, encrypted_msg, rsa, padding);    // Encryption function process

    return output_size;
} 


// This funtion will be able to write the encoded message into a text file
void write_b64file(char * b64_msg)
{
    char * b64file = "b64_encoded_output.txt";
    FILE * f64 = fopen(b64file, "wb");
    fputs(b64_msg, f64);
    fclose(f64);
}