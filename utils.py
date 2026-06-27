import random
import string

def generate_transaction_id():
    lenght = 10
    chars = string.ascii_lowercase + string.digits
    id = ''.join(random.choices(chars, k=lenght))
    return id

print(generate_transaction_id())