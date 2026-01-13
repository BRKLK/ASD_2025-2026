# Comb Sort
def CombSort(arr):
    n = len(arr)
    gap = n

    swapped = True

    while gap != 1 or swapped:

        # Getting new gap
        gap = (gap*10)//13
        if gap < 1:
            gap = 1

        swapped = False
        
        for i in range(n-gap):
            if arr[i] > arr[i+gap]:
                temp = arr[i]
                arr[i] = arr[i+gap]
                arr[i+gap] = temp
                swapped = True
    
    return arr


arr = [8, 4, 1, 56, 3, -44, 23, -6, 28, 0]
print(CombSort(arr))



