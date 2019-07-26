import subprocess
import time

#for RSA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
hash = "SHA-256"

#for symmetric encryption
from cryptography.fernet import Fernet
from ast import literal_eval


#KERBEROS FUNCTIONS

def add_new_princ(flag_pseudonym, idName):
    print("first enter your admin pass ( sudo pass ), after that follow the procedure bellow...\n")
    if (flag_pseudonym):
        print("1) please type \033[1;34;40m addprinc "+str(idName)+" \033[0;0m \n")
    else:
        print("1) please type \033[1;34;40m addprinc "+str(idName)+" \033[0;0m \n")
        
    print("2) enter your desired password \033[0;0m\n")
    print("3) type:  \033[1;34;40m exit \033[0;0m \n")
    subprocess.call(['sudo','kadmin.local'])
    print("\n")
    print("added your pseudonym to kerberos!\n")
    return
    
def has_kerberos_ticket(address):
	#address = "/tmp/"+ str(username)+".ticket"
	return True if subprocess.call(['klist', '-c', address]) == 0 else False


def validate_ticket(address):
	if (has_kerberos_ticket(address)):
		print("ticket  \033[1;32;40m validated \033[0;0m \n")
	else:
		print("ticket:  \033[1;31;40m NOT validated \033[0;0m \n")


def get_ticket_from_kerberos(flag_pseudonym):
    if (flag_pseudonym):
        username = input("enter your kerberos pseudonym:  ")
    else:
        username = input("enter your kerberos username:  ")
    print("ticket for username:" +str(username)+"\n")
    address="/tmp/"+str(username)+".ticket"
    subprocess.call(["kinit","-c", address, username])
    print("")
    print("ticket generated in:  " + address)
    return address
    #validate_ticket(username)
    #print("username is \033[1;32;40m" + extract_username_from_ticket(username)+"\033[0;0m \n")

def extract_username_from_ticket(address):
	print("\n")
	print("Extracting username from ticket")
	#address = "/tmp/"+ str(username)+".ticket"
	#address = "/home/nubuntu/projectGitRepo/Navid/navidFiles/reza.ticket"
	extractedFile = "/tmp/"+str(address)+"EX.txt"

	cmd = "klist -c "+address+">"+extractedFile
	ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output = ps.communicate()[0]
	process_file = open(extractedFile,'r')
	to_process = process_file.readlines()
	splitedone = to_process[1].split('Default principal: ')
	splitedFinal = splitedone[1].split('@')
	usernameExtracted = splitedFinal[0]
	return usernameExtracted

#File with symmetric_encryption functions
def fileToData(file_address):
    input_file = file_address
    with open(input_file, 'rb') as f:
        data = f.read()
    return data

def dataToFile(data,name):
    output_file = name
    with open(output_file, 'wb') as f:
        f.write(data)
    return
    
    
    
#RSA FUNCTIONS    
    
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


#symmetric_encryption FUNCTIONS    
def symmetric_key_generator(symmetric_key_Name):
    print("Generating symmetric key:  " + symmetric_key_Name+".key in file")
    symmetric_key = Fernet.generate_key()
    file = open(symmetric_key_Name+'.key', 'wb')
    file.write(symmetric_key)
    file.close()
    print("Your symmetric key K1 is:  "+ str(symmetric_key))
    return
    
def fetchSymmetricKey(symmetric_key_Name):
    with open(symmetric_key_Name+'.key') as file:
        symmetric_key = bytes(file.read(), "utf-8")
    return Fernet(symmetric_key)

def fetchSymmetricKey_plain(symmetric_key_Name):
    with open(symmetric_key_Name+'.key') as file:
        symmetric_key = bytes(file.read(), "utf-8")
    return symmetric_key

def symmetric_encryption(symmetric_key_Name,message):
    fernet_key = fetchSymmetricKey(symmetric_key_Name)
    message_to_encrypt = message.encode()
    encrypted_message = fernet_key.encrypt(message_to_encrypt)
    return encrypted_message

def symmetric_decryption(symmetric_key_Name,encrypted_message):
    fernet_key = fetchSymmetricKey(symmetric_key_Name)
    return fernet_key.decrypt(encrypted_message)

    
#RSA KEYs FUNCTIONS
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

