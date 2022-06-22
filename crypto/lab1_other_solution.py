from itertools import permutations
from collections import Counter

ct = [bytes.fromhex(x.strip()) for x in open('ciphers.txt')]
key = [Counter(c[i]^32 for c,d in permutations(ct, 2) if 96 < c[i]^d[i]|32 <= 122).most_common(1)[0][0] for i in range(len(ct[-1]))]   

print(''.join(chr(ct[-1][i]^key[i]) for i in range(len(ct[-1]))))