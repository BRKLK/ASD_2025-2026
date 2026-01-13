def ShellSort(arr):
    l = len(arr)
    gap = l // 2
    swapped = False

    while gap > 1 or swapped:
        swapped = False

        for i in range(gap, l):
            temp = arr[i]
            j = i-gap
            while j >= 0:
                if arr[j] > temp:
                    arr[j+gap] = arr[j]
                    j -= gap
                    swapped = True
                else:
                    break
            arr[j + gap] = temp
        gap = gap // 2

    return arr


arr1 = [4, 2, 6, 3, 5, 8, 12, 4, 22, 7]
arr2 = [4, 2, 3, 1, 6]
print(ShellSort(arr1))