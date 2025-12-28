def count_sort(arr, exp):
    n = len(arr)
    # output = [0] * n
    count = [[] for _ in range(10)]

    for num in arr:
        key = (num // exp) % 10
        count[key].append(num)
    
    output = []
    for el in count:
        output += el

    return output

def radix_sort(arr):
    max_val = max(arr)

    exp = 1
    while max_val // exp > 0:
        arr = count_sort(arr, exp)
        exp *= 10

    return arr




print(radix_sort([170, 45, 75, 90, 802, 24, 2, 66]))
    
