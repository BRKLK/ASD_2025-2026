def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]

    left = [el for el in arr if el < pivot]
    middle = [el for el in arr if el == pivot]
    right = [el for el in arr if el > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# Тест
data = [12, 7, 14, 9, 10, 11]
print(quick_sort(data))