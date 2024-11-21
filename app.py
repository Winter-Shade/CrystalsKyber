# from flask import Flask, jsonify, request, render_template
import kyber
import ntruEncrypt
import os
# import DES
# import AES
from sympy import latex, Poly, symbols
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class Crystals:
    def __init__(self):
        self.publicKey, self.privateKey = kyber.generate_keys(kyber.params)

    def generateKeys(self):
        self.publicKey, self.privateKey = kyber.generate_keys(kyber.params)
        return (self.publicKey, self.privateKey)

    def returnKeys(self):
        return (self.publicKey, self.privateKey)
    
    def generateCiphertext(self, message):
        self.ciphertext = kyber.encrypt(self.publicKey, message, kyber.params)
        self.len_original_message = len(message)
        return self.ciphertext
    
    def decryptMessage(self):
        self.decrypted_message = kyber.decrypt(self.ciphertext, self.private_key, kyber.params)
        return self.decrypted_message

# Instantiate Crystals at the top level
crystals = Crystals()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/kyber')
def indexKyber():
    return render_template('index.html')



@app.route('/generate_keys', methods=['POST'])
def generate_keys():
    publicKey, privateKey = crystals.generateKeys()

    A_html = create_matrix_html(publicKey[0], 'A')
    t_html = create_matrix_html(publicKey[1], 't')
    s_html = create_matrix_html(privateKey, 's')

    return jsonify({"A_html": A_html, "t_html": t_html, "s_html": s_html})

@app.route('/generate_ciphertext', methods=['POST'])
def generate_ciphertext():
    data = request.get_json()
    binary_message = data.get('binaryMessage', '')

    publicKey = crystals.publicKey
    # Convert binary message to list of bits and encrypt
    message_list = [int(bit) for bit in binary_message]
    len_original_message = len(message_list)
    u, v = crystals.generateCiphertext(message_list)

    u_html = create_vector_html(u, 'u')
    # v_html = latex(v.as_expr())  # Converts v to LaTeX
    v_html = '<br>'.join([f"v : \\({latex(v.as_expr())}\\)"])

    return jsonify({"u_html": u_html, "v_html": v_html})



@app.route('/decrypt_message', methods=['POST'])
def decrypt_message():
    decrypted_message = kyber.decrypt(crystals.ciphertext, crystals.privateKey, kyber.params)
    message= decrypted_message.all_coeffs()
    output = ""
    if len(message)!=crystals.len_original_message:
        output += '0' * (crystals.len_original_message - len(message))
    
    output += ''.join(str(num) for num in message)
    message_html = f"Decrypted Message: {output}"
    return jsonify({"Message_html": message_html})


@app.route('/get_polynomial', methods=['GET'])
def get_polynomial():
    matrix = request.args.get('matrix')
    index = request.args.get('index')

    if matrix == 'A':
        i, j = int(index[0]), int(index[2])
        polynomial = crystals.publicKey[0][i][j]
    elif matrix == 't':
        i = int(index[0])
        polynomial = crystals.publicKey[1][i][0]
    elif matrix == 's':
        i = int(index[0])
        polynomial = crystals.privateKey[i][0]
    elif matrix == 'u':
        i = int(index[0])
        polynomial = crystals.ciphertext[0][i][0]
    elif matrix == 'v':
        polynomial = crystals.ciphertext[1]
    else:
        return jsonify({"error": "Invalid matrix name"}), 400

    polynomial_latex = latex(polynomial.as_expr())
    return jsonify({"polynomial": polynomial_latex})

# def create_matrix_html(matrix, name):
#     # Check if matrix is 3x1
#     if len(matrix[0]) == 1:
#         return '<br>'.join([f"{name}[{i},0]: {latex(matrix[i][0].as_expr())}" for i in range(3)])
#     # Assume 3x3 otherwise
#     return '<br>'.join([f"{name}[{i},{j}]: {latex(matrix[i][j].as_expr())}" for i in range(3) for j in range(3)])

# def create_vector_html(vector, name):
#     return '<br>'.join([f"{name}[{i}]: {latex(vector[i, 0].as_expr())}" for i in range(3)])

def create_matrix_html(matrix, name):
    if len(matrix[0]) == 1:
        return '<br>'.join([f"{name}[{i},0]: \\({latex(matrix[i][0].as_expr())}\\)" for i in range(3)])
    return '<br>'.join([f"{name}[{i},{j}]: \\({latex(matrix[i][j].as_expr())}\\)" for i in range(3) for j in range(3)])

