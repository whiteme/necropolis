
def Drop_All_Corpses(header , data):
    csv_list = []
    for sub_ary in data:
        for item in sub_ary:
            row = list()
            for col in header:
                row.append(item[col])
            csv_list.append(row)
    sorted_list = sorted(csv_list, key=lambda x: x[0])
    return sorted_list