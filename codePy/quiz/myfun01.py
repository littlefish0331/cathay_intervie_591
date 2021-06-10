import re
def chtnum2dignum(x):
    chtnum = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    dignum = map(str, range(0, 11))
    dict_cht2dig = dict(zip(chtnum, dignum))
    # dict_cht2dig = dict((re.escape(k), v) for k, v in dict_cht2dig.items()) # in case there are escape string
    pattern = re.compile("|".join(dict_cht2dig.keys()))
    
    try:    
        chtnum = list(x.replace('層', ''))
        dignum = [int(pattern.sub(lambda m: dict_cht2dig[re.escape(m.group(0))], x)) for x in chtnum]
        digit_output = 0
        base_term = 1
        for i in range(len(dignum))[::-1]:
            if (dignum[i] == 10 and i == 0):
                digit_output = digit_output + int(dignum[i])
            elif (dignum[i] == 10):
                base_term = int(dignum[i])
            else:
                digit_output = digit_output + base_term * int(dignum[i])
    except:
        '''
        some '總樓層數' are nan
        '''
        digit_output = 0
    
    return digit_output