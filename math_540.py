# computes the gcd of two numbers by means of Euclid's algorithm
def gcd(a,b,to_print=False):
    if a == 0 and b == 0: return 0
    elif a == 0: return b
    elif b == 0: return a
    if not (a >= b):
        b,a=a,b
    r=[a,b]
    going = True
    while going: 
        r.append(r[len(r)-2]%r[len(r)-1])
        x1=r[len(r)-3]
        x2=r[len(r)-2]
        x3=r[len(r)-1]
        c=x1//x2
        if to_print: print(str(x1) + " = " + str(c) + "*" + str(x2) + " + " + str(x3))
        going = (x1%x2) != 0
    if to_print: print("gcd("+str(a)+","+str(b)+')='+str(x2))
    return x2

# determines whether a number is prime
def isPrime(n):
    if n<2: return False
    for i in range(2,int(n**.5+1)):
        if n%i==0: return False
    return True

# finds the prime factorization of a number
def prime_factorization(a):
    if not (a%1==0): return
    prime_factors = []
    for i in range(int(a*.5)+1):
        if isPrime(i):
            while a%i == 0:
                prime_factors.append(i)
                a=int(a/i)
        if a == 1: return [1]+prime_factors
    if not prime_factors:
        return [1,a]

pf = prime_factorization

# finds the factorization of a number
def factorization(a):
    if a == 0: return set([0])
    if not (a%1==0): return
    factors = set()
    for i in range(1,int(a*.5)+1):
        modulo = a%i
        if modulo == 0:
            factors.add(i)
    if not factors:
        factors = list(set([1,a]))
    else:
        factors.add(a)
        factors = list(factors)
    factors.sort()
    return factors

f = factorization


# Euler's phi function. Finds the number of numbers less than a number 
# that are coprime with the number. IE, # of a<n such that gcd(a,n) = 1
def euler_phi(n):
    number_of_coprime=0
    for i in range(n):
        if gcd(i,n,False)==1: number_of_coprime +=1
    return number_of_coprime

phi=euler_phi

# finds the multiplicative inverse of a number n mod m
def modular_inverse(n,m):
    for i in range(1,m+1):
        product = n*i
        if product % m == 1:
            return i
    print("no solution")

# prints a table of the phi function values
def phi_seq(n=-1):
    i = 1
    while True:
        input("phi("+str(i)+"): " + str(phi(i)))
        i+=1
        if n!=-1:
            if i == n: return

# creates a list of numbers less than n 
# relatively prime to n
def relative_primes(n):
    list_of_rps=[]
    for i in range(n):
        if gcd(i,n,False)==1:
            list_of_rps.append(i)
    return list_of_rps

rps = relative_primes

# prints a table of the sum of the numbers less than n 
# that are relatively prime to n
def rp_seq(n):
    for i in range(n,printAll=True):
        if printAll: print("sum of relatively prime to ("+str(i)+"): " + str(rps(i)))
        else: input("sum of relatively prime to ("+str(i)+"): " + str(rps(i)))

# finds the order of a number a modulo n
# returns k where a^k ≡ 1 (mod n)
def modular_order(a,n,to_print=True):
    if a == n: 
        if to_print: return print("ord of " + str(a) + " (mod " + str(n)+") is: 0")
        else: return 0
    for i in range(1,n):
        if a**i % n == 1:
            if to_print: return print("ord of " + str(a) + " (mod " + str(n)+") is: "+ str(i))
            else: return i

ord = modular_order

# a is a primitive root of n if when you take powers, 
# a^k such that k>1 and k<n, the number of unique 
# answers you get (mod n) is equal to phi(n). that is, 
# there is a unique value modulo n for each coprime < n
def find_primitive_root(n,to_print=True):
    r = 2
    found = False
    while not found:
        residues = set()
        for i in range(0,n):
            x = r**i%n
            residues.add(x)
            if len(residues)== phi(n): 
                if to_print: return print(str(r) +" is a primitive root of "+str(n))
                else: return r
        r+=1

pr = find_primitive_root









