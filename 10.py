def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(a: list[int], b: list[int]):
    res = []
    i = 0
    j = 0

    while i < len(a) and j < len(b):
        if a[i] >= b[j]:
            res.append(b[j])
            j += 1
        else:
            res.append(a[i])
            i += 1
    
    res += a[i:]
    res += b[j:]

    return res


# Тесты 
data = [38, 27, 43, 3, 9, 82, 10]
print("Исходный:", data)
sorted_data = merge_sort(data)
print("Отсортированный:", sorted_data)