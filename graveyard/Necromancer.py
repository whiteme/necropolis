import pandas as pd
import numpy as np
import json , random
from datetime import datetime


def Raise_dead(data_conf , start_datetime , freq , rows):
    dates = __datetime(start_datetime , freq , rows)
    dates_str = dates.strftime('%Y-%m-%d %H:%M:%S')
    tmp = {}
    tmp["index"] = dates_str
    for i in range(len(data_conf)):
        item = data_conf[i]
        col_name = data_conf[i]['prop']
        tmp[col_name] = __dispatcher(item , rows)
    df = pd.DataFrame(tmp)
    return df




def __dispatcher(item , rows):
    if item['func'] == 'F_RAND_STR':
        return __rand_str(rows)
    #
    elif item['func'] == 'F_RAND_NUM':
        return __rand_num(rows)
    #
    elif item['func'] == 'F_CONST':
        if item.__contains__('input') and  item['input'] is not None :
            return __const(item['input'] , rows)
        else:
            return __const(item['name'] , rows)
    #
    elif item['func'] == 'F_COUNT':
        default_count = 3
        if item.__contains__('input') and  item['input'] is not None :
            default_count = item['input']
        if item.__contains__('prefix') and  item['prefix'] is not None :
            return __count(item['prefix'] , int(default_count) , rows)
        else:
            return __count( None , int(default_count) , rows)
    #
    elif item['func'] == 'F_SEQ':
        default_begin = 1
        if item.__contains__('input') and  item['input'] is not None :
            default_begin = item['input']
        if item.__contains__('prefix') and  item['prefix'] is not None :
            return __seq(item['prefix'] , int(default_begin) , rows)
        else:
            return __seq( None , int(default_begin) , rows)
    
    elif item['func'] == 'F_EMPTY':
        return ""
    
    elif item['func'] == 'F_STAT_SUM':
        if item.__contains__('input') and  item['input'] is not None :
            return __sum(int(item['input']) , rows)
        else:
            return __sum(50000 , rows)
    elif item['func'] == 'F_STAT_AVG':
        return __sum(10000 , rows)
    
    elif item['func'] == 'F_STAT_TREND':
        init_val = 10000
        delta = "1%"
        if item.__contains__('input') and  item['input'] is not None :
            init_val = float(item['input'])
        if item.__contains__('prefix') and  item['prefix'] is not None :
            delta =  item['prefix'] 
        return __trend(init_val , delta , rows)
    elif item['func'] == 'F_RAND_IP':
        return __rand_ip(rows)
    elif item['func'] == 'F_RAND_PHONE':
        return __rand_phone(rows)
    else:
        return ""
    

def __datetime(start_date , freq_arg , rows):
    return pd.date_range(start_date , periods=rows , freq=freq_arg )

def __const(const , rows):
    return pd.Series([const]*rows)


def __seq(prefix  , begin , rows):
    arr = np.arange(int(begin), int(begin) + rows)
    if prefix is not None:
        arr= np.array([prefix + '{}'.format(i) for i in arr])
    s = pd.Series(arr)
    return s

def __count(prefix , cnt , rows ):
    arr = np.random.randint(1 , cnt+1, size=rows)
    if prefix is not None:
         arr= np.array([prefix + '{}'.format(i) for i in arr])
    return pd.Series(arr)

def __rand_str(rows):
    return pd.Series(np.random.choice(list('abcdefghijklmnopqrstuvwxyz'), size=rows))

def __rand_num(rows):
    return pd.Series( np.random.randint(1, 201, size=rows))

def __sum(sum , rows):
    s = pd.Series(np.zeros(rows))
    total_sum = 0
    while total_sum < sum:
        idx = np.random.randint(0, rows)
        increment = min(np.random.randint(1, 100), sum - total_sum)
        s[idx] += increment
        total_sum = s.sum()
    return s

def __avg(avg , rows):
    pass

def __trend(init_val , delta , rows):
    # delta = str()
    if delta.find('%') != -1:
        pct = float(delta[:-1])/100.0 + 1.0
        arr = [pct ** (i+1) for i in range(rows)]
        # print(arr)
        s = pd.Series(arr) * init_val
        return s.round(2)
    else:
        arr = [ float(delta)*(i+1)  for i in range(rows)]
        # print(arr)
        # return pd.Series(arr).cumsum() + init_val
        return pd.Series(arr) + init_val
    

def __inc(init_val , rows):
    decrease_factors = [0.95 ** i for i in range(rows)]
    arr = pd.Series(decrease_factors).cumsum() + init_val
    return arr

def __rand_ip(rows):
    arr = [".".join(str(random.randint(0, 255)) for _ in range(4)) for _ in range(rows)]
    return pd.Series(arr)

def __rand_phone(rows):
    def generate_random_phone_number():
        prefix = ['130', '131', '132', '145', '150', '151', '152', '153', '155', '156', '157', '158', '159', '170', '176', '177', '178', '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
        p = random.choice(prefix)
        num = random.randint(10000000, 99999999)
        return p + str(num)
    return pd.Series([generate_random_phone_number() for _ in range(rows)])

def __distrib(vals_ary , ratios , rows):
    cum_ratios = np.array(ratios) / sum(ratios)
    # print(cum_ratios)
    arr = np.random.choice(vals_ary, size=rows, p=cum_ratios)
    return pd.Series(arr)


if __name__ == "__main__":
    # print(__seq("seq_0000" , 1000 , 10))

    a = '110%'
    print(__trend(10000 , "-10%" , 10))
    # print(__distrib(["a","bb","ccc"] , [2 , 1 , 1], 10) )