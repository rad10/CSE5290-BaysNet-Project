from Elements import Node


def normalize(arr: list) -> list:
    total = sum(arr)
    for i in range(len(arr)):
        arr[i] /= total
    return arr
