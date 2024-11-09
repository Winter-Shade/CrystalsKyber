from flask import Flask, jsonify, request, render_template
import kyber
from sympy import latex, Poly

app = Flask(__name__)

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

# if __name__ == '__main__':
#     app.run(debug=True)
