def InsertionSort(arr):

    for i in range(1, len(arr)):
        temp = arr[i]
        j = i-1
        while j >= 0:
            if arr[j] > temp:
                arr[j+1] = arr[j]
            else:
                break
            j -= 1
        arr[j+1] = temp

    return arr

arr1 = [6, 1, 7, 4, 2, 9, 8, 5, 3]
print(InsertionSort(arr1))