import json
from cryptography.fernet import Fernet
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import linecache
from random import randint
import hashlib
from time import sleep
import time
import os
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



def fetchPrd(message):
    return message.split("||")[0]

def fetchBid(message):
    return message.split("||")[1]


def fetchProducts():
    with open('products.json') as json_file:
        data = json.load(json_file)
    return data['products']


def getProductId(products, prd):
    for product, product_info in products.items():
        if product_info["PRD"] == prd:
            return product_info["id"]



def getDefaultPrice(products, prd):
    for product, product_info in products.items():
        if product_info["PRD"] == prd:
            return product_info["price"]


def fetchGoodsIsbn(products):
    with open('PRD.txt') as file:
        prd = file.readline().split(" ")[1]
    for (key, value) in products.items():
        if value["PRD"] == prd:
            return value["ISBN"]


def getChecksum(message):
    hash_object = hashlib.sha256(message)
    return hash_object.hexdigest()


def fetchTid():
    with open('TID.txt') as file:
        return file.readline().split(" ")[1]


def fetchEpo():
    payment_order_file = open("payment order.txt")
    temp = 0
    for line in payment_order_file:
        if temp == 1:
            encrypted_epo = line[2:-1]
            fernet_key = fetchSymmetricKey("CM")
            return str(fernet_key.decrypt(encrypted_epo.encode()))[2:-1]
        temp += 1


def fetchMerchantKey():
    file = open("merchant key.key")
    return file.readline()

def getTimeStamp():
    return int(time.time()) // 1000

def fetchPrivateKey(key_type):
    if key_type == "C":
        pr_key_file = open("PV_C.pem", "rb").read()
        return RSA.importKey(pr_key_file)
    elif key_type == "M":
        pr_key_file = open("PV_M.pem", "rb").read()
        return RSA.importKey(pr_key_file)



def clearSign(message, key_type):
    time_stamp = str(getTimeStamp())
    private_key = fetchPrivateKey(key_type)
    digest = SHA256.new()
    digest.update((message + "||" + time_stamp).encode())
    signer = PKCS1_v1_5.new(private_key)
    result = message + "||" + time_stamp + "||" + str(signer.sign(digest))
    return result

def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    digest = SHA256.new()
    digest.update(message)
    return signer.verify(digest, signature)

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



def removeBackslash(string):
    if string[1] == '\\':
        return string[3:-2]
    else:
        return string[2:-1]


def fetchSignedResultNtoM():
    with open("signed-result-netbill-to-merchant.txt") as f:
        signed_result_netbill_to_merchant = f.readline()
        f.close()
    if signed_result_netbill_to_merchant == "Epoid Is Not Unique" or signed_result_netbill_to_merchant == "Balance Not Enough" or signed_result_netbill_to_merchant == "Customer does not have access to buy!" or signed_result_netbill_to_merchant == "You do not have an account in NetBill database":
        return signed_result_netbill_to_merchant

    fernet_key = fetchSymmetricKey("MN")
    string = signed_result_netbill_to_merchant[2:-1]
    print("\n\n\n")
    print(string)
    return str(fernet_key.decrypt(string.encode()))



def bargain(bid, suggesting_price):
    while int(bid) < int(suggesting_price):
        f = open("price-request.txt")
        temp = 0
        for lines in f:
            if temp == 1:
                price_request = lines[2:-1].encode()
            temp += 1
        
        print("\n")
        validate_ticket("Phase4_decrypted_ticket.ticket")
        username = extract_username_from_ticket("Phase4_decrypted_ticket.ticket")
        print("\n client identity or pseudonym:   "+ username +"\n\n")


        f.close()
        fernet_key = fetchSymmetricKey("CM")
        decrypted = str(fernet_key.decrypt(price_request))[2:-1]
        bid = fetchBid(decrypted)
        suggesting_price = str(int(suggesting_price) - 1)
        print("bid is: " + bid)
        print("my suggesting price is: " + suggesting_price)
        print()
        message_to_encrypt = (product_id + "||" + suggesting_price + "||" + TID).encode()
        encrypted_message = fernet_key.encrypt(message_to_encrypt)
        price_quote = [encrypted_message]
        history = open("history for price quote.txt", "a+")
        history.write("plain text: " + str(message_to_encrypt) + "\n")
        history.write("cipher text: "+str(price_quote[0]) + "\n"+"\n")
        with open("price-quote.txt", "w") as f:
            for item in price_quote:
                f.write("%s\n" % item)
        sleep(1)
    print("final price is: " + suggesting_price)
    with open("final-price.txt", "w+") as f:
        f.write("price: " + suggesting_price)
        f.close()
    sleep(1.5)


