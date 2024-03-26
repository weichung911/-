
def remove_duplicate_lists(lists):
    seen = set()
    result = []
    for sublist in lists:
        if len(sublist) == len(set(sublist)):
            result.append(sublist)
    return result


# 示例
input_lists = [['a', 'a'], ['a', 'b'], ['c', 'b'], ['b', 'c', 'c']]
output = remove_duplicate_lists(input_lists)
print(output)