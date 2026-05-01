from argon2 import PasswordHasher

hasher = PasswordHasher()

def verify_password(input_password, target):
    return hasher.verify(target, input_password)

def encode_password(password):
    return hasher.hash(password) 