def heapify(arr: list[int], index: int, n: int):
    largest = index
    left = 2 * index + 1
    right = 2 * index + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != index:
        arr[index], arr[largest] = arr[largest], arr[index]
        heapify(arr, largest, n)


def build_max_heap(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, i, n)


def heap_sort(arr):
    build_max_heap(arr)
    n = len(arr)
    
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]

        heapify(arr, 0, i)
    
    return arr

# Проверка
data = [12, 11, 13, 5, 6, 7]
heap_sort(data)
print(data) # [5, 6, 7, 11, 12, 13]
