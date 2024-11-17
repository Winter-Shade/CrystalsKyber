from flask import Flask, render_template, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
