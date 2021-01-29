import sys
import bcrypt

password = b"learningisfun"

# Hash a password for the first time, with a certain number of rounds
salt = bcrypt.gensalt(14)
hashed = bcrypt.hashpw(password, salt)
print(salt)
print(hashed)

# Check a plain text string against the salted, hashed digest
print(bcrypt.checkpw(password, hashed))