import sys, os
import base64
  
def xor_crypt_string(data, key = 'awesomepassword', encode = False, decode = False):
	from itertools import cycle

	print(data)
	if decode:
		data = base64.decodestring(data)
		print("decoded: " + str(data))
	xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))

	xored_bytes = bytes(xored, 'utf-8')

	if encode:
		return base64.encodestring(xored_bytes).strip()
	return xored
   
def bytexor(a, b, byteorder=sys.byteorder):	# xor two bytestrings of different lengths
	# fix to the shortest length
	outlen = min(len(a), len(b))
	a, b = a[:len(b)], b[:len(a)]
	
	int_a = int.from_bytes(a, byteorder)
	int_b = int.from_bytes(b, byteorder)
	int_xor = int_a ^ int_b
	
	return int_xor.to_bytes(outlen, byteorder)
	
def bytenot(bytestr, byteorder=sys.byteorder):	# bitwise 'not' on a bytestring
	
	size = len(bytestr)
	as_int = int.from_bytes(bytestr, byteorder)
	result_int = toUnsignedInt(~as_int, size)
	return result_int.to_bytes(size, byteorder)
	
def byteincrement(bytestr, byteorder=sys.byteorder): # bitstring + 1
	#print(bytestr.hex())
	size = len(bytestr)
	as_int = int.from_bytes(bytestr, byteorder)
	result_int = toUnsignedInt(as_int + 1, size)
	return result_int.to_bytes(size, byteorder)

def toUnsignedInt(val, size):
	# Python automatically pads out integers to much longer than the original
	# size, so this function returns the value to its original byte length.
	# This is necessary because bitwise operators operate on the larger integers.
	return val & (~(-1 << (size * 8)))

def main():
	#secret_data = "XOR procedure"
	#print("The cipher text is")
	#print(xor_crypt_string(secret_data, encode = True))
	#print("The plain text fetched")
	#print(xor_crypt_string(xor_crypt_string(secret_data, encode = True), decode = True))

	str1 = "e86d2de2"
	print("Using string " + str1)
	bytes1 = bytes.fromhex(str1)
	int1 = int.from_bytes(bytes1, sys.byteorder)
	print(int1.to_bytes(len(bytes1), sys.byteorder).hex())
	int2 = toUnsignedInt(~int1, len(bytes1))
	print(int2.to_bytes(len(bytes1), sys.byteorder).hex())
	print(bytenot(bytes1).hex())
				
if __name__ == "__main__":
	main()