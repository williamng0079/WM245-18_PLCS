#include <stdio.h>
#include <string.h>
#include <openssl/pem.h>
#include <openssl/ssl.h>
#include <openssl/rsa.h>
#include <openssl/evp.h>
#include <openssl/bio.h>
#include <openssl/err.h>

/* https://www.openssl.org/docs/man1.1.1/man3/ : The documentation for the openssl version 1.1.1 c library function calls, all fucntion explainations below are researched from this source. */
/* http://hayageek.com/rsa-encryption-decryption-openssl-c/ : The source reference of this code, author: Kusuma, R (2014) */
/* Prior to running the program, please install openssl dev package using sudo apt-get install libssl-dev */

/* The code can be compiled with "gcc -o RSA_encrypt RSA_encrypt.c -lcrypto  " */


/* Function prototypes */
RSA * makeRSA(char * filename, int keytype);
int public_encryption(unsigned char * msg, int msg_len, char * filename, unsigned char * encrypted_msg);


/* Program Entry */
int main()
{
    char msg[2048/8] = "This is the secret message to be encrypted";    // Storing message withe 2048/8 limit number of chars
    char * pubkey = "stegano-example-public.pem";                       // Calling the key file name
    unsigned char encrypted_msg[4098] = {};                             // Creating a variable later to be used to store the encrypted binary
    int encrypted_length;                                               // Variable to store the len of the binary

    encrypted_length = public_encryption(msg, strlen(msg), pubkey, encrypted_msg); // Calling the encryption function

    if(encrypted_length == -1)                                          // Error check, -1 return means the error occur during the function.
    {
        printf("Error occured during public encryption\n");
        exit(0);
    }
    
    //printf("The encryped message is %s\n", encrypted_msg);             // Display encrypted message for testing 

    printf("The size of the encrypted message is %d\n", encrypted_length); 
    
    FILE * f2 = fopen("RSA_encrypted_msg.bin", "wb");                    // Create a file to store and observe the encrypted binary output

    fputs(encrypted_msg, f2);
    fclose(f2);
    
    return 0;
    
}

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


// The next function is used to encrypt message with the rsa structure defined previously 

int public_encryption(unsigned char * msg, int msg_len, char * filename, unsigned char * encrypted_msg)
{
    int padding = RSA_PKCS1_OAEP_PADDING;           // Invoke padding to introduce randomness, OAEP is choose 
    
    int output_size;
    
    RSA *rsa = makeRSA(filename, 1);
    
    output_size = RSA_public_encrypt(msg_len, msg, encrypted_msg, rsa, padding);    // Encryption process

    return output_size;
} 

