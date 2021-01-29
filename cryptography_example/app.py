from cryptography.fernet import Fernet

#key = b'8cozhW9kSi5poZ6TWFuMCV123zg-9NORTs3gJq_J5Do='
key = Fernet.generate_key()
f = Fernet(key)
print(key)

message_to_encrypt = b'encrypting is just as useful'

# Encrypt
ciphertext = f.encrypt(message_to_encrypt)
print(ciphertext)

# Decrypt
decryptedtext = f.decrypt(ciphertext)
print(decryptedtext)