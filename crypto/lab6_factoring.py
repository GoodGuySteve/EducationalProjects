import gmpy2
from gmpy2 import mpfr, mpz, ceil, floor, c_div, c_mod, isqrt

def findLowerPrime(modulus, lowerBound):
	
	guess = lowerBound
	while guess < modulus:
		if c_mod(modulus, guess) == mpz('0'):
			return guess
		guess += 1

def checkPrimes(prime1, prime2, modulus):

	return prime1 * prime2 == modulus

def main():

	# Problem #1
	modulus1 = mpz('17976931348623159077293051907890247336179769789423065727343008115 \
	77326758055056206869853794492129829595855013875371640157101398586 \
	47833778606925583497541085196591615128057575940752635007475935288 \
	71082364994994077189561705436114947486504671101510156394068052754 \
	0071584560878577663743040086340742855278549092581')
	#modulus1 = mpz(31*37)
	
	#modulus1_float = mpfr(modulus1.digits())
	
	# Technically, this should be a ceiling function since it breaks when there is no
	# fractional remainder. However, because we're operating on primes, we will never 
	# run into a case where there isn't a fractional remainder
	average1 = mpz(isqrt(modulus1) + 1)
	
	#print("modulus: " + str(modulus1))
	#print("square root of modulus: " + str(average1))
	#print("difference of squares: " + str((average1 *  average1) - modulus1))
	#print("midpoint: " + str(isqrt((average1 * average1) - modulus1)))
	
	midpoint1 = mpz(isqrt((average1 * average1) - modulus1))
	
	lowPrime1 = average1 - midpoint1
	
	print("lowest prime: " + str(lowPrime1))
	print(checkPrimes(lowPrime1, c_div(modulus1, lowPrime1), modulus1))

	#ans1 = findLowerPrime(modulus1, lowerBound1)
	#print(ans1)

	return 0

if __name__ == "__main__":
	main()