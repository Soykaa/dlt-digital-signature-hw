import argparse
import random
from typing import Tuple

from sympy import gcd, mod_inverse, randprime


def generate_prime(n: int = 1024) -> int:
    """ Generates random [big enough] prime number. """
    return randprime(2 ** (n - 1), 2 ** n - 1)


def get_coprime_num(num: int) -> int:
    """ Calculates the coprime for the given number. """
    coprime_num = random.randint(2, num - 1)
    while gcd(coprime_num, num) != 1:
        coprime_num = random.randint(2, num - 1)
    return coprime_num


def generate_keypair() -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """ Calculates a pair of keys: public & private. """
    p = generate_prime()
    q = generate_prime()
    n = p * q
    m = (p - 1) * (q - 1)
    e = get_coprime_num(m)
    d = mod_inverse(e, m)
    return (e, n), (d, n)


def encrypt(msg: str, pub_key: Tuple[int, int]) -> int:
    """ Encrypts the message using the given public key. """
    e, n = pub_key
    return pow(int(msg), e, n)


def decrypt(enc_msg: int, prt_key: Tuple[int, int]) -> str:
    """ Decrypts the encrypted message using the given private key. """
    d, n = prt_key
    return str(pow(enc_msg, d, n))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RSA algorithm')
    parser.add_argument('-i', '--input', type=str, help='Path to input file')
    parser.add_argument('-o', '--output', type=str, help='Path to output file')
    parser.add_argument('-l', '--logs', action='store_true', help='Logs')
    args = parser.parse_args()
    with open(args.input, 'r') as input_file:
        message = input_file.read()
    public_key, private_key = generate_keypair()
    encrypted_text = encrypt(message, public_key)
    decrypted_text = decrypt(encrypted_text, private_key)
    assert (message == decrypted_text)
    with open(args.output, 'w') as output_file:
        output_file.write(decrypted_text)
    if args.logs:
        print(f'original: {message}')
        print(f'encrypted: {encrypted_text}')
        print(f'decrypted: {decrypted_text}')
