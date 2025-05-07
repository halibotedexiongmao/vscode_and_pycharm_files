#循环：
def find_max(lst):
    max_value = lst[0]
    for i in lst:
        if i > max_value:
            max_value = i
    return max_value

char_list = list(input("请输入10个字符: "))
print(find_max(char_list))

#递归：
def find_max(lst, index=0):
    if index == len(lst) - 1:
        return lst[index]
    current_max = find_max(lst, index + 1)
    return lst[index] if lst[index] > current_max else current_max

char_list = list(input("请输入10个字符: "))
print(find_max(char_list))