def generate_pseudonyms_to_verify(true_identity):
    ts = int(time.time()) // 1000 #validate for about quarter an hour 
    print("\n")
    print("timestamp is:"+str(ts)+" which is validated for about quarter an hour\n")
    time.sleep(1.5)
    K1 = symmetric_key_generator("K1")
    K1 = str(fetchSymmetricKey_plain("K1"))
    pseudonyms = str(true_identity)+str(ts)+K1+"MerchantID"
    print("pseudonym is:  "+str(true_identity)+str(ts)+K1+"MerchantID")
    return pseudonyms

def generate_pseudonyms_withK2(true_identity):
    ts = int(time.time()) // 1000 #validate for about quarter an hour 
    print("\n")
    time.sleep(1.5)
    K2 = str(fetchSymmetricKey_plain("K2"))
    pseudonyms = str(true_identity)+str(ts)+K2+"MerchantID"
    return pseudonyms

def generate_pseudonyms_withOutK(true_identity):
    ts = int(time.time()) // 1000 #validate for about quarter an hour 
    print("\n")
    time.sleep(1.5)
    pseudonyms = str(true_identity)+str(ts)+"MerchantID"
    return pseudonyms

def generate_pseudonyms_for_serverPhase2(true_identity):
    ts = int(time.time()) // 1000 #validate for about quarter an hour 
    print("\n")
    K1 = fetchSymmetricKey_plain("K1")
    K1 = str(K1)
    pseudonyms = str(true_identity)+str(ts)+K1+"MerchantID"
    print("pseudonym by server is:  "+str(true_identity)+str(ts)+K1+"MerchantID")
    time.sleep(1.5)
    return pseudonyms

#PSEUDONYM HANDLING
def generate_pseudonyms(true_identity):
    message = generate_pseudonyms_to_verify(true_identity)
    
    encrypted_message, pu, pv = generate_pairKey_and_encrypt_with_serverPU(message) #remember the encrypted_message is bytes

    signature = sign( encrypted_message,pv) #remember the signature is bytes

    messege_encrypted_signed = [encrypted_message,signature,pu]

    print("Encrypted message ready for pseudonym verfication!\n")
    time.sleep(1.5)
    
    return messege_encrypted_signed,pu,pv

def pseudonym_verification_server(messege_encrypted_signed,pu,true_identity):
    print("verification process for encrypted pseudonym started...\n")
    signature_validation_result = verify(messege_encrypted_signed[0],messege_encrypted_signed[1],pu)
    
    time.sleep(1.5)

    if (signature_validation_result):
        print("the signature validation result:  "+"\033[1;32;40m validated \033[0;0m \n")
    else: 
        print("the signature validation result:  "+"\033[1;31;40m NOT validated \033[0;0m \n")

    decrypted = decrypt(messege_encrypted_signed[0],import_key("private_PseudoServer"))
    
    decrypted_messege = decrypted.decode()
    
    time.sleep(1.5)

    print("the decrypted messege to verify is:  "+ str(decrypted_messege)+"\n")
    
    print("server now generates the valid pseudonym from ture identity because of replay attacks...\n")
    
    time.sleep(1.5)

   
    pseudonyms = generate_pseudonyms_for_serverPhase2(true_identity)
    
    
    print("Comparsion of generated pseudonym and recieved pseudonym...\n")
    
    time.sleep(1.5)

    if (pseudonyms == decrypted_messege):
        print("the pseudonym validation result:  "+"\033[1;32;40m validated \033[0;0m \n")
    else:
        print("the pseudonym validation result:  "+"\033[1;31;40m NOT validated \033[0;0m \n")
    
    
    #Part2 for data send to client
    
    #the second part of the message
    signature_from_server_p22 = pseudonym_server_send_and_sign(generate_pseudonyms_withOutK(true_identity))
    print("signature generated for phase 2, part 2!")
    
    #building first part of message
    K2 = fetchSymmetricKey_plain("K2")
    
    message = generate_pseudonyms_withK2(true_identity)
    print("first part of message in phase 2 (pseudonym with k2), plain text:  "+ message)
    
    encrypted_message = encrypt(str.encode(message),import_key("PU_M"))
    signature_from_server_p21 = sign(encrypted_message,import_key("private_PseudoServer"))
    
    time.sleep(1.5)
    print("message (pseudonym with k2) is now encrypted and signed!")
    
    whole_message_unencrypted = [K2,encrypted_message,signature_from_server_p21,generate_pseudonyms_withOutK(true_identity),signature_from_server_p22]
    print("whole messege before symmetric encryption is now available!  :\n")
    print(str(whole_message_unencrypted))
    
    print("\n")
    print("symmetric encryption began!\n")
    print("\n")
    encrypted_message = symmetric_encryption("K1",str(whole_message_unencrypted))
    
    print("whole message after encryption:  \n" +str(encrypted_message))
    return encrypted_message,generate_pseudonyms_withOutK(true_identity)
    
