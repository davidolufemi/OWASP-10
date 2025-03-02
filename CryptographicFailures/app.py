import hashlib
import os
# MD5 is an outdated hashing algorithm that is considered cryptographically insecure due to its vulnerability to collision attacks.

# Vulnerable use of MD5
password = "user_password"
password_collision = "6d7fce9eb1e91c5a830e27f4c4b180e4"
hashed_password = hashlib.md5(password.encode()).hexdigest()
hashed_password_collision = hashlib.md5(password.encode()).hexdigest()

print("Hashed password:", hashed_password)
print("Hashed password:", hashed_password_collision)



# These two passwords produce the same hash and result in a collision. 


# Storing passwords without a salt makes it vulnerable to rainbow table attacks, where attackers can precompute hashes of common passwords and easily break weak password hashes.


# Storing password without salt (bad practice)
password = "user_password"
hashed_password = hashlib.sha256(password.encode()).hexdigest()

print("Hashed password:", hashed_password)


# With salt


# Create a salt
salt = os.urandom(16)  # 16 bytes of randomness

# Store password with salt
password = "user_password"
salted_password = salt + password.encode()
hashed_password = hashlib.sha256(salted_password).hexdigest()

print("Hashed password with salt:", hashed_password)
