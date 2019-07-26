import subprocess
import time
from shutil import copyfile



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


def get_ticket_from_kerberos(username):
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
    extractedFile = "/tmp/"+str(username)+"EX.txt"
    cmd = "klist -c "+address+">"+extractedFile
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    process_file = open(extractedFile,'r')
    to_process = process_file.readlines()
    splitedone = to_process[1].split('Default principal: ')
    splitedFinal = splitedone[1].split('@')
    usernameExtracted = splitedFinal[0]
    return usernameExtracted

    
    
val = input("do you ticket for Merchant or NetBill? type M or N:  ")
val = str(val)

if (val =="M"):
    add_new_princ(False,"Merchant")
    address_ticket = get_ticket_from_kerberos("Merchant")
    copyfile(address_ticket, "./Merchant.ticket")
    print("Ticket copied to local folder!")
elif (val =="N"):
    add_new_princ(False,"NetBill")
    address_ticket = get_ticket_from_kerberos("NetBill")
    copyfile(address_ticket, "./NetBill.ticket")
    print("Ticket copied to local folder!")
else:
    print("not a good value!\n\n BYE! \n\n")





