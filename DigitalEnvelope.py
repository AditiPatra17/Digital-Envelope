#Digital Envelope

import random

print("Aditi Patra 21BIT0125")

# Key Generation
def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)  # Start from 2 instead of phi
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)  # Start from 2 instead of phi

    d = modular_inverse(e, phi)

    return ((e, n), (d, n))

# Transfer Encrypted Message to Digital Envelope (Creation of Digital Envelope)
def encrypt(message, public_key):
    e, n = public_key
    encrypted_msg = pow(message, e, n)
    return encrypted_msg

def decrypt(encrypted_msg, private_key):
    d, n = private_key
    decrypted_msg = pow(encrypted_msg, d, n)
    return decrypted_msg

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

def modular_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd == 1:
        return x % m
    else:
        raise ValueError("Modular inverse does not exist.")

# Check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

# Take input for p and q, ensure they are prime numbers
p = int(input("Enter a prime number for p: "))
while not is_prime(p):
    p = int(input("Invalid input. Enter a prime number for p: "))

q = int(input("Enter a prime number for q: "))
while not is_prime(q):
    q = int(input("Invalid input. Enter a prime number for q: "))

public_key, private_key = generate_keypair(p, q)

m = int(input("Enter a number as the message: "))

# Generate random symmetric key
k = random.randint(2**2048, 2**4096)  # Generate a random key between 2 and n-1

# Encrypt the message using the public key
ct1 = encrypt(m, public_key)

# Encrypt the symmetric key using the public key
r = pow(k, public_key[0], public_key[1])
ct2 = encrypt(r, public_key)

# Store ct1 in a file
with open("ct1.txt", "w") as file:
    file.write(str(ct1))

# Store ct2 in a file
with open("ct2.txt", "w") as file:
    file.write(str(ct2))
    
# Decrypt the symmetric key using the private key
dec = decrypt(ct2, private_key)

# Obtain the original message by decrypting ct1 with dec
nm = decrypt(ct1, private_key)

print("Symmetric Key (k):", k)
print("Encrypted Symmetric Key (r):", r)
print("Encrypted Message (ct1):", ct1)
print("Decrypted Symmetric Key:", dec)
print("Decrypted Message (nm):", nm)
