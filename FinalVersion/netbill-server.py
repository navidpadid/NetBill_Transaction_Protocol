import json
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA, DSA
#from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
import time
import subprocess
from ast import literal_eval



#file operations navid
def fileToDataACL(file_address):
    input_file = file_address
    with open(input_file, 'r') as f:
        data = f.read()
    return data

def dataToFileACL(data,name):
    output_file = name
    with open(output_file, 'w') as f:
        f.write(data)
    return

def in_acl():
    username = extract_username_from_ticket("Phase4_decrypted_ticket.ticket")
    data = fileToDataACL("accessList.txt")
    print("customer username:  "+username)
    dataArray = literal_eval(data) #str -> list
    if username in dataArray:   
        return True
    else:
        return False


#navid functions
    
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





def fetchAllEpoids():
    keys = []
    values = []
    with open('epoids.json') as json_file:
        data = json.load(json_file)
    for a, b in data.items():
        for key, value in b.items():
            keys.append(key)
            values.append(value)
    return keys, values


def fetchProducts():
    with open('products.json') as json_file:
        data = json.load(json_file)
    return data['products']



def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    digest = SHA256.new()
    digest.update(message)
    return signer.verify(digest, signature)


def fetchEndorsedEpo():
    endorsed_epo_file = open("endorsed epo.txt")
    temp = 0
    
    
    print("\n")
    validate_ticket("Merchant.ticket")
    username = extract_username_from_ticket("Merchant.ticket")
    print("\n merchant identity:   "+ username +"\n\n")
    
    
    for line in endorsed_epo_file:
        if temp == 1:
            encrypted_endorsed_epo = line[2:-1]
            fernet_key = fetchSymmetricKey("MN")
            return str(fernet_key.decrypt(encrypted_endorsed_epo.encode()))[2:-1]
        temp += 1


def fetchSymmetricKey(key_type):
    symmetric_key = ""
    if key_type == "CM":
        with open('symmetric key CM.key') as file:
            symmetric_key = bytes(file.read(), "utf-8")
    elif key_type == "CN":
        with open('symmetric key CN.key') as file:
            symmetric_key = bytes(file.read(), "utf-8")
    elif key_type == "MN":
        with open('symmetric key MN.key') as file:
            symmetric_key = bytes(file.read(), "utf-8")

    return Fernet(symmetric_key)

def removeBackslash(string):
    if string[1] == '\\':
        return string[3:-2]
    else:
        return string[2:-1]


def fetchPublicKey(key_type):
    if key_type == "C":
        pu_key_file = open("PU_C.pem", "rb").read()
        return RSA.importKey(pu_key_file)
    elif key_type == "M":
        pu_key_file = open("PU_M.pem", "rb").read()
        return RSA.importKey(pu_key_file)
    elif key_type == "N":
        pu_key_file = open("PU_NetBill.pem", "rb").read()
        return RSA.importKey(pu_key_file)


def fetchAccountBalance(account_number):
    with open('customer-accounts-netbill.json') as json_file:
        data = json.load(json_file)
    for a, b in data.items():
        for num, info in b.items():
            if num == account_number:
                return info["balance"]


def fetchPrivateKey(key_type):
    if key_type == "C":
        p_key_file = open("PV_C.pem", "rb").read()
        return RSA.importKey(p_key_file)
    elif key_type == "M":
        p_key_file = open("PV_M.pem", "rb").read()
        return RSA.importKey(p_key_file)
    elif key_type == "N":
        p_key_file = open("PV_NetBill.pem", "rb").read()
        return RSA.importKey(p_key_file)


def getTimeStamp():
    return int(time.time()) // 1000


def dsaSign(message, key_type):
    time_stamp = str(getTimeStamp())
    private_key = fetchPrivateKey(key_type)
    digest = SHA256.new()
    digest.update((message + "||" + time_stamp).encode())
    signer = PKCS1_v1_5.new(private_key)
    result = message + "||" + time_stamp + "||" + str(signer.sign(digest))
    return result


def updateEpoids(epoid, keys, epoids):
    new_epoids = {}
    index = str(int(keys[len(keys) - 1]) + 1)
    for i in range(0, len(keys)):
        new_epoids[keys[i]] = epoids[i]
    new_epoids[index] = epoid

    with open("epoids.json", "w") as fp:
        json.dump({"epoids": new_epoids}, fp)
        fp.close()

