# import key pieces from bottle package
import random
import time

from bottle import route, run, static_file
# import os for reading environment variables
import os
import math


def get_number_of_prime_bits():
    return int(os.environ.get('N_BITS', '40'))

def get_search_time():
    return int(os.environ.get('SEARCH_TIME', '2'))

def get_static_root():
    """
    Return root directory for static content
    """
    return os.environ.get('STATIC_CONTENT_ROOT', '/opt/app-root/src/static')


@route('/')
def root_page():
    """
    Route for root path, just try to return index.html
    """
    return static_file('/index.html', get_static_root())


@route('/static/<path:path>')
def server_static(path):
    """
    Any path not defined more specifically is handled as static content
    """
    return static_file(path, get_static_root())


@route('/healthz')
def health():
    """
    Status endpoint for health checks
    """
    return 'OK'


@route('/api/v1/primes')
def primes():
    # code from https://stackoverflow.com/questions/4114167/
    def is_prime(n):
        if n == 2:
            return True
        if n % 2 == 0 or n <= 1:
            return False

        sqr = int(math.sqrt(n)) + 1

        for divisor in range(3, sqr, 2):
            if n % divisor == 0:
                return False
        return True

    end_ts = time.time() + get_search_time()
    primes = []
    while time.time() < end_ts:
        n = random.getrandbits(get_number_of_prime_bits())
        if is_prime(n):
            primes.append(n)
    primes.sort()
    msg = 'Found %d primes for you: %s' % (len(primes), primes)
    print(msg)
    return msg


if __name__ == '__main__':
    # Here we simply start the server process
    run(host='0.0.0.0', port=8080, reloader=True)
