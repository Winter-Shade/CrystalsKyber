from flask import Flask, render_template, request, redirect, url_for, flash
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/DES')
def index():
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


if __name__ == '__main__':
    app.run(debug=True)
