# binary search -- function with many parameters

binary_search()
def binary_search(start, end, numbers, target):
    if start > end: return start
    mid = start + (end-start)//2
    
    if numbers[mid] == target:
        return mid
    
    elif numbers[mid] > target:
        return binary_search(start, mid-1, numbers, target)
    
    return binary_search(mid+1, end, numbers, target)

nums = [0, -56, 103, 124, 2, 5, 1, -10, -13, 54]
nums = sorted(nums)

start = 0
end = len(nums)-1
target = 5