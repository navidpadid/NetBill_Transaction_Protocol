import json
from cryptography.fernet import Fernet
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from time import sleep
import time
import os
import hashlib
from random import randint
import subprocess






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





def cleanFilesToStart():
    open("history for price quote.txt", "w").close()
    open("history for price request.txt", "w").close()
    open("signed-result-netbill-to-merchant.txt", "w").close()
    open("price-quote.txt", "w").close()
    open("goods.txt", "w").close()
    open("TRD.txt", "w").close()
    open("PID.txt", "w").close()
    open("goods-request.txt", "w").close()
    open("history for goods request.txt", "w").close()
    open("signed-result-merchant-to-customer.txt", "w").close()
    open("endorsed epo.txt", "w").close()
    open("epoid.txt", "w").close()
    open("final-price.txt", "w").close()
    open("payment order.txt", "w").close()
    open("PRD.txt", "w").close()
    open("price-request.txt", "w").close()
    open("TID.txt", "w").close()


def fetchProductsNames():
    result = []

    with open('products.json') as json_file:
        data = json.load(json_file)
    for a, b in data.items():
        for c, d in b.items():
            result.append(c)

    return result

def fetchTid():
    with open('TID.txt') as file:
        return file.readline().split(" ")[1]


def fetchProducts():
    with open('products.json') as json_file:
        data = json.load(json_file)
    return data['products']


def getPrdOf(product_name, products):
    return products[product_name]["PRD"]

def fetchPrd():
    prd_file = open("PRD.txt")
    return prd_file.readline().split(" ")[1]

def fetchProductId(prd):
    products = fetchProducts()
    for product, product_info in products.items():
        if product_info["PRD"] == prd:
            return product_info["id"]


def fetchNegotiatedPrice():
    price_file = open("final-price.txt")
    return price_file.readline().split(" ")[1]

def fetchEncryptedChecksumEpoid():
    goods_file = open("goods.txt")
    temp = 0
    for line in goods_file:
        if temp == 1:
            return line
        temp += 1

def decryptWithCmKey(cipher):
    fernet_key = fetchSymmetricKey("CM")
    return str(fernet_key.decrypt(cipher[2:-1].encode()))[2:-1]

def getChecksum(message):
    hash_object = hashlib.sha256(message)
    return hash_object.hexdigest()


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


def fetchPrivateKey(key_type):
    if key_type == "C":
        p_key_file = open("PV_C.pem", "rb").read()
        return RSA.importKey(p_key_file)
    elif key_type == "M":
        p_key_file = open("PV_M.pem", "rb").read()
        return RSA.importKey(p_key_file)



def getTimeStamp():
    return int(time.time()) // 1000


def clearSign(message, key_type):
    time_stamp = str(getTimeStamp())
    private_key = fetchPrivateKey(key_type)
    digest = SHA256.new()
    digest.update((message + "||" + time_stamp).encode())
    signer = PKCS1_v1_5.new(private_key)
    result = message + "||" + time_stamp + "||" + str(signer.sign(digest))
    return result


def encryptWithCnKey(identity, auth, acc_num, nonce, memo):
    fernet_key = fetchSymmetricKey("CN")
    return fernet_key.encrypt((identity + "||" + auth + "||" + acc_num + "||" + nonce + "||" + memo).encode())


def fetSuggestedPrice(message):
    return message.split("||")[1]


def fetchReceipt(encoded_message, fernet_key):
    message = str(fernet_key.decrypt(encoded_message[2:-1].encode()))[2:-1]
    return message


def fetchMerchantKeyFromReceipt(receipt):
    receipt_array = receipt.split("||")
    return receipt_array[5]


def fetchEncryptedGoods():
    with open ("goods.txt") as f:
        return f.readline()



def decryptGoods(message, key):
    fernet_key = Fernet(key.encode())
    return str(fernet_key.decrypt(message[2:-1].encode()))[2:-1]


