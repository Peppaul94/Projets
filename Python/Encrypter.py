from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from rsa_share import save_session_data
import binascii
import base64

keyPair = RSA.generate(3072)

def keyGenerator():
    pubKey = keyPair.publickey()
    pubKeyPEM = pubKey.exportKey()
    privKeyPEM = keyPair.exportKey()
    session_data['privKey'] = keyPair.exportKey().decode('utf-8')
    return pubKey

def encrypter(pubKey, file_path):
    print (f"Fichier à chiffré: "+file_path)
    with open(file_path, "rb") as f: #Ouvre le fichier en "bytes". Nécessaire pour chiffrer via rsa
        msg = f.read()
    encryptor = PKCS1_OAEP.new(pubKey)
    encrypted = encryptor.encrypt(msg)
    ciphertext_text = base64.b64encode(encrypted).decode("ascii")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ciphertext_text)
    session_data['encrypted'] = ciphertext_text
    #session_data['encrypted'] = binascii.hexlify(encrypted).decode('utf-8')
    print("Encrypted:", ciphertext_text)

session_data={}
pubKey=keyGenerator()
file_path = input("Entrez le fichier à chiffré (RSA): ")
encrypter(pubKey, file_path)
save_session_data(session_data)
