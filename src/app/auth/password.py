from argon2 import PasswordHasher

def verify_password(input_password, target):
    return encode_password(input_password) == target

def encode_password(password):
    return password