def create_vector_html(vector, name):
    return '<br>'.join([f"{name}[{i}]: \\({latex(vector[i, 0].as_expr())}\\)" for i in range(3)])

@app.route('/ntru')
def ntruIndex():
    return render_template('ntru.html')

class NTRU:
    def __init__(self):
        self.x = symbols('x')
        self.N = 256
        self.p = 3
        self.q = 2048
        self.d = 3
        self.h, self.sk = ntruEncrypt.generate_keypair(self.N, self.p, self.q, self.d)
        self.publicKey, self.privateKey = Poly(self.h.coeffs, self.x), (Poly(self.sk[0].coeffs, self.x), Poly(self.sk[1].coeffs, self.x))


    def generateKeys(self):
        h, sk = ntruEncrypt.generate_keypair(self.N, self.p, self.q, self.d)
        self.publicKey, self.privateKey = Poly(self.h.coeffs, self.x), (Poly(self.sk[0].coeffs, self.x), Poly(self.sk[1].coeffs, self.x))

        return (self.publicKey, self.privateKey)

    def returnKeys(self):
        return (self.publicKey, self.privateKey)

    def generateCiphertext(self, message):
        message = ntruEncrypt.message_to_bits(message)
        message = ntruEncrypt.Zx(message)
        self.cptxt = ntruEncrypt.encrypt(message, self.h, self.N, self.q, self.d)
        self.ciphertext = Poly(ntruEncrypt.encrypt(message, self.h, self.N, self.q, self.d).coeffs, self.x)
        return self.ciphertext

    def decryptMessage(self):
        self.decrypted_message = ntruEncrypt.decrypt(self.cptxt, self.sk, self.N, self.p, self.q)
        self.decrypted_message = ntruEncrypt.bits_to_message(self.decrypted_message.coeffs)
        return self.decrypted_message

ntru = NTRU()

import json

x = symbols('x')
@app.route('/generate_ntru_keys', methods=['POST'])
def generate_ntru_keys():
    publicKey, privateKey = ntru.generateKeys()

    return jsonify({
        'public_key': latex(publicKey.as_expr()),  # Convert Poly object to string
        'private_key_0': latex(privateKey[0].as_expr()),
        'private_key_1': latex(privateKey[1].as_expr())
    })

@app.route('/generate_ntru_ciphertext', methods=['POST'])
def generate_ntru_ciphertext():
    data = request.get_json()
    message = data.get('textMessage', '')

    # Generate ciphertext as a polynomial
    ciphertext = ntru.generateCiphertext(message)

    # Convert ciphertext polynomial to a string compatible with LaTeX
    ciphertext_latex = latex(ciphertext.as_expr())  # Convert Python's power operator to LaTeX format

    return jsonify({"ciphertext": ciphertext_latex})


@app.route('/decrypt_ntru_message', methods=['POST'])
def decrypt_ntru_message():
    decrypted_message = ntru.decryptMessage()

    message_html = f"{decrypted_message}"
    return jsonify({"decryptedMessage": message_html})


@app.route('/DES')
def indexDES():
    return render_template('des3.html')


@app.route('/des3', methods=['GET', 'POST'])
def des3():
    result = None
    if request.method == 'POST':
        try:
            # Get form data
            rounds = int(request.form['rounds'])
            key_choice = request.form['keychoice']
            plaintext = request.form['plaintext']

            # Validate rounds
            if rounds not in {2, 3}:
                flash("Invalid choice! Only 2 or 3 rounds are allowed.", "error")
                return redirect(url_for('des3'))

            # Determine the required key length for DES3 (2 rounds = 16 bytes, 3 rounds = 24 bytes)
            keylen = 16 if rounds == 2 else 24

            # Handle key input or generation
            if key_choice == 'N':
                key = request.form['key'].encode()
                if len(key) != keylen:
                    flash(f"Invalid key length! Key must be {keylen} bytes. for {rounds}-round DES", "error")
                    return redirect(url_for('des3'))
            else:
                key = get_random_bytes(keylen)
                flash(f"Generated random key (hex): {key.hex()}", "info")

            # Generate IV
            iv = get_random_bytes(DES3.block_size)
            flash(f"Generated IV (hex): {iv.hex()}", "info")

            # Encrypt plaintext
            cipher = DES3.new(key, DES3.MODE_CBC, iv)
            padded_plaintext = pad(plaintext.encode(), DES3.block_size)
            ciphertext = cipher.encrypt(padded_plaintext)

            # Decrypt ciphertext to verify encryption
            decipher = DES3.new(key, DES3.MODE_CBC, iv)
            decrypted_padded_text = decipher.decrypt(ciphertext)
            decrypted_text = unpad(decrypted_padded_text, DES3.block_size)

            result = {
                "ciphertext": ciphertext.hex(),
                "decrypted_text": decrypted_text.decode('utf-8'),
                "key": key.hex(),
                "iv": iv.hex(),
            }
        except ValueError as ve:
            flash(f"Value error: {str(ve)}", "error")
            return redirect(url_for('des3'))
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", "error")
            return redirect(url_for('des3'))

        # Return with the result if POST is successful
        return render_template('des3.html', result=result)

    # Ensure a response for GET requests
    return render_template('des3.html')



