import sys, os
import urllib3
import hex_utils

http = urllib3.PoolManager(10)
TARGET = 'http://crypto-class.appspot.com/po?er='

zeroBlock = b'\x00'*16

# Pad front of bytestring with 0s
# Note, truncates front of bytestring if the string is larger than size
def padFront(bytestring, size):
	newString = zeroBlock + bytestring
	return newString[len(newString)-size : len(newString)]

def oracle(q):	#input hex text, returns status code
	target = TARGET + q                         # Create query URL
	r = http.request('GET', target)
	return r.status              # Valid pad if status = 404

def isValidPad(ciphertext):
	#print("Sending request on: " + ciphertext)

	assert(len(ciphertext) % 16 == 0)
	assert(len(ciphertext) >= 32)
	
	status = oracle(ciphertext)
	if (status == 404 or status == 200):
		return True
	if (status == 403):
		return False
	print("Unexpected status: " + str(status))
	return False
	
def solveBlock(ciphertext, initVector):

	knownBytes = bytes.fromhex("") # These are always at the end of the block
	
	# For first round, xor guess with 0x01, then replace last byte of IV with it
	# for second round, xor guess concat truth with 0x0202, then replace last 2 bytes
	
	# Iterate through each character of ciphertext block
	for i in range(0, 16):
		# generate mask of proper length
		padMask = b""
		for j in range(0, i+1):
			padMask = padMask + (i+1).to_bytes(1, sys.byteorder)
		padMask = padFront(padMask, 16)
			
		# Note: we're running in reverse to work around the case where 
		# the ciphertext already has valid padding, since xor with 1 will 
		# trick this algorithm into thinking the valid value is 1
		for j in range(255, -1, -1):
			# Guess each byte until one works
			guess = j.to_bytes(1, sys.byteorder) + knownBytes
			# Trim off excess leading zeros
			guess = padFront(guess, 16)
			
			testIv = hex_utils.bytexor(initVector, guess)
			testIv = hex_utils.bytexor(testIv, padMask)
			
			if (isValidPad((testIv + ciphertext).hex())):
				knownBytes = j.to_bytes(1, sys.byteorder) + knownBytes
				print ("known bytes:" + str(knownBytes))
				sys.stdout.flush()
				break
			
	return knownBytes

def main():
	
	# Note that we assume ciphertext is using AES CBC with random IV,
	# so we assume that block size is 16 bytes and first 16 bytes is 
	# the given IV
	
	goalCiphertext = bytes.fromhex("f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4")
	
	# Make sure assumptions about block size and IV hold true at a glance
	assert(len(goalCiphertext) % 16 == 0)
	assert(len(goalCiphertext) >= 32)
	
	# Break ciphertext into 16-byte AES blocks
	cipherBlocks = [goalCiphertext[i:i+16] for i in range(0, len(goalCiphertext), 16)]
	initVector = cipherBlocks[0]
	
	firstBlock = solveBlock(cipherBlocks[1], initVector)
	print(firstBlock) # "The Magic Words "
	plaintext = firstBlock
	
	# Block 2: "are Squeamish Os"
	# Block 3: "sifrage" (no null terminator, just padding)
	for i in range(2, len(cipherBlocks)):
		block = cipherBlocks[i]
		newInitVector = cipherBlocks[i-1]
		plaintext = plaintext + solveBlock(block, newInitVector)
	
	print(plaintext)
	
	return 0

if __name__ == "__main__":
	main()