def pseudonym_server_send_and_sign(decrypted_messege):
    signature = sign( str.encode(decrypted_messege),import_key("private_PseudoServer")) #remember the signature is bytes
    print("signature from server on pseudonym generated!\n")
    return signature
    
 
def phase3_process(enc_message_p2):
    decrypted_messege = symmetric_decryption("K1",enc_message_p2)
    original_array_message = literal_eval(decrypted_messege.decode()) #bytes -> str -> list
    print("original_array_message with decryption is:  \n\n"+ str(original_array_message))
    part_to_send = original_array_message[1]
    print("\n")
    print("the message to send in phase3 is:  \n\n" + str(part_to_send))
    return part_to_send


def phase4_process(ticket_address):
    ticket_data = fileToData(ticket_address)
    CM = fetchSymmetricKey_plain("symmetric key")
    time.sleep(1.5)
    message = [ticket_data, CM]
    print("whole message before encrytion in phase 4:   \n" + str(message))
    encrypted = symmetric_encryption("K2",str(message))
    print("\n")
    print("whole message after encrytion in phase 4:   \n" + str(encrypted))
    print("\n")
    dataToFile(encrypted,"Phase4_encrypted_data.encrypted")
    print("wrote the encrypted_message to  Phase4_encrypted_data.encrypted")
    return encrypted

def phase4_DecFile_validateTicket(address):
    
    print("reading encrypted file and decrypting")
    time.sleep(1.5)
    data = fileToData(address)
    decrypted_messege = symmetric_decryption("K2",data)
    original_array_message = literal_eval(decrypted_messege.decode()) #bytes -> str -> list
    
    print("\n")
    print("the original list after decryption:  \n")
    print(original_array_message)
    print("\n")
    dataToFile(original_array_message[0],"Phase4_decrypted_ticket.ticket")
    address = address = "Phase4_decrypted_ticket.ticket"
    validate_ticket("Phase4_decrypted_ticket.ticket")
    return

    








    
print("First you need to create a netbill account!")
true_identity = input("What is your identity? ( please don't use '||' in your username'):  ")
val = input("do you want to use Pseudonyms? type Y or N:  ")
print("\n")


    

    
pseudonym_final = true_identity
flag_pseudonym = 0
if (val == "Y"):

    print("\033[1;34;40m Begining phase 1 of pseudonym protocol! \033[0;0m \n")
    messege_encrypted_signed,pu,pv = generate_pseudonyms(true_identity)
    print("\033[1;34;40m Begining phase 2 of pseudonym protocol! \033[0;0m \n")
    enc_message_p2,pseudonym_final = pseudonym_verification_server(messege_encrypted_signed,pu,true_identity)
    print("\n")
    print("\033[1;34;40m Begining phase 3 of pseudonym protocol! \033[0;0m \n")
    phase3_messege = phase3_process(enc_message_p2)
    print("\n")
    print("\033[1;34;40m Begining phase 4 of pseudonym protocol! \033[0;0m \n")
    print("\n")
    print("your final pseudonym is:   \033[1;31;40m "+ pseudonym_final+"\033[0;0m \n")
    print("\n")
    print("now you should authenticate your self to the kerberos server\n")
    print("\n")
    flag_pseudonym = 1
    

    
add_new_princ(flag_pseudonym,pseudonym_final)
address_ticket = get_ticket_from_kerberos(flag_pseudonym)
time.sleep(1)
enc_message_p4 = phase4_process(address_ticket)

print("  \033[1;34;40m now i will decrypt phase4 message \033[0;0m \n")

phase4_DecFile_validateTicket("Phase4_encrypted_data.encrypted")