def aes_encrypt_decrypt(keylen, keychoice, key_input, plaintext):
    key_bytes = keylen // 8

    if keychoice == 'N':
        key = key_input.encode()
        if len(key) != key_bytes:
            return "Invalid key length!"
    elif keychoice == 'Y':
        key = secrets.token_bytes(key_bytes)

    cipher = AES.new(key, AES.MODE_CBC)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)

    ciphertext = cipher.encrypt(padded_plaintext)

    iv = cipher.iv
    cipher_decrypt = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher_decrypt.decrypt(ciphertext)
    decrypted_data = unpad(decrypted_data, AES.block_size).decode()

    return {
        "key_hex": key.hex(),
        "iv_hex": iv.hex(),
        "ciphertext_hex": ciphertext.hex(),
        "decrypted_data": decrypted_data,
        "decrypted_data_hex": decrypted_data.encode().hex()
    }


@app.route('/AES', methods=['GET', 'POST'])
def indexAES():
    result = None
    if request.method == 'POST':
        keylen = int(request.form['keylen'])
        keychoice = request.form['keychoice']
        key_input = request.form['key_input']
        plaintext = request.form['plaintext']

        result = aes_encrypt_decrypt(keylen, keychoice, key_input, plaintext)
        if isinstance(result, dict):
            return render_template('aes.html', result=result)
        else:
            return render_template('aes.html', error=result)

    return render_template('aes.html')
@app.route('/Table',methods = ['GET','POST'])
def table():
    data = [
    {
        "Algorithm": "NTRU",
        "Type": "Asymmetric (Public-Key)",
        "Key Size": "1-2 KB (Public/Private)",
        "Ciphertext Size": "~1 KB",
        "Performance": "Moderate (All operations)",
        "Security Basis": "Lattice-based (Quantum-Secure)",
        "Quantum Resistance": "Yes",
        "Ciphertext Expansion": "High",
        "Bulk Data Suitability": "No (Inefficient)",
        "Typical Use Case": "Key exchange, Signatures",
        "Route": "/ntru"
    },
    {
        "Algorithm": "Kyber",
        "Type": "Asymmetric (Public-Key)",
        "Key Size": "1-2 KB (Public/Private)",
        "Ciphertext Size": "~800 B",
        "Performance": "Fast (All operations)",
        "Security Basis": "Lattice-based (Quantum-Secure)",
        "Quantum Resistance": "Yes",
        "Ciphertext Expansion": "Moderate",
        "Bulk Data Suitability": "No (Inefficient)",
        "Typical Use Case": "Key exchange, Encryption",
        "Route": "/kyber",
    },
    {
        "Algorithm": "AES",
        "Type": "Symmetric (Shared-Key)",
        "Key Size": "128, 192, or 256 bits",
        "Ciphertext Size": "Same as plaintext",
        "Performance": "Extremely fast",
        "Security Basis": "Substitution-permutation",
        "Quantum Resistance": "No",
        "Ciphertext Expansion": "None",
        "Bulk Data Suitability": "Yes",
        "Typical Use Case": "Encrypting large data",
        "Route": "/AES",
    },
    {
        "Algorithm": "DES",
        "Type": "Symmetric (Shared-Key)",
        "Key Size": "56 bits (Effective Key Size)",
        "Ciphertext Size": "Same as plaintext",
        "Performance": "Fast (But outdated)",
        "Security Basis": "Substitution-permutation",
        "Quantum Resistance": "No",
        "Ciphertext Expansion": "None",
        "Bulk Data Suitability": "No (Weak and Outdated)",
        "Typical Use Case": "Deprecated",
        "Route": "/DES",
    },
    ]
    return render_template("table.html", data=data)
    
if __name__ == '__main__':
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 8080))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)
