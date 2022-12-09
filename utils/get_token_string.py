from utils.hash_password import hash_password
import random
# do it by plugin!!


def get_token_string(password_hash, id):
    return hash_password(password_hash + id + str(random.randint(0, 1000)))
