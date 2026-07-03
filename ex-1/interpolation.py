stack = [10,20,30,40,50,60, 67,70,80,90]

l = 0
r = len(stack) - 1

key = int(input("Enter the key to search: "))

while l<=r and key>=stack[l] and key<=stack[r]:

    estimated = l + ((key - stack[l]) * (r - l) // (stack[r] - stack[l]))

    if stack[estimated] < key:
        l = estimated + 1
    elif stack[estimated] > key:
        r = estimated - 1
    elif stack[estimated] == key:
        print(f"Key found at index: ", estimated)
        break
else:
    print("Key not found in the stack")
