import gmpy2
from gmpy2 import mpfr, mpz, ceil, floor, c_div, f_div, c_mod, isqrt

# Given an average of the two primes and the modulus p*q, calculate the two 
# primes that make up the modulus and output them (smaller, larger).
def getPrimes(average, modulus):
	
	print("modulus: " + str(modulus))
	print("square root of modulus: " + str(average))
	print("difference of squares: " + str((average *  average) - modulus))
	print("midpoint: " + str(isqrt((average * average) - modulus)))
	
	midpoint = mpz(isqrt((average * average) - modulus))
	
	firstPrime = average - midpoint
	secondPrime = f_div(modulus, firstPrime)
	
	if (firstPrime > secondPrime):
		return (secondPrime, firstPrime)
	else:
		return (firstPrime, secondPrime)

def checkPrimes(prime1, prime2, modulus):

	return prime1 * prime2 == modulus


# Given the modulus and a lower bound for the prime average, guess until the
# two prime factors of the modulus are located
def findPrimes(modulus, lowerBound):
	
	guess = lowerBound
	while guess < modulus:
		(lowerTestPrime, higherTestPrime) = getPrimes(guess, modulus)
		if checkPrimes(lowerTestPrime, higherTestPrime, modulus):
			return (lowerTestPrime, higherTestPrime)
		guess += 1
		
def main():

	# Problem #1 ---------------------------------------
	modulus1 = mpz('17976931348623159077293051907890247336179769789423065727343008115 \
	77326758055056206869853794492129829595855013875371640157101398586 \
	47833778606925583497541085196591615128057575940752635007475935288 \
	71082364994994077189561705436114947486504671101510156394068052754 \
	0071584560878577663743040086340742855278549092581')
	
	# Technically, the +1 should be a ceiling function since it breaks when there is no
	# fractional remainder. However, because we're operating on primes, we will never 
	# run into a case where there isn't a fractional remainder
	average1 = mpz(isqrt(modulus1) + 1)
	
	(lowPrime1, highPrime1) = getPrimes(average1, modulus1)
	print("lowest prime #1: " + str(lowPrime1))
	print("higher prime #1: " + str(highPrime1))
	print("ans1 checks out: " + str(checkPrimes(lowPrime1, highPrime1, modulus1)))
	'''
	# Problem #2 ----------------------------------------------------
	modulus2 = mpz('6484558428080716696628242653467722787263437207069762630604390703787 \
	9730861808111646271401527606141756919558732184025452065542490671989 \
	2428844841839353281972988531310511738648965962582821502504990264452 \
	1008852816733037111422964210278402893076574586452336833570778346897 \
	15838646088239640236866252211790085787877')
	
	lowerBound2 = mpz(isqrt(modulus2) + 1)

	(lowPrime2, highPrime2) = findPrimes(modulus2, lowerBound2)
	print("lowest prime #2: " + str(lowPrime2))
	print("higher prime #2: " + str(highPrime2))
	print("ans2 checks out: " + str(checkPrimes(lowPrime2, highPrime2, modulus2)))'''
	
	# Problem #3 ----------------------------------------------------
	modulus3 = mpz('72006226374735042527956443552558373833808445147399984182665305798191 \
	63556901883377904234086641876639384851752649940178970835240791356868 \
	77441155132015188279331812309091996246361896836573643119174094961348 \
	52463970788523879939683923036467667022162701835329944324119217381272 \
	9276147530748597302192751375739387929')
	#modulus3 = mpz('2039652913367') # 1166083 * 1749149 - good for testing
	
	# We're attempting to solve for 3p * 2q, so the easiest method is to multiply the modulus
	# by 24 and then factor the 24 out later. This shifts our entire solution so that using the
	# square root to find the midpoint of this new system still works properly.
	newModulus3 = 24 * modulus3
	weightedAverage3 = mpz((isqrt(newModulus3) + 1))
		
	newAverage3 = weightedAverage3

	'''Debug output here should be:
	modulus: 12237917480202
	square root of modulus: 3789807 <- should be value of newAverage3
	difference of squares: 2124719617047
	midpoint: 1457641
	preliminary3 lowPrime: 2332166
	preliminary3 highPrime: 5247447
	'''
	
	(lowPrime3, highPrime3) = getPrimes(newAverage3, newModulus3)
	#(lowPrime3, highPrime3) = findPrimes(newModulus3, newAverage3)
	print("preliminary3 lowPrime: " + str(lowPrime3))
	print("preliminary3 highPrime: " + str(highPrime3))
	print("preliminary3 checks out: " + str(checkPrimes(lowPrime3, highPrime3, newModulus3)))
	
	# Since we calculated the primes around a modulus multiplied by 24, we need to divide the factors
	# back out.
	if (c_mod(lowPrime3, 6) == 0):
		lowPrime3 = c_div(lowPrime3, 6)
		highPrime3 = c_div(highPrime3, 4)
	else:
		lowPrime3 = c_div(lowPrime3, 4)
		highPrime3 = c_div(highPrime3, 6)
	if lowPrime3 > highPrime3:
		# Order changed from the division, so swap them back into order
		tmp = lowPrime3
		lowPrime3 = highPrime3
		highPrime3 = tmp
	
	print("lowest prime #3: " + str(lowPrime3))
	print("higher prime #3: " + str(highPrime3))
	print("ans3 checks out: " + str(checkPrimes(lowPrime3, highPrime3, modulus3)))
	
	

	return 0

if __name__ == "__main__":
	main()