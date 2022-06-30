import urllib3

http = urllib3.PoolManager(10)
TARGET = 'http://crypto-class.appspot.com/po?er='

def oracle(q):	#input hex text, returns status code
	target = TARGET + q                         # Create query URL
	r = http.request('GET', target)
	return r.status              # Valid pad if status = 404

ct = (
	'f20bdba6ff29eed7b046d1df9fb70000'
	'58b1ffb4210a580f748b4ac714c001bd'
	'4a61044426fb515dad3f21f18aa577c0'
	'bdf302936266926ff37dbf7035d5eeb4'	# All 4 blocks of PA4
)

print('Padding OK,  Message OK:\t',oracle(ct))

ct = (
	'f20bdba6ff29eed7b046d1df9fb70000'
	'58b1ffb4210a580f748b4ac714c001bd'
	'4a61044426fb515dad3f21f18aa577c0'
	'bdf302936266926ff37dbf7035d5eeb5' #<-------last byte altered
)

print('Message ??, Padding Bad:\t',oracle(ct))

ct = (
	'4a61044426fb515dad3f21f18aa577c0'
	'bdf302936266926ff37dbf7035d5eeb4'	# Last 2 blocks of PA4
)

print('Message bad, Padding OK:\t',oracle(ct))

ct = (
	'This is just messed up'	# This is not hex
)

print('Server says please use "hex":\t',oracle(ct))

ct = '123'				#this is almost hex, but not

print('Server says somethings wrong:\t',oracle(ct))