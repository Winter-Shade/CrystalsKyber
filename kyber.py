# import streamlit as st
import numpy as np
from sympy import symbols, Poly, latex
import math
import random

# Define the polynomial variable
x = symbols('x')

class LatticeParameters:
    def __init__(self, n, k, q):
        self.n = n  # Polynomial degree
        self.k = k  # Number of polynomials in matrix
        self.q = q  # Modulus for coefficients

# Initialize lattice parameters
n, k, q = 256, 3, 3329
params = LatticeParameters(n=n, k=k, q=q)
poly_modulus = Poly(x ** n + 1, x)


def ensure_non_negative_coefficients(poly, q):
    coeffs = poly.all_coeffs()
    adjusted_coeffs = [(c + q) if c < 0 else c for c in coeffs]
    return Poly(adjusted_coeffs, poly.gen)

def symmetric_mod(r, q):
    return abs(r) if r <= q / 2 else abs(r - q)

def round_q(x, q):
    x_dash = symmetric_mod(x, q)
    return 0 if math.floor(q / 4) > x_dash > math.ceil(-q / 4) else 1

def round_q_poly(f, q):
    coeffs = f.all_coeffs()
    rounded_coeffs = [round_q(c, q) for c in coeffs]
    return Poly(rounded_coeffs, x)

def generate_small_poly(eta, q, n):
    possible_coeffs = np.concatenate((np.arange(0, eta + 1), np.arange(q - eta, q)))
    coeffs = np.random.choice(possible_coeffs, n, replace=True)
    return Poly(coeffs, x)

def generate_matrix_A(n, q, k):
    A = np.empty((k, k), dtype=object)
    for i in range(k):
        for j in range(k):
            coeffs = np.random.randint(0, q, n)
            A[i][j] = Poly(coeffs, x)
    return A


def generate_keys(params):
    A = generate_matrix_A(params.n, params.q, params.k)
    s = np.array([generate_small_poly(2, params.q, params.n) for _ in range(params.k)]).reshape((params.k, 1))
    e = np.array([generate_small_poly(2, params.q, params.n) for _ in range(params.k)]).reshape((params.k, 1))

    t = A.dot(s) + e
    for i in range(params.k):
        t[i][0] = ensure_non_negative_coefficients(t[i][0].rem(poly_modulus).set_modulus(params.q), params.q)

    public_key = [A, t]
    private_key = s
    return public_key, private_key

def encrypt(public_key, message, params):
    A, t = public_key
    r = np.array([generate_small_poly(2, params.q, params.n) for _ in range(params.k)]).reshape((params.k, 1))
    e1 = np.array([generate_small_poly(2, params.q, params.n) for _ in range(params.k)]).reshape((params.k, 1))
    e2 = generate_small_poly(2, params.q, params.n)

    u = A.transpose().dot(r) + e1
    for i in range(params.k):
        u[i][0] = ensure_non_negative_coefficients(u[i][0].rem(poly_modulus).set_modulus(params.q), params.q)

    m = Poly(message, x)
    v = ((t.transpose()).dot(r) + e2 + (params.q // 2) * m)[0][0]
    v = ensure_non_negative_coefficients(v.rem(poly_modulus).set_modulus(params.q), params.q)

    return [u, v]

def decrypt(ciphertext, private_key, params):
    u, v = ciphertext
    s = private_key
    decryption = (v - (s.transpose().dot(u))[0][0])
    decryption = decryption.rem(poly_modulus).set_modulus(params.q)
    return round_q_poly(decryption, params.q)

### STREAMLIT APP ###

# st.title("Kyber-PKE")

# st.header("Message Input")
# message_input = st.text_input("Enter a binary message (e.g., 1010...):", "")
# message_input = '010111'
# if st.button("Generate Keys"):
# public_key, private_key = generate_keys(params)
# A, t = public_key
# A = latex(A[0][0])
# print(A)
#     st.session_state.public_key = public_key
#     st.session_state.private_key = private_key
#     st.success("Keys generated successfully!")

# if "public_key" in st.session_state and message_input:
#     if st.button("Encrypt"):
# message_list = [int(bit) for bit in message_input]
# ciphertext = encrypt(public_key, message_list, params)
# print(latex(ciphertext[1]))
#         st.session_state.ciphertext = ciphertext
#         st.write("Ciphertext:", ciphertext)

# if "ciphertext" in st.session_state:
#     if st.button("Decrypt"):
#         decrypted_message = decrypt(st.session_state.ciphertext, st.session_state.private_key, params)
#         st.write("Decrypted Message:", decrypted_message.all_coeffs())
