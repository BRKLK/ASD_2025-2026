def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def next_prime(n):
    if n <= 2:
        return 2
    prime = n
    if prime % 2 == 0:
        prime += 1
    while not is_prime(prime):
        prime += 2
    return prime

def fnv1a_hash(key, table_size):
    fnv_prime = 16777619
    hash_value = 2166136261

    for char in key:
        hash_value ^= ord(char)
        hash_value *= fnv_prime
    
    return hash_value % table_size

words = []

with open("hash_input_data.txt", 'r', encoding="utf-8") as f:
    words = [word for line in f for word in line.split(" ")]

table_size = next_prime(len(words))

hash_table = [[] for _ in range(table_size)]

for word in words:
    ind = fnv1a_hash(key=word, table_size=table_size)

    if word not in hash_table[ind]:
        hash_table[ind].append(word)

with open("output_14.txt", "w", encoding="utf-8") as f:
    for chain in hash_table:
        print(chain)
        f.write(' '.join(map(str, chain)) + "\n")