def sendGoods():
    
      
    print("\n")
    validate_ticket("Phase4_decrypted_ticket.ticket")
    username = extract_username_from_ticket("Phase4_decrypted_ticket.ticket")
    print("\n client identity or pseudonym:   "+ username +"\n\n")
    print("\n Ready to send goods! \n")
    sleep(2)
    
    goods_isbn = fetchGoodsIsbn(products)
    merchant_key = Fernet.generate_key()
    file = open('merchant key.key', 'wb')
    file.write(merchant_key)
    file.close()

    fernet_key = Fernet(merchant_key)
    encrypted_goods = fernet_key.encrypt(goods_isbn.encode())
    checksum_of_goods = getChecksum(encrypted_goods)

    fernet_key = fetchSymmetricKey("CM")
    EPOID = goods_isbn + "@" + fetchTid()
    file = open("epoid.txt", "w+")
    file.write("epoid: " + EPOID)
    file.close()

    goods = [encrypted_goods, fernet_key.encrypt((checksum_of_goods + "||" + EPOID).encode())]

    while True:
        f = open("goods-request.txt")
        if os.stat("goods-request.txt").st_size != 0:
            with open("goods.txt", "w") as f:
                for item in goods:
                    f.write("%s\n" % item)
            f.close()
            print()
            print("----------------------------------")
            print("----------------------------------")
            print()
            print("goods sent")
            break
        sleep(1)


def sendEndorsedEpo():
    while True:
        if os.stat("payment order.txt").st_size != 0:
            print()
            print("----------------------------------")
            print("----------------------------------")
            print("Payment Order Received")
            print("processing...")
            sleep(1.5)
            
            print("\n")
            validate_ticket("Phase4_decrypted_ticket.ticket")
            username = extract_username_from_ticket("Phase4_decrypted_ticket.ticket")
            print("\n client identity or pseudonym:   "+ username +"\n\n")
            print("\n Ready to send the transaction request to NetBill! \n")
            sleep(1.5)
            
            T_MN_M = "merchant-netbill"
            clear_signed_epo = fetchEpo()

            unhahsed_clear_signed_epo = str.join("||",
                                                 clear_signed_epo.split("||")[0:len(clear_signed_epo.split("||")) - 1])
            hashed_clear_signed_epo = clear_signed_epo.split("||")[len(clear_signed_epo.split("||")) - 1]

            merchant_account_number = "200"
            merchant_memo_field = "merchant-memo-field"
            merchant_key = fetchMerchantKey()
            plain_clear_signed_info = clearSign(
                clear_signed_epo + "||" + merchant_account_number + "||" + merchant_memo_field +
                "||" + merchant_key, "M")

            fernet_key = fetchSymmetricKey("MN")
            endorsed_epo = [T_MN_M.encode().decode('unicode-escape').encode('ISO-8859-1'),
                            fernet_key.encrypt(
                                plain_clear_signed_info.encode().decode('unicode-escape').encode('ISO-8859-1'))]

            if verify(unhahsed_clear_signed_epo.encode().decode('unicode-escape').encode('ISO-8859-1'),
                      removeBackslash(hashed_clear_signed_epo).encode().decode('unicode-escape').encode('ISO-8859-1'),
                      fetchPublicKey("C")):
                with open("endorsed epo.txt", "w+") as f:
                    for item in endorsed_epo:
                        f.write("%s\n" % item)
                print("Endorsed Epo Is Sent to NetBill Server")
                print("Waiting For Response From NetBill Server...")
                return True
            else:
                print("Sorry, but Your Signature Is Not Verified")
                print("Closing App")
                return False

            break
        sleep(1)

