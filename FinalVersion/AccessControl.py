from ast import literal_eval



#file operations
def fileToData(file_address):
    input_file = file_address
    with open(input_file, 'r') as f:
        data = f.read()
    return data

def dataToFile(data,name):
    output_file = name
    with open(output_file, 'w') as f:
        f.write(data)
    return






print("\033[1;34;40m*********************************\n")
print("**** Welcome To NetBill Access Control App\n")
print("*********************************\n\033[0;0m")

print("\n\n")

end = True


while (end is not False):
    command = input("Enter your command: (type \033[1;31;40m help \033[0;0m to see list of commands)    \n")
    commandArr = command.split(' ')
    if (commandArr[0] == "help"):
        print("\n")
        print("list of commands:\n")
        print("to add a user with purchasing access type:   add USERIDENTITY")
        print("\n note that USERIDENTITY may be PSEUDONYM")
        print("\n")
        print("to see current users type:   list\n")
        print("to exit the app type:   exit\n\n")
    elif (commandArr[0] == "add"):
        userToAdd = commandArr[1]
        data = fileToData("accessList.txt")
        dataArray = literal_eval(data) #str -> list
        dataArray.append(str(userToAdd))
        dataToFile(str(dataArray),"accessList.txt")
        print("success! user " +str(userToAdd)+" added to accessList \n\n")
    elif (commandArr[0] == "list"):
        data = fileToData("accessList.txt")
        dataArray = literal_eval(data) #str -> list
        print(dataArray)
        print("\n\n")
    elif (commandArr[0] == "exit"):
        end = False
    else:
        print("ERROR, type \033[1;31;40m help \033[0;0m to see list of commands \n\n")
print("Goodbye!\n")
        
        
        
