import sys, os

import math
# These are built-in CBC used for testing
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from Crypto.Cipher import AES

from hex_utils import bytexor, byteincrement

def testCrypto():
	# Tests the crypto library with an example off the internet

	key = os.urandom(32)
	iv = os.urandom(16)
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	encryptor = cipher.encryptor()
	ciphertext = encryptor.update(b"a secret message") + encryptor.finalize()
	decryptor = cipher.decryptor()
	plaintext = decryptor.update(ciphertext) + decryptor.finalize()
	print(plaintext)
	
def testBuiltInCBC(key, ciphertext_string):
	# See what ciphertext decrypts to using built-in CBC
	ciphertext = bytes.fromhex(ciphertext_string)
	iv = ciphertext[0:16]
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	decryptor = cipher.decryptor()
	plaintext = decryptor.update(ciphertext) + decryptor.finalize()
	
	# need to manually strip the padding
	padnum = plaintext[len(plaintext)-1] & 0xff
	
	print(plaintext[16:len(plaintext)-padnum])
	
def testBuiltInCTR(key, ciphertext_string):
	# See what ciphertext decrypts to using built-in CTR
	ciphertext = bytes.fromhex(ciphertext_string)
	iv = ciphertext[0:16]
	cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
	decryptor = cipher.decryptor()
	plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
	
	print(plaintext)
	
def myAesEncrypt(key, messageBlock):
	# CBC on a single block with IV of 0 is equivalent to doing just AES
	# (if we don't care about speed, which we don't)
	iv = bytes.fromhex("00000000000000000000000000000000")
	# TODO

def myCBCEncrypt(key, message): # message should be in bytes, not string
	blocksize = 16
	
	iv = os.urandom(blocksize)
	padNum = blocksize - (len(message) % blocksize)
	
	# Pad the message out to blocksize (always need at least 1 padding byte)
	for i in range(0, padNum):
		message = message + (padNum & 0xff).to_bytes(1, sys.byteorder)
		
	# Now encrypt block-by-block
	ciphertext = iv
	cipher = AES.new(key, AES.MODE_ECB)
	for i in range(0, int(len(message) / blocksize)):
		iv_block = ciphertext[i*blocksize:(i+1)*blocksize]
		plaintext_block = message[i*blocksize:(i+1)*blocksize]
		xor_block = bytexor(iv_block, plaintext_block)
		# AES encrypt previous ciphertext xor the plaintext
		ciphertext = ciphertext + cipher.encrypt(xor_block)
		
	return ciphertext
	
def myCBCDecrypt(key, ciphertext): # ciphertext should be in bytes, not string
	blocksize = 16
	
	iv = ciphertext[0:blocksize]
	
	# Decrypt block by block
	plaintext = b""
	cipher = AES.new(key, AES.MODE_ECB)
	# Note first block is IV, so skip that
	for i in range(1, int(len(ciphertext) / blocksize)):
		decrypt_block = cipher.decrypt(ciphertext[i*blocksize:(i+1)*blocksize])
		iv_block = ciphertext[(i-1)*blocksize:i*blocksize]
		plaintext = plaintext + bytexor(decrypt_block, iv_block)
	
	# need to manually strip the padding bytes in the message afterwards
	padnum = plaintext[len(plaintext)-1] & 0xff
	print(plaintext[0:len(plaintext)-padnum])

def myCTREncrypt(key, message): # message should be in bytes, not string
	# CTR encryption and decryption are the same operation, it's just a matter
	# of generating the IV on encryption	
	blocksize = 16
	iv = os.urandom(blocksize)
	return iv + myCTRDecrypt(key, iv + message)
	

def myCTRDecrypt(key, ciphertext): # ciphertext should be in bytes, not string
	blocksize = 16 # TODO this isn't included in the counter code because I'm lazy
	
	iv = ciphertext[0:blocksize]
	nonce = iv[0:8]
	counter = iv[8:16]
	# Decrypt block by block
	plaintext = b""
	cipher = AES.new(key, AES.MODE_ECB)
	# Note first block is IV, so skip that
	for i in range(1, math.ceil(len(ciphertext) / blocksize)):
		# Encrypt block is also used for decryption
		encrypt_block = cipher.encrypt(iv)
		ciphertext_block = ciphertext[i*blocksize:(i+1)*blocksize]
		plaintext = plaintext + bytexor(encrypt_block, ciphertext_block)
		# For CTR, increment only the latter 8 bytes of the IV
		# BEWARE: counter is in network byte order (bigendian)
		counter = byteincrement(counter, 'big')
		iv = nonce + counter
	
	# CTR has no padding
	return plaintext
	
def main():
	testCrypto()
	
	key1 = bytes.fromhex("140b41b22a29beb4061bda66b6747e14")
	problem1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
	problem2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"

	key2 = bytes.fromhex("36f18357be4dbd77f050515c73fcf9f2")
	problem3 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
	problem4 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
	
	testBuiltInCBC(key1, problem1)
	testBuiltInCBC(key1, problem2)
	
	testBuiltInCTR(key2, problem3)
	testBuiltInCTR(key2, problem4)
	
	myKey = os.urandom(16)
	myMessage = b"Hello, world!"
	result = myCBCEncrypt(myKey, myMessage)
	testBuiltInCBC(myKey, result.hex())
	
	myCBCDecrypt(key1, bytes.fromhex(problem1))
	myCBCDecrypt(key1, bytes.fromhex(problem2))
	print(myCTRDecrypt(key2, bytes.fromhex(problem3)))
	print(myCTRDecrypt(key2, bytes.fromhex(problem4)))
	
	result = myCTREncrypt(myKey, myMessage)
	testBuiltInCTR(myKey, result.hex())
	
	return 0

if __name__ == "__main__":
	main()