import sympy as sym
from sympy import GF, symbols, Poly
import math
from random import randrange
from copy import deepcopy

class Zx:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def degree(self):
        return len(self.coeffs) - 1

    def add(self, other):
        result = deepcopy(self)
        for i in range(len(other.coeffs)):
            if i < len(result.coeffs):
                result.coeffs[i] += other.coeffs[i]
            else:
                result.coeffs.append(other.coeffs[i])
        return result

    def multiply(self, other):
        result = [0] * (len(self.coeffs) + len(other.coeffs) - 1)
        for i in range(len(self.coeffs)):
            for j in range(len(other.coeffs)):
                result[i + j] += self.coeffs[i] * other.coeffs[j]
        return Zx(result)

    def multiply_single_term(self, coeff, degree):
        result = deepcopy(self)
        result.coeffs = [c * coeff for c in result.coeffs]
        result.coeffs = [0] * degree + result.coeffs
        return result

    def randompoly(self, d, N):
        self.coeffs = [0] * N
        for _ in range(d):
            idx = randrange(N)
            self.coeffs[idx] = randrange(-1, 2, 2)  # Randomly assigns -1 or 1 to `d` terms.

def cyclic_convolution(F, G, N):
    result = F.multiply(G)
    t = Zx([0] * N)
    for i in range(len(result.coeffs)):
        t.coeffs[i % N] += result.coeffs[i]
    return t

def balancedmodulus(F, q, N):
    result = Zx([])
    for i in range(N):
        result.coeffs.append(((F.coeffs[i] + q // 2) % q) - q // 2)
    return result

def make_poly(coeffs):
    x = sym.Symbol('x')
    n = len(coeffs)
    coeffs = list(reversed(coeffs))
    poly = 0
    for i in range(n):
        poly += coeffs[i] * (x**i)
    return sym.poly(poly)

def invertmodprime(f, N, p):
    f_poly = make_poly(f.coeffs[::-1])
    x = sym.Symbol('x')
    inv_poly = sym.polys.polytools.invert(f_poly, x**N - 1, domain=GF(p, symmetric=False))
    inv_coeffs = inv_poly.all_coeffs()[::-1]
    return Zx(inv_coeffs)

def invertmodpowerof2(f, N, q):
    if not (q & (q - 1) == 0):  # Check if q is a power of 2
        raise ValueError("q must be a power of 2")
    g = invertmodprime(f, N, 2)
    while True:
        r = balancedmodulus(cyclic_convolution(f, g, N), q, N)
        if r.coeffs[0] == 1 and all(c == 0 for c in r.coeffs[1:]):
            break
        e = Zx([2])
        g = balancedmodulus(cyclic_convolution(g, e.add(r.multiply_single_term(-1, 0)), N), q, N)
    return g

def generate_small_poly(d, N, p, q):
    while True:
        try:
            f = Zx([])
            f.randompoly(d, N)
            invertmodprime(f, N, p)
            invertmodpowerof2(f, N, q)
            return f
        except Exception:
            continue

def generate_keypair(N, p, q, d):
    while True:
        try:
            f = generate_small_poly(d, N, p, q)
            f_p_inv = invertmodprime(f, N, p)
            f_q_inv = invertmodpowerof2(f, N, q)

            g = Zx([])
            g.randompoly(d, N)

            h = balancedmodulus(cyclic_convolution(f_q_inv, g, N).multiply_single_term(p, 0), q, N)
            return h, (f, f_p_inv)
        except Exception as e:
            print(f"Key generation error: {e}")
            continue

def encrypt(m, h, N, q, d):
    r = Zx([])
    r.randompoly(d, N)
    return balancedmodulus(cyclic_convolution(h, r, N).add(m), q, N)

def decrypt(c, sk, N, p, q):
    f, f_p_inv = sk
    a = balancedmodulus(cyclic_convolution(c, f, N), q, N)
    return balancedmodulus(cyclic_convolution(a, f_p_inv, N), p, N)


def message_to_bits(message):
    """
    Converts a string message into a list of binary bits (coefficients).
    
    Args:
        message (str): The input message as a string.

    Returns:
        list: A list of binary bits representing the message.
    """
    # Convert each character into its ASCII value and then to binary
    bits_list = []
    for char in message:
        ascii_value = ord(char)  # ASCII value of the character
        binary_representation = f"{ascii_value:08b}"  # Convert to an 8-bit binary string
        bits_list.extend([int(bit) for bit in binary_representation])  # Add bits to the list

    return bits_list


# Example usage
# message = "Cryptography is great, isn't it gonna be greater than 256"
# bits = message_to_bits(message)
# print("Message:", message)
# print("Bits:", bits)
# print(len(bits))


def bits_to_message(bits):
    """
    Converts a list of binary bits (coefficients) back into a string message.
    
    Args:
        bits (list): A list of binary bits representing the message.
    
    Returns:
        str: The original message as a string.
    """
    # Group the bits into 8-bit chunks, each representing a character
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]  # Extract the next 8 bits
        ascii_value = int("".join(map(str, byte)), 2)  # Convert the 8 bits to an integer (ASCII)
        chars.append(chr(ascii_value))  # Convert the ASCII value back to a character

    return ''.join(chars)





# Parameters
N = 256  # Degree of polynomial
p = 3   # Small modulus
q = 2048  # Large modulus (power of 2)
d = 3   # Number of non-zero coefficients

# Generate keys
h, sk = generate_keypair(N, p, q, d)

# Example message (small polynomial)
m = input('Enter your message: ')
m = message_to_bits(m)
m = Zx(m)

# Encrypt and decrypt
c = encrypt(m, h, N, q, d)
decrypted_m = decrypt(c, sk, N, p, q)

x = symbols('x')
# Verify
# print(Poly(m.coeffs, x))
print("Decrypted message:", decrypted_m.coeffs)
dm = bits_to_message(decrypted_m.coeffs)
print(dm)
