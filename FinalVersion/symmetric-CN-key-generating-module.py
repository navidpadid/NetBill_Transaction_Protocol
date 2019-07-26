from cryptography.fernet import Fernet

symmetric_key = Fernet.generate_key()
print(type(symmetric_key))

file = open('symmetric key CN.key', 'wb')
file.write(symmetric_key)
file.close()
