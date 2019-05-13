assignment 3

Steven Tran: fierysnake@csu.fullerton.edu

Jake Cliff tallmadman@csu.fullerton.edu

Kenny Chao: kchao@csu.fullerton.edu

Scott Ng: scottng49@csu.fullerton.edu


Python



python2 signer.py <KEY FILE NAME> <SIGNATURE FILE NAME> <INPUT FILE NAME> sign/verify


Extra Credit:

Extra credit has been implemented. Since the signature file is appeneded to the text before it goes into AES encryption.
There is no need for the signature file name

python2 signer.py <KEY FILE NAME> <INPUT FILE NAME> sign/verify/decrypt

If the user choose not to use AES encryption when signing the file, verify works. (signing causes the signature to appear
in the default file and verify will remove it)

If the user choose to encrpyt it creates a new text file called ciphertext.txt and when decrypting ciphertext will
output a new text file called plaintext.txt. The default file used will still be there but with the signature attached.

Special:

I had python3 installed in my tuffix machine so I had to specified what kind of python to use because python3 does 
print with parentheses.
