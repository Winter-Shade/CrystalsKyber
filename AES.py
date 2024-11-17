from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import secrets
def print_binary(data):
    return data.hex()
keylen = int(input("Choose AES type (128, 192, 256): "))
if keylen not in {128, 192, 256}:
    print(f"Invalid Key length | {{{keylen}}} is not valid")
    exit()
key_bytes = keylen//8
keychoice = input("Enter 'Y' to choose random key and 'N' to give key as input: ")
if keychoice == 'N':
    key = input(f"Enter Key({keylen}-bits/{key_bytes}-bytes) {key_bytes} charecters: ").encode()
    if len(key) != key_bytes:
        print("Invalid key! Try Again")
        exit()
elif keychoice == 'Y':
    key = secrets.token_bytes(key_bytes)
    print(f"Random {keylen}-bits key(in hex): ",key.hex())
plaintext = input("Enter plaintext: ").encode()

cipher = AES.new(key, AES.MODE_CBC) 

padded_plaintext = pad(plaintext, AES.block_size)

print("Initial Padded Plaintext (in hex):")
print(print_binary(padded_plaintext))

ciphertext = cipher.encrypt(padded_plaintext)
print("\nCiphertext (in hex):")
print(ciphertext.hex())

iv = cipher.iv
cipher_decrypt = AES.new(key, AES.MODE_CBC, iv)

decrypted_data = cipher_decrypt.decrypt(ciphertext)
decrypted_data = unpad(decrypted_data, AES.block_size)

print("\nDecrypted Data:")
print(decrypted_data.decode())
print("Decrypted Data (in hex):")
print(print_binary(decrypted_data))
