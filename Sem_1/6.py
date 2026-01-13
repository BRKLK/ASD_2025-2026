# Selection sort
def SelectionSort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        temp = arr[i]
        arr[i] = arr[min_index]
        arr[min_index] = temp

    return arr


arr1 = [4, 5, 12, 2, 3, 1, 2, 8, 6, 7]
print(SelectionSort(arr1))
