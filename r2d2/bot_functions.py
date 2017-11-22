from .morze import *


def sort_string(s):
    s = remove_spaces(s)
    s = ''.join(sorted(s))
    return s


def remove_spaces(s):
    s = rl_strip(s)
    s = s.lower()
    s = s.replace('\'', '')
    s = s.replace('/', '')
    s = s.replace(' ', '')
    s = s.replace('-', '')
    return s


def rl_strip(s):
    s = s.rstrip()
    s = s.lstrip()
    s = s.strip()
    return s


def string_like(s):
    string_list = ['%']
    for c in s:
        string_list.append(c + '%')
    return ''.join(string_list)


def string_finder(s):
    s = rl_strip(s)
    s = s.lower()
    s = s.replace('*', '%')
    s = s.replace('+', '%')
    s = s.replace('?', '_')
    s = s.replace('.', '_')
    return s


def check_morze(s):
    news = ''
    s = s.lower()
    if len(s) < 5:
        return 0
    for c in s:
        if c not in news and c != ' ':
            news += c
            if len(news) == 3:
                return 0
    return news


def replace_morze(s, mask):
    s = s.lower()
    result = []
    result.append(s.replace(mask[0], '-'))
    result[0] = result[0].replace(mask[1], '.')
    result.append(s.replace(mask[0], '.'))
    result[1] = result[1].replace(mask[1], '-')
    return result


def ukr_morze(s):
    result = ''
    morze_list = s.split(' ')
    for key in morze_list:
        if key in morze_ukr:
            result += morze_ukr.get(key)
    return result


def rus_morze(s):
    result = ''
    morze_list = s.split(' ')
    for key in morze_list:
        if key in morze_ukr:
            result += morze_rus.get(key)
    return result


def eng_morze(s):
    result = ''
    morze_list = s.split(' ')
    for key in morze_list:
        if key in morze_ukr:
            result += morze_eng.get(key)
    return result


def check_abc(s):
    test = s.replace(' ', '')
    if not test.isdigit():
        return 0
    num_list = s.split(' ')
    for num in num_list:
        if int(num) > 33:
            return 0
        if int(num) == 0:
            return 0
    return 1


def ukr_abc(s):
    result = ''
    abc_list = s.split(' ')
    for key in abc_list:
        if int(key) <= len(abc_ukr):
            result += abc_ukr[int(key) - 1]
        else:
            return ''
    return result


def rus_abc(s):
    result = ''
    abc_list = s.split(' ')
    for key in abc_list:
        if int(key)<=len (abc_rus):
            result += abc_rus[int(key)-1]
        else:
            return ''
    return result


def eng_abc(s):
    result = ''
    abc_list = s.split(' ')
    for key in abc_list:
        if int(key)<=len (abc_eng):
            result += abc_eng[int(key)-1]
        else:
            return ''
    return result

def caesar (s,bot,msg):
    if s.find(' ')!=-1:
        s = s[s.find(' '):]
        if s[len(s)-1:].isdigit():
            num = s[len(s)-1:]
            s_copy = s
            s = s[:len(s)-1]
        else:
            return 'Невірно набрана команда'
        temp_num = s_copy[len(s_copy)-2:].strip() #переробити це уродство
        if temp_num.isdigit():
           num = s_copy[len(s_copy)-2:].strip()
           s = s_copy[:len(s_copy)-2]
        s = s.replace (num,'')
        s = s.strip()
        s = s.upper()
        result = ['','','',num]
        i = 0
        for ch in s:
            if ch in abc_ukr:
                result[0]+=abc_ukr[(abc_ukr.index(ch)-int(num)+len(abc_ukr))%len(abc_ukr)]
            else:
                if ch in [' ',',','.',':','!','?','\'','-']:
                    result[0]+=ch
                else:
                    result[0]=''
        for ch in s:
            if ch in abc_rus:
                result[1]+=abc_rus[(abc_rus.index(ch)-int(num)+len(abc_rus))%len(abc_rus)]
            else:
                if ch in [' ',',','.',':','!','?','\'','-']:
                    result[1]+=ch
                else:
                    result[1]=''
        for ch in s:
            if ch in abc_eng:
                result[2]+=abc_eng[(abc_eng.index(ch)-int(num)+len(abc_eng))%len(abc_eng)]
            else:
                if ch in [' ',',','.',':','!','?','\'','-']:
                    result[2] +=ch
                else:
                    result[2]=''
        for i in range(len(result)):
            if len(result[i])!=len(s):
                result[i]=''
        result [3] = num
        return result
    else:
        return 'Невірно набрана команда'
