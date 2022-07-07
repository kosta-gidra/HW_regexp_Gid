import csv
import re


def read_file():
    with open('phonebook_raw.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
        return contacts_list


def reform_number(file):
    for row in file[1:]:
        pattern = r'(\+*\d)[\s(]*\(*(\d{3})[\)-]*\s*(\d{3})\-*(\d{2})\-*(\d{2})(\s*)\(*([доб.]*)\s*([\d{4}]*)\)*'
        sub = r'+7(\2)\3-\4-\5\6\7\8'
        result = re.sub(pattern, sub, row[5])
        row[5] = result
    return file


def reform_names(file):
    for row in file[1:]:
        name = ' '.join(row[:3])
        names = name.split(' ')
        row[0] = names[0]
        row[1] = names[1]
        row[2] = names[2]
    return file


def merge_duplicates(file):
    duplicate = {'example': file[0]}
    for row in file[1:]:
        name = []
        name = ' '.join(row[:2])
        if name not in duplicate.keys():
            duplicate[f'{name}'] = row
        else:
            data_list = duplicate[name]
            merge_list = []
            count = -1
            for data in row:
                count += 1
                if data == '':
                    merge_list.append(data_list[count])
                else:
                    merge_list.append(data)
            duplicate[f'{name}'] = merge_list
    merged_file = [merged_lists for merged_lists in duplicate.values()]
    return merged_file


def write_file(file):
    with open('phonebook.csv', 'w', newline='', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(file)
        return


if __name__ == '__main__':
    print(read_file())
    print(merge_duplicates(reform_names(reform_number(read_file()))))
    file = merge_duplicates(reform_names(reform_number(read_file())))
    write_file(file)