def sendSignedResult():
    while True:
        if os.stat("signed-result-netbill-to-merchant.txt").st_size != 0:
            decrypted_signed_result_netbill_to_merchant = fetchSignedResultNtoM()
            if decrypted_signed_result_netbill_to_merchant == "Balance Not Enough" or decrypted_signed_result_netbill_to_merchant == "Epoid Is Not Unique" or decrypted_signed_result_netbill_to_merchant == "You do not have an account in NetBill database" or decrypted_signed_result_netbill_to_merchant == "Customer does not have access to buy!":
                with open("signed-result-merchant-to-customer.txt", "w+") as f:
                    f.write("Error: " + decrypted_signed_result_netbill_to_merchant)
                    f.close()
                return decrypted_signed_result_netbill_to_merchant

            print()
            print("----------------------------------")
            print("----------------------------------")
            print("Signed Result Received From NetBill Server")

            signed_result_array = decrypted_signed_result_netbill_to_merchant.split("||")
            decrypted_part_of_signed_result = str.join("||", signed_result_array[0:len(signed_result_array) - 1])

            signed_result_array_temp = decrypted_part_of_signed_result.split("||")
            unhashed_part_of_signed_result = str.join("||", signed_result_array_temp[0:len(signed_result_array_temp) - 1])[2:]
            hashed_part_of_signed_result = signed_result_array_temp[len(signed_result_array_temp) - 1]
            signed_result_verified = True

            if verify(unhashed_part_of_signed_result.encode(),
                      removeBackslash(hashed_part_of_signed_result).encode().decode('unicode-escape').encode('ISO-8859-1'),
                      fetchPublicKey("N")):
                fernet_key = fetchSymmetricKey("CM")
                decrypted_signed_result_merchant_to_customer = decrypted_signed_result_netbill_to_merchant[2:-1]
                encrypted_signed_result_merchant_to_customer = fernet_key.encrypt(
                    decrypted_signed_result_merchant_to_customer.encode())
                print()
                print("Result From NetBill Server is Successfully Verified")
                print()
                with open("signed-result-merchant-to-customer.txt", "w+") as f:
                    f.write(str(encrypted_signed_result_merchant_to_customer))
                    f.close()
                print()
                print()
                print("Signed Result Forwarded to Customer")
            else:
                with open("signed-result-merchant-to-customer.txt", "w+") as f:
                    f.write("Error: Signature From NetBill Server Is Not Verified")
                    f.close()
                return "Signature From NetBill Server Is Not Verified"

            break

        sleep(1)




TID = str(randint(0, 1000000))
tid_file = open("TID.txt", "w+")
tid_file.write("tid: " + TID)
tid_file.close()
customer_identity = linecache.getline("price-request.txt", 1)
price_request = linecache.getline("price-request.txt", 2)[2:-1].encode()
fernet_key = fetchSymmetricKey("CM")
decrypted = str(fernet_key.decrypt(price_request))[2:-1]

PRD = fetchPrd(decrypted)
prd_file = open("PRD.txt", "w+")
prd_file.write("PRD: "+PRD)
prd_file.close()

products = fetchProducts()
product_id = getProductId(products, PRD)
default_price = getDefaultPrice(products, PRD)
suggesting_price = default_price



bid = fetchBid(decrypted)

bargain(bid, suggesting_price)
sendGoods()
signature_is_verifed = sendEndorsedEpo()
if signature_is_verifed:
    semi_result = sendSignedResult()
    if semi_result is not None:
        print(semi_result)
        print("Closing App")




# open("history for price quote.txt", "w").close()
# open("price-quote.txt", "w").close()
# open("goods.txt", "w").close()
# open("TRD.txt", "w").close()
# open("PID.txt", "w").close()
