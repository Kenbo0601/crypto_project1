# CS485 PSU-CRYPT  

Kenichi Sakamoto 
kenichi2@pdx.edu  


Implementation of a block-encryption algorithm called PSU-CRYPT. 
The encryption algorithm is similar to Feistel Cipher.

How to Build:  
1: python3 encryption.py  
2: python3 decryption.py  

The encryption.py reads a standard ascii file called "plaintext.txt" and encrypts the message, this program outputs the file called "ciphertext.txt".
 
The decryption.py reads the ciphertext.txt, then it prints the original message at the end of the program.


### A list of files   
  - encrytion.py #this program encrypts the original message
  - decryption.py #this program decrypts the encrypted message
  - ftable.py #ftable which is used in both encryption and decryption process
  - plaintext.txt #contains the original message
  - ciphertext.txt #contains the encrypted message
