import math
import random


def random_characters():
    # 集装箱编号由4位字母和6位数字组成
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    mapping = {"A": 10, "G": 17, "M": 24, "S": 30, "Y": 37, "B": 12, "H": 18, "N": 25, "T": 31, "Z": 38, "C": 13,
               "I": 19,
               "O": 26, "U": 32, "D": 14, "J": 20, "P": 27, "V": 34, "E": 15, "K": 21, "Q": 28, "W": 35, "F": 16,
               "L": 23,
               "R": 29, "X": 36, }

    # 生成10位的基本编号
    base_number = ''.join(random.sample(letters, 4)) + ''.join(random.sample(numbers, 6))
    # 计算校验码
    check_code = 0
    for i in range(10):
        number = base_number[i]
        if i <= 3:
            check_code += mapping[number] * math.pow(2, i)
        else:
            check_code += int(number) * math.pow(2, i)

    check_code = int(check_code) % 11

    container_number = base_number + str(check_code)
    return container_number