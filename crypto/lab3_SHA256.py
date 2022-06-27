import sys, os
import hashlib

# Length of data block
dataBlockLen = 1024
# Length of hash value (in bytes)
hashLen = 32

# Given a file, generate the final hash that would be generate with a 1024-byte scheme.
# It is encoded as follows:
# 1) Calculate the hash on the last (possibly partial) block
# 2) Append this hash to the previous block, then calculate the hash on the
#    MODIFIED block (1024 bytes + 32 byte hash)
# 3) Final hash is the hash of the first block with the next block's hash appended
def generateHash(filename):
	
	file = open(filename, "rb")
	fileContents = file.read()
	
	lastBlockLen = len(fileContents) % dataBlockLen
	lastBlockContents = fileContents[len(fileContents) - lastBlockLen : len(fileContents)]
	hash = hashlib.sha256(lastBlockContents).digest()
	
	# Starting from the last block, calculate the hash on each previous block
	
	# First calculate index of second-to-last block, then iterate back block-by-block
	for i in range(len(fileContents) - lastBlockLen - dataBlockLen, -1, -dataBlockLen):
		modifiedBlock = fileContents[i : i+dataBlockLen] + hash
		hash = hashlib.sha256(modifiedBlock).digest()
	
	file.close()
	return hash

# Scheme is: assume we have a file encoded in 1024-byte blocks that have a 32-byte
# has appended to it.
# Note that we don't have a test file pre-generated, so we can't really test this
# effectively.
def validateFile(filename, hash):

	isValid = True

	# Each data block has the next block's hash appended to it
	readBlockLen = dataBlockLen + hashLen

	file = open(filename, "rb")
	
	nextHash = hash
	nextBlock = file.read(readBlockLen)
	i = 0 # for debugging
	while(len(nextBlock) > 0):
		if len(nextBlock) == readBlockLen:
			if nextHash != hashlib.sha256(nextBlock):
				print("Hash mismatch on block " + str(i) + "!")
				print(nextHash.hex() + " != " + hashlib.sha256(nextBlock).hexdigest())
				isValid = False
				break
			nextHash = nextBlock[dataBlockLen:dataBlockLen+hashLen]
		else:
			# Final block, don't need to do anything else
			break
		nextBlock = file.read(readBlockLen)
		i += 1
		
	file.close()
	return isValid

# Function for generating basic files for help with testing. These are files with known
# hashes validated by instructor:
#first hash of b4:
#d8f8a9eadd284c4dbd94af448fefb24940251e75ca2943df31f7cfbb6a4f97ed
#
#second hash of b3+b4hash:
#26949e3320c315f179e2dfc95a4158dcf9a9f6ebf3dfc69252cd83ad274eeafa
#
#third hash of b2+b3hash:
#946e42c2bd9cbb56dcbefe0eea7ad361e18a4a052421b088b8050b1ba99795ff
#
#final hash of b1+b2hash and test answer:
#af7aca38c840da949c02a57e1c31d48ab7a1b9c7486638a892f2409770ec3ae5
def generateBasicFiles():
	rawhex1 = b'\x11'*1024
	rawhex2 = b'\x22'*1024
	rawhex3 = b'\x33'*1024
	rawhex4 = b'\x44'*773
	e1 = open('b1','wb')
	e2 = open('b2','wb')
	e3 = open('b3','wb')
	e4 = open('b4','wb')
	t1 = open('test11223344','wb')
	e1.write(rawhex1)
	e2.write(rawhex2)
	e3.write(rawhex3)
	e4.write(rawhex4)
	t1.write(rawhex1+rawhex2+rawhex3+rawhex4)
	t1.close()
	e1.close()
	e2.close()
	e3.close()
	e4.close()

def main():

	# This hash validates the generated files
	basicHash = bytes.fromhex("af7aca38c840da949c02a57e1c31d48ab7a1b9c7486638a892f2409770ec3ae5")
	# This is the hash used to validate the first block of the test video
	testHash = bytes.fromhex("03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8")

	# Test with my known generated files
	generateBasicFiles()
	assert(generateHash("test11223344") == basicHash)

	# Test that this works on the provided test file
	assert(generateHash("lab3_test_video.mp4") == testHash)
	
	# Finally, generate problem solution
	print(generateHash("lab3_problem_video.mp4").hex())
	
	return 0

if __name__ == "__main__":
	main()