import datetime

def date_bin(date):
    '''
    На вход поступеает datetime.datetime.now().
    По году ограничение до 2999.
    На выходе бинарная строка длиной 40 символов.
    >>> 2017-04-03 00:22:15.851022
    0010001010000011000000000000010100110111
    '''
    return bin(date.year-2000)[2:].zfill(7) + bin(date.month)[2:].zfill(4) + \
           bin(date.day)[2:].zfill(5) + \
           bin(date.hour*3600+date.minute*60+date.second)[2:].zfill(24)

def bin_to_bytes(bdate):
    '''
    На вход поступает бинарная строка
    На выходе строка байтов
    >>> 0010001010000011000000000000010100110111
    b'"\x83\x00\x057'
    '''
    list = []
    for i in range(8, len(bdate)+8, 8):
        list.append(int(bdate[i-8:i], 2))
    return bytes(list)




date = datetime.datetime.now()
print(date)
print(date_bin(date), len(date_bin(date)))
bdate = date_bin(date)
print(bin_to_bytes(bdate))
rez = bytes([int(bdate[:8], 2), int(bdate[8:16], 2), int(bdate[16:24], 2), int(bdate[24:32], 2), int(bdate[32:], 2)])
print(rez, type(rez))