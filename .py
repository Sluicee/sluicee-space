import random
import string

def generate_secret_key():
    # Генерируем случайную строку длиной 50 символов
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(50))

print(generate_secret_key())
