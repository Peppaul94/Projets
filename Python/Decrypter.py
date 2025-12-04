from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from rsa_share import load_session_data
import binascii
import base64

def menu():
    file_path = input("Please type the path of the file you'd like to decrypt: ")
    decrypted_file = input("Please type the name of the decrypted file: ")
    return file_path , decrypted_file

def decrypter(file_path,  decrypted_file):
    with open(file_path, "rb") as f:
        data = f.read()
    privKey = RSA.import_key(session_data['privKey'])
    ciphertext = base64.b64decode(data)
    decryptor = PKCS1_OAEP.new(privKey)
    plaintext = decryptor.decrypt(ciphertext)
    with open(file_path, "wb") as f:
        f.write(plaintext)
    print ("Decrypted message: ", plaintext)
    #encrypted = binascii.unhexlify(session_data['encrypted'])
    #decryptor = PKCS1_OAEP.new(privKey)
    #decrypted = decryptor.decrypt(encrypted)
    #print('Decrypted:', decrypted.decode('utf-8'))

fileOfUser=menu()
session_data = load_session_data()
#decrypter(file)
decrypter(fileOfUser[0], fileOfUser[1])