def updateAccounts(acc_num, price):
    with open('customer-accounts-netbill.json') as json_file:
        all_accounts = json.load(json_file)
    container = {}
    for a, b in all_accounts.items():
        for num, info in b.items():
            if num == acc_num:
                container[num] = {
                    "balance": str(int(info["balance"]) - int(price)),
                    "blocked": info["blocked"]
                }
            else:
                container[num] = info
    new_accounts = {"accounts": container}
    with open('customer-accounts-netbill.json', "w") as json_file:
        json.dump(new_accounts, json_file)
        json_file.close()


endorsed_epo = fetchEndorsedEpo()

message_is_verified = True
epoid_is_unique = True
balance_is_enough = True

fernet_key = fetchSymmetricKey("MN")
unhashed_endorsed_epo = str.join("||", endorsed_epo.split("||")[0:len(endorsed_epo.split("||")) - 1])
hashed_endorsed_epo = endorsed_epo.split("||")[len(endorsed_epo.split("||")) - 1]

if verify(unhashed_endorsed_epo.encode(),
             removeBackslash(hashed_endorsed_epo.encode().decode('unicode-escape').encode('ISO-8859-1')),
             fetchPublicKey("M")):
    print()
    print("Endorsed Epo is Successfully Verified")
    print()
else:
    message_is_verified = False
    flag = "Message is not Verifeid"

result = "0"

flag = "OK!"
key_epoids, epoids = fetchAllEpoids()

merchant_key = unhashed_endorsed_epo.split("||")[14]
epo_array = unhashed_endorsed_epo.split("||")[0:11]
epo = str.join("||", epo_array)
identity = epo_array[0]
price = epo_array[2]
product_id = epo_array[1]
m = epo_array[3]
current_epoid = epo_array[7]
encrypted_part_epo = (epo_array[len(epo_array) - 2])[3:-2]
fernet_key = fetchSymmetricKey("CN")
[true_identity, authorization, CAcct, AcctVn, CMemo] = (str(fernet_key.decrypt(encrypted_part_epo.encode()))[2:-1]).split("||")


if current_epoid in epoids:
    epoid_is_unique = False


receipt = str(result) + "||" \
        + identity + "||" \
        + price + "||" \
        + product_id + "||" \
        + m + "||" \
        + merchant_key + "||" \
        + current_epoid

account_balance = fetchAccountBalance(CAcct)

if account_balance is not None and int(account_balance) < int(price):
    balance_is_enough = False
    flag = "Balance Not Enough"

if account_balance is None:
    flag = "You do not have an account in NetBill database"


if account_balance is not None and int(account_balance) - int(price) < 100 and balance_is_enough:
    flag = "Balance Reached Below 100"


if not epoid_is_unique:
    flag = "Epoid Is Not Unique"
    epoid_is_unique = False
    
    
res = in_acl()
if not res:
    flag = "Customer does not have access to buy!"

if not res or not epoid_is_unique or not balance_is_enough or account_balance is None:
    with open("signed-result-netbill-to-merchant.txt", "w+") as f:
        f.write(flag)
        f.close()

else:
    updateEpoids(current_epoid, key_epoids, epoids)
    updateAccounts(CAcct, price)

    signed_receipt = dsaSign(receipt, "N")

    decrypted_second_part = current_epoid + "||" + CAcct + "||" + str(int(account_balance) - int(price)) + "||" + flag

    fernet_key = fetchSymmetricKey("CN")
    signed_result_part_two = fernet_key.encrypt(decrypted_second_part.encode().decode('unicode-escape').encode('ISO-8859-1'))

    fernet_key = fetchSymmetricKey("MN")
    decrypted_signed_result = signed_receipt + "||" + str(signed_result_part_two)
    signed_result = fernet_key.encrypt(decrypted_signed_result.encode().decode('unicode-escape').encode('ISO-8859-1'))



    with open("signed-result-netbill-to-merchant.txt", "w+") as f:
        f.write(str(signed_result))
        f.close()
    print()
    print("Signed Result Sent to Merchant")
    print()
