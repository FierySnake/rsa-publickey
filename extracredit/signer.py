import os, random, struct
import sys
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from base64 import b64encode, b64decode

##################################################
# Loads the RSA key object from the location
# @param keyPath - the path of the key
# @return - the RSA key object with the loaded key
##################################################
def loadKey(keyPath):

	# The RSA key
	key = None

	# Open the key file
	with open(keyPath, 'r') as keyFile:

		# Read the key file
		keyFileContent = keyFile.read()

		# Decode the key
		decodedKey = b64decode(keyFileContent)

		# Load the key
		key = RSA.importKey(decodedKey)

		keyFile.close()

	# Return the key
	return key


##################################################
# Signs the string using an RSA private key
# @param sigKey - the signature key
# @param string - the string
##################################################
def digSig(sigKey, string):

	# TODO: return the signature of the file
	#pass

	return sigKey.sign(string,' ')

##########################################################
# Returns the file signature
# @param fileName - the name of the file
# @param privKey - the private key to sign the file with
# @return fileSig - the file signature
##########################################################
def getFileSig(fileName, privKey):

	# TODO:
	# 1. Open the file
	# 2. Read the contents
	# 3. Compute the SHA-512 hash of the contents
	# 4. Sign the hash computed in 4. using the digSig() function
	# you implemented.
	# 5. Return the signed hash; this is your digital signature
	#pass

	with open(fileName,'r') as file:
		content = file.read()
		file.close()

	dataHash = SHA512.new(content).hexdigest()

	return digSig(privKey,dataHash)


###########################################################
# Verifies the signature of the file
# @param fileName - the name of the file
# @param pubKey - the public key to use for verification
# @param signature - the signature of the file to verify
##########################################################
def verifyFileSig(fileName, pubKey, signature):

	# TODO:
	# 1. Read the contents of the input file (fileName)
	# 2. Compute the SHA-512 hash of the contents
	# 3. Use the verifySig function you implemented in
	# order to verify the file signature
	# 4. Return the result of the verification i.e.,
	# True if matches and False if it does not match
	#pass

	with open(fileName,'r') as file:
		content = file.read()
		file.close()

	dataHash = SHA512.new(content).hexdigest()
	return verifySig(dataHash,signature,pubKey)

############################################
# Saves the digital signature to a file
# @param fileName - the name of the file
# @param signature - the signature to save
############################################
def saveSig(fileName, signature):

	# TODO:
	# Signature is a tuple with a single value.
	# Get the first value of the tuple, convert it
	# to a string, and save it to the file (i.e., indicated
	# by fileName)
	signature_string = signature[0];
	signature_string = str(signature_string)
	with open(fileName,'a') as file:
		file.write('\n' + signature_string)
		file.close()
	#pass

###########################################
# Loads the signature and converts it into
# a tuple
# @param fileName - the file containing the
# signature
# @return - the signature
###########################################
def loadSig(fileName):

	with open(fileName,'r') as file:
		signature = file.read()
		file.close()

	return tuple((int(signature),None))

	# TODO: Load the signature from the specified file.
	# Open the file, read the signature string, convert it
	# into an integer, and then put the integer into a single
	# element tuple
	# pass

#################################################
# Verifies the signature
# @param theHash - the hash
# @param sig - the signature to check against
# @param veriKey - the verification key
# @return - True if the signature matched and
# false otherwise
#################################################
def verifySig(theHash, sig, veriKey):

	# TODO: Verify the hash against the provided
	# signature using the verify() function of the
	# key and return the result
	#pass

	return veriKey.verify(theHash,sig)



# The main function
def main():

	# Make sure that all the arguments have been provided
	if len(sys.argv) < 4:
		print "USAGE: " + sys.argv[0] + " <KEY FILE NAME> <INPUT FILE NAME> sign/verify/decrypt"
		exit(-1)

	# The key file
	keyFileName = sys.argv[1]

	# Signature file name
	#sigFileName = sys.argv[2]

	# The input file name
	inputFileName = sys.argv[2]

	# The mode i.e., sign or verify
	mode = sys.argv[3]

	# TODO: Load the key using the loadKey() function provided.
	Key = loadKey(keyFileName)

	# We are signing
	if mode == "sign":

		# TODO: 1. Get the file signature
		#       2. Save the signature to the file
		saveSig(inputFileName,getFileSig(inputFileName,Key))
		print "Signature saved to file ", inputFileName

		input = raw_input("Do you want to encrypt your file using AES? (YES/NO) ")
		if input == "YES":
			key = raw_input("What is the key you want to use to encrypt the message(16 letters) ")
			iv = Random.new().read(AES.block_size)
			cipher = AES.new(bytes(key),AES.MODE_CFB,iv)
			#cipher = AES.new(bytes("superkoolkid1234"),AES.MODE_CFB,iv)

			with open(inputFileName,'r') as file:
				content = file.read()
				file.close()

			ciphertext = cipher.encrypt(bytes(content)).encode("hex")
			iv = iv.encode("hex")

			#print ciphertext.encode("hex")

			with open("ciphertext.txt",'w') as file:
				file.write(ciphertext + '\n' + iv)
				file.close()

			print "AES encryption is used, ciphertext for sending is under ciphertext.txt"
		else:
			print "AES encryption not used"

	# We are verifying the signature
	elif mode == "verify":

		# TODO Use the verifyFileSig() function to check if the
		# signature signature in the signature file matches the
		# signature of the input file
		#pass
		#signature = loadSig(sigFileName)

		with open(inputFileName,'r') as file:
			files = file.readlines()
			file.close()

		files[0] = files[0].strip('\n')

		with open(inputFileName,'w') as file:
			file.write(files[0])
			file.close()

		signature = tuple((int(files[1]),None))


		if verifyFileSig(inputFileName,Key,signature) == True:
			print "Signature Matches"
		else:
			print "Signature DO NOT MATCH"

	elif mode == "decrypt":
		key = raw_input("What is the key for AES decryption? ")

		with open(inputFileName,'r') as file:
			files = file.readlines()
			file.close()

		files[0] = files[0].strip('\n')
		#print files

		iv = files[1].decode("hex")
		#cipher = AES.new(bytes("superkoolkid1234"),AES.MODE_CFB,iv)
		cipher = AES.new(bytes(key),AES.MODE_CFB,iv)

		#ciphertext = cipher.encrypt(bytes(content)).encode("hex")
		plaintext = cipher.decrypt(files[0].decode("hex"))

		plaintext = plaintext.split('\n',)

		with open("plaintext.txt",'w') as file:
			file.write(plaintext[0])
			file.close()

		signature = tuple((int(plaintext[1]),None))

		if verifyFileSig("plaintext.txt",Key,signature) == True:
			print "Signature Matches"
			print "Ciphertext has been decrypted, plaintext for reading is under plaintext.txt"
		else:
			print "Signature DO NOT MATCH"
			print "MESSAGE HAS BEEN COMPROMISED"

	else:
		print "Invalid mode ", mode

### Call the main function ####
if __name__ == "__main__":
	main()
