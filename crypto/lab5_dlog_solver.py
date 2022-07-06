import gmpy2
from gmpy2 import mpz

# Calculates the log of the given base on arg over the given prime modulus
def dlog(base, arg, modulus):
	# Using algebra, we change arg = exp(base, x) to arg = exp(base, x0*B + x1),
	# where B is the halfway point in our search space
	# A 40-bit search space makes B 20 bits
	midpoint = mpz('1') << 20
	#print(midpoint.digits())
	
	# This now lets us transform the equation to arg / exp(base, x1) = exp(exp(base, B) x0)
	# where x0 and x1 are both less than B. This dramatically reduces our search space and
	# number of multiplications needed

	# First, we generate a hash table mapping each solution of the left side of the equation
	# to its value of x1.
	xValues = {}
	for x1 in range(0, midpoint + 1):
		# left side: arg / exp(base, x1)
		val = gmpy2.divm(arg, pow(base, x1, modulus), modulus)
		xValues[val] = x1
	
	print("Table created.")
	
	# Then we check which values of the right side match the left side. This can be done
	# with a multiply and then a lookup to find values for x0 and x1
	baseToB = pow(base, midpoint, modulus)
	for x0 in range(0, midpoint + 1):
		val = pow(baseToB, x0, modulus)
		if (val in xValues):
			x1 = xValues[val]
			print("Found match for " + str(x0) + ", " + str(x1))
			break

	# Final solution: x = x0*B + x1
	return (x0 * midpoint + x1) % modulus

def main():

	primeModulus = mpz('13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171')
	logBase = mpz('11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568')
	logArg = mpz('3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333')

	answer = dlog(logBase, logArg, primeModulus)

	print(answer.digits())

	return 0

if __name__ == "__main__":
	main()