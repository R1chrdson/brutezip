import itertools

# Returns number of passswords checked
def bruteforce(length, maximal, symbols, z, isprint=True, regular=True):
    counter = 0
    
    if length > maximal:
        print('', end='\r')
        return counter

    generator = itertools.product(symbols, repeat=length)
    for guess in generator:
        if regular:
            counter += 1
        guess = ''.join(guess)
        if isprint:
                print("\rStatus: {}".format(guess), end="", flush=True)
        if checkpass(z, bytes(guess, 'utf-8')):
            if regular:
                print('', end='\r')
                print('The password is:', guess)
            return counter
    counter += bruteforce(length + 1, maximal, symbols, z, isprint)
    return counter

def checkpass(z, password):
    try:
        z.read(z.namelist()[0], pwd=password)
        return True
    except:
        return False


# Calculates number of checks before brute force method will get this password
# The formula is: 
# number = d**1 + d**2 + ... + d**l-1 + (d**l-1 )*s[p[0]] + (d**l-2)*s[p[1]] + ... + (d**0)*s[p[l-1]]
# where s - aplhabet, d - len of aplhabet, p - password, l - len of password
def calculate(password, symbols):
    l = len(password)
    d = len(symbols)
    result = 1
    for i in range(1, l):
        result += d**i
    for i in range(l - 1, -1, -1):
        result += (d**i)*symbols.find(password[0])
        password = password[1:]
    return result
