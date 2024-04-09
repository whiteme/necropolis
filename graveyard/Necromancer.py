import pandas as pd
import numpy as np
import json
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
    elif item['func'] == 'F_RAND_NUM':
        return __rand_num(rows)
    elif item['func'] == 'F_CONST':
        if item['input'] is not None :
            return __const(item['input'] , rows)
        else:
            return __const(item['name'] , rows)
    elif item['func'] == 'F_EMPTY':
        return ""
    elif item['func'] == 'F_STAT_SUM':
        return __sum(50000 , rows)
    elif item['func'] == 'F_STAT_AVG':
        return __avg(10000 , rows)
    else:
        return ""
    

def __datetime(start_date , freq_arg , rows):
    freq = pd.offsets.Day()
    if freq_arg == "M" :
        freq = pd.offsets.Minute()
    elif freq_arg == "H":
        freq = pd.offsets.Hour()
    return pd.date_range(start_date ,periods=rows , freq=freq)

def __const(const , rows):
    return pd.Series([const]*rows)

def __count(cnt , rows):
    data = np.random.randint(1 , cnt+2, size=rows)
    return pd.Series(data)

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

def __inc(init_val , rows):
    decrease_factors = [0.95 ** i for i in range(rows)]
    arr = pd.Series(decrease_factors).cumsum() + init_val
    return arr

def __seq(prefix  , rows , begin):
    arr = np.arange(begin, begin + rows)
    s = pd.Series(arr)
    s = s.apply(lambda x: prefix + str(x))
    return s


if __name__ == "__main__":
    arr = __const("abc" , 5)
    t = {}
    t["a"] = arr
    print(pd.DataFrame({"index" : list("abcde") , "value":arr} ))