import argparse
import string
import zipfile
from time import time
from collections import OrderedDict

import bruteforce

def main():
    # Create arguments parser
    parser = argparse.ArgumentParser(
        description='Program which helps to crack zip passwords by bruteforce', 
        epilog='Default symbols set is all lowercase and uppercase letter and digits')
    parser.add_argument('filename', 
        help='Name of zip file to crack')
    parser.add_argument('-min', type=int, default=1, nargs='?', 
        help='Minimal length of password (default = 1)')
    parser.add_argument('-max', type=int, default=6,  nargs='?', 
        help='Maximal length of password (default = 6)')
    parser.add_argument('-l', '--lower', action='store_true', 
        help='Includes lowercase alphabet symbols')
    parser.add_argument('-u', '--upper', action='store_true', 
        help='Includes uppercase alphabet symbols')
    parser.add_argument('-d', '--digits', action='store_true', 
        help='Includes numerical symbols')
    parser.add_argument('-s', '--special', action='store_true', 
        help='Includes special symbols')
    parser.add_argument('-b', '--bar', default=True, action='store_false',
        help='Disable statusbar')
    parser.add_argument('-e', '--estimate', type=str, nargs='?',
        help='Check entered password and calculate number of password checked to bruteforce it. If you\'re using special symbols or spaces, please wrap your password by \' \' for instance: \'password\'')
    args = parser.parse_args()

    try:
        z = zipfile.ZipFile(args.filename, 'r')
    except:
        print('Wrong filename')
        exit(1)

    # Create alphabet for brute force method
    symbols = ''
    if args.lower:
        symbols += string.ascii_lowercase
    if args.upper:
        symbols += string.ascii_uppercase
    if args.digits:
        symbols += string.digits
    if args.special:
        symbols += string.punctuation
    if len(symbols) == 0:
        symbols += string.ascii_letters + string.digits

    combinationNumber = 0
    for i in range(args.min, args.max + 1):
        combinationNumber += len(symbols)**i
    print('Number of possible password combinations is:', combinationNumber, end='\n\n')


    if args.estimate:
        for char in args.estimate:
            if char not in symbols:
                print('Wrong set of symbols')
                exit(0)
        symbols = ''.join(OrderedDict.fromkeys(symbols))
        print('{} password'.format(('Incorrect', 'Correct')[bruteforce.checkpass(z, bytes(args.estimate, 'utf8'))]))
        checked = bruteforce.calculate(args.estimate, symbols)
        print('Number of passwords need to bruteforce it:', checked)
        args.max = 1
        start = time()
        bruteforce.bruteforce(1, 1, symbols, z, args.bar, False)
        end = time()
        speed = len(symbols)/(end-start)
        print('Average speed is', str(round(speed, 2)) + 'p/s')
        print('\nTime needed to bruteforce it: ', str(round(checked/speed, 2)) + 's')
        exit(1)
    else:
        if(int(args.min) > int(args.max)):
            print('-min should be less than -max')
            exit(1)

    start = time()
    counter = bruteforce.bruteforce(args.min, args.max, symbols, z, args.bar)
    end = time()
    if counter != combinationNumber:
        print('Number of passwords checked:', counter)
        print('Average speed:', str(round((counter/(end-start)), 2)) + 'p/s', end='\n\n')
    else:
        print('Password not found')
    print('Time elapsed:', str(round((end-start), 2)) + 's')

if __name__ == '__main__':
    main()