def bargain(bid, identity, prd):
    price_quote = ""
    while True:
        f = open("price-quote.txt")
        temp = 0

        if os.stat("price-quote.txt").st_size != 0:
            for line in f:
                if temp == 0:
                    price_quote = line[2:-1].encode()
                temp += 1
            f.close()
            break
        sleep(1)
    fernet_key = fetchSymmetricKey("CM")
    decrypted = str(fernet_key.decrypt(price_quote))[2:-1]
    suggested_price = fetSuggestedPrice(decrypted)

    while abs(int(bid) - int(suggested_price)) > 1:
        f = open("price-quote.txt")
        temp = 0

        for line in f:
            if temp == 0:
                price_quote = line[2:-1].encode()
            temp += 1
        f.close()

        decrypted = str(fernet_key.decrypt(price_quote))[2:-1]
        suggested_price = fetSuggestedPrice(decrypted)

        bid = str(int((int(bid) + int(suggested_price)) / 2))
        fernet_key = fetchSymmetricKey("CM")

        message_to_encrypt = (prd + "||" + bid).encode()
        encrypted_message = fernet_key.encrypt(message_to_encrypt)
        price_request = [identity.encode(), encrypted_message]
        history = open("history for price request.txt", "a+")
        history.write("plain text: "+identity + " " + str(message_to_encrypt) + "\n")
        history.write("cipher text: "+str(price_request[0]) + " " + str(price_request[1]) + "\n"+"\n")
        with open("price-request.txt", "w") as f:
            for item in price_request:
                f.write("%s\n" % item)
        print("My Bid Is: "+bid)
        print("Suggested Price Is: " +suggested_price)
        print()
        sleep(1)
    print("Final Price Is: " + bid)


def sendGoodsRequest(identity):
    while True:
        if os.stat("price-quote.txt").st_size != 0:
            TID = fetchTid()
            fernet_key = fetchSymmetricKey("CM")
            message_to_encrypt = TID.encode()
            encrypted_message = fernet_key.encrypt(message_to_encrypt)
            history = open("history for goods request.txt", "a+")
            history.write("plain text: " + T_CM_IDENTITY + " " + str(message_to_encrypt) + "\n")
            goods_request = [identity, encrypted_message]
            history.write("cipher text: " + str(goods_request[0]) + " " + str(goods_request[1]) + "\n" + "\n")
            with open("goods-request.txt", "w+") as f:
                for item in price_request:
                    f.write("%s\n" % item)
                f.close()
            print()
            print("----------------------------------")
            print("----------------------------------")
            print()
            print("Goods Request Sent")
            break
        sleep(1)

def sendPaymentOrder(T_CM_IDENTITY):
    while True:
        if os.stat("goods.txt").st_size != 0:
            print()
            print("----------------------------------")
            print("----------------------------------")
            print("Encrypted Goods Received")
            sleep(1.5)
            prd = fetchPrd()
            customer_identity = "customer-identity"
            product_id = fetchProductId(prd)
            negotiated_price = fetchNegotiatedPrice()
            merchant_identity = "merchant-identity"

            encrypted_checksum_epoid = fetchEncryptedChecksumEpoid()
            checksum_epoid = decryptWithCmKey(encrypted_checksum_epoid)
            checksum_of_encrypted_good = checksum_epoid.split("||")[0]
            epoid = checksum_epoid.split("||")[1]

            checksum_of_prd = getChecksum(prd.encode())
            
            username = extract_username_from_ticket("Phase4_decrypted_ticket.ticket")
            print("\n customer username:  "+username)
            print("\n")
            customer_account_number = username
            account_verification_nonce = str(randint(0, 1000)) + "@" + customer_account_number
            checksum_of_acc_number_nonce = getChecksum(
                (customer_account_number + "||" + account_verification_nonce).encode())

            T_CN_Identity = "true-identity"

            authorization_token = "auth-token"
            customer_memo_field = "customer-memo-field"

            fernet_key = fetchSymmetricKey("CN")
            encrypted_part_of_epo = [T_CN_Identity.encode(),
                                     encryptWithCnKey(T_CN_Identity, authorization_token, customer_account_number,
                                                      account_verification_nonce, customer_memo_field)]

            epo = customer_identity + "||" \
                  + product_id + "||" \
                  + negotiated_price + "||" \
                  + merchant_identity + "||" \
                  + checksum_of_encrypted_good + "||" \
                  + checksum_of_prd + "||" \
                  + checksum_of_acc_number_nonce + "||" \
                  + epoid + "||" \
                  + str(encrypted_part_of_epo[0]) + "||" \
                  + str(encrypted_part_of_epo[1])

            clear_signed_epo = clearSign(epo, "C")

            fernet_key = fetchSymmetricKey("CM")
            encrypted_clear_epo = fernet_key.encrypt(
                clear_signed_epo.encode().decode('unicode-escape').encode('ISO-8859-1'))
            fernet_key = fetchSymmetricKey("CM")
            payment_order = [T_CM_IDENTITY.encode().decode('unicode-escape').encode('ISO-8859-1'), encrypted_clear_epo]

            with open("payment order.txt", "w+") as f:
                for item in payment_order:
                    f.write("%s\n" % item)
                f.close()
            print()
            print("Signed Electronic Payment Order Sent")
            print("Waiting For Response From Merchant")
            break
        sleep(1)

def receiveSignedResult():
    while True:
        if os.stat("signed-result-merchant-to-customer.txt").st_size != 0:
            print()
            print("----------------------------------")
            print("----------------------------------")
            print("Result Received")
            with open("signed-result-merchant-to-customer.txt") as f:
                result = f.readline()
                if "Error" in result:
                    print()
                    print(result)
                    return
            fernet_key = fetchSymmetricKey("CM")
            receipt = fetchReceipt(result, fernet_key)
            merchantKey = fetchMerchantKeyFromReceipt(receipt)
            encrypted_goods = fetchEncryptedGoods()
            goods = decryptGoods(encrypted_goods, merchantKey)
            print()
            print("hooray, got my ISBN :)")
            print("ISBN is : " + goods)
            break
        sleep(1)






cleanFilesToStart()
products_names = fetchProductsNames()
print()
print("What do you want to buy? Enter the Number of the Product...")
temp = 0
print()
for item in products_names:
    print(str(temp+1) + ". " + item)
    print()
    temp += 1

idx = int(input())
PRODUCT_TO_PURCHASE = products_names[idx - 1]
print()
print("What Will Be Your Starting Bid for This Item?")
print()
starting_bid = input()

T_CM_IDENTITY = "merchant-customer"
products = fetchProducts()
PRD = getPrdOf(PRODUCT_TO_PURCHASE, products)

fernet_key = fetchSymmetricKey("CM")

message_to_encrypt = (PRD + "||" + starting_bid).encode()
encrypted_message = fernet_key.encrypt(message_to_encrypt)
price_request = [T_CM_IDENTITY.encode(), encrypted_message]
history = open("history for price request.txt", "a+")
history.write("plain text: "+T_CM_IDENTITY + " " + str(message_to_encrypt) + "\n")
history.write("cipher text: " + str(price_request[0]) + " " + str(price_request[1]) + "\n"+"\n")

print("price request sent, waiting for response...")
print()
with open("price-request.txt", "w") as f:
    for item in price_request:
        f.write("%s\n" % item)
    f.close()


bargain(starting_bid, T_CM_IDENTITY, PRD)
sendGoodsRequest(T_CM_IDENTITY)
sendPaymentOrder(T_CM_IDENTITY)
receiveSignedResult()

# open("history for price request.txt", "w").close()
# open("price-request.txt", "w").close()
# open("goods-request.txt", "w").close()


