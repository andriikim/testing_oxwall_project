import random
import string


cyr_symbol = ''.join([chr(l) for l in range(0x0400, 0x04FF)
                      if chr(l).isprintable()])


def random_string(min_len=1, max_len=255):
    length = random.randrange(min_len, max_len+1)
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10 + cyr_symbol
    return ''.join(random.choices(symbols, k=length))


if __name__ == "__main__":
    print(random_string())

