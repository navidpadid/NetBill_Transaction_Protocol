import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
hash = "SHA-256"

def newkeys(keysize):
   random_generator = Random.new().read
   key = RSA.generate(keysize, random_generator)
   private, public = key, key.publickey()
   return public, private

def getpublickey(priv_key):
   return priv_key.publickey()

def encrypt(message, pub_key):
   cipher = PKCS1_OAEP.new(pub_key)
   return cipher.encrypt(message)

def decrypt(ciphertext, priv_key):
   cipher = PKCS1_OAEP.new(priv_key)
   return cipher.decrypt(ciphertext)

def sign(message, priv_key, hashAlg = "SHA-256"):
   global hash
   hash = hashAlg
   signer = PKCS1_v1_5.new(priv_key)
   
   if (hash == "SHA-512"):
      digest = SHA512.new()
   elif (hash == "SHA-384"):
      digest = SHA384.new()
   elif (hash == "SHA-256"):
      digest = SHA256.new()
   elif (hash == "SHA-1"):
      digest = SHA.new()
   else:
      digest = MD5.new()
   digest.update(message)
   return signer.sign(digest)

def verify(message, signature, pub_key):
   signer = PKCS1_v1_5.new(pub_key)
   if (hash == "SHA-512"):
      digest = SHA512.new()
   elif (hash == "SHA-384"):
      digest = SHA384.new()
   elif (hash == "SHA-256"):
      digest = SHA256.new()
   elif (hash == "SHA-1"):
      digest = SHA.new()
   else:
      digest = MD5.new()
   digest.update(message)
   return signer.verify(digest, signature)


def generate_pseudonyms(true_identity):
    ts = int(time.time()) // 1000 #validate for about quarter an hour 
    print("timestamp is: "+str(ts)+" which is validated for about quarter an hour\n")
    secret = "NavidRocks!"
    pseudonyms = str(true_identity)+"||"+str(ts) +"||"+str(secret)
    print("pseudonym is: "+ str(true_identity)+str(ts) +str(secret))
    
def newkeys(keysize):
   random_generator = Random.new().read
   key = RSA.generate(keysize, random_generator)
   private, public = key, key.publickey()
   return public, private    
    
def import_key(fileName):
    address = "./"+fileName+".pem"
    key = RSA.importKey(open(address, "rb").read())
    return key
    


def generate_pairKey_and_encrypt_with_serverPU(message,size=2048):
    pu, pv = newkeys(2048)
    print("Generated new RSA pair keys for you!\n")
    public = pu.exportKey('PEM').decode('ascii')
    print("Your public key is: \n")
    print(str(public)+"\n")
    print("Your private key is: \n")
    private = pv.exportKey('PEM').decode('ascii')
    print(private +"\n")
    encrypted_message = encrypt(str.encode(message),import_key("PU_ThePsuedoServer"))
    return encrypted_message, pu, pv 




message = "navid kheili khuuubeee! va AWli :D ksdjflasdlfkjdsalfjdskla sdfkjsdklfjs sdfkjsdkfjsdl"

encrypted_message, pu, pv = generate_pairKey_and_encrypt_with_serverPU(message) #remember the encrypted_message is bytes

signature = sign( encrypted_message,pv) #remember the signature is bytes

messege_encrypted_signed = [encrypted_message,signature,pu]

print(verify(messege_encrypted_signed[0],messege_encrypted_signed[1],pu))

decrypted = decrypt(messege_encrypted_signed[0],import_key("private_PseudoServer"))

decrypted_messege = decrypted.decode()

print(decrypted_messege)