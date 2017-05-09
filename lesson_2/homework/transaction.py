from datetime import datetime
import struct


def pack_to_bytes(*args):
    '''
    На вход берем пакет байтов, преобразованную в нужный формат дату
    или другие числа и строку.
    На выходе получаем упакованные в пакет байты.
    :param args:
    :return:
    '''
    packet = b''
    for i in args:
        if type(i) == str:
            for j in i:
                packet += struct.pack('B', ord(j))
        else:
            blen = len(bin(i)[2:])
            if blen % 8:
                mask = (blen // 8) * 8
            else:
                mask = blen
            if mask >= 8:
                for j in range(mask, 0, -8):
                    packet += struct.pack('B', (i >> j) & 255)
            packet += struct.pack('B', i & 255)
    return packet


def date_trans(date):
    '''
    Получаем тукущую дату.
    Отдаем день 2 байта и секунды 3 байта переформатированные.
    :return:
    >>> len(bin(date_trans(datetime.now())))
    40
    '''
    # date = datetime.now()
    year = date.year - 2000
    sec = date.hour * 3600 + date.minute * 60 + date.second
    today = (year << 9) | (date.month << 5) | (date.day & 31)
    tdate = today << 24 | sec
    return tdate


def decode(pack):
    '''
    На вход получаем пакет.
    На выходе раскодируем его в кортеж из данных транзакции и дату.
    :param pack: 
    :return:
    >>> decode(b'zz\\x07\"\\xa9\\x01\\x00K\\x00\\x03')
    ((0, 3), datetime.datetime(2017, 5, 9, 18, 13, 31))
    '''
    packlen = struct.unpack_from('B', pack, 2)[0] + 3
    fmt = 'B' * packlen
    depack = struct.unpack(fmt, pack)
    i = depack.index(122)
    if depack[i] == depack[i + 1] == 122:
        bdate = depack[i + 3] << 8 | depack[i + 4]
        year = (bdate >> 9) + 2000
        month = (bdate >> 5) & 15
        day = bdate & 31
        bsec = depack[i + 5] << 16 | depack[i + 6] << 8 | depack[i + 7]
        hours = bsec // 3600
        minuts = (bsec - (3600 * hours)) // 60
        sec = bsec - 3600 * hours - minuts * 60
        date = datetime(year, month, day, hours, minuts, sec)
        btransaction = 0
        for j in range(i + 8, i + packlen):
            btransaction |= depack[j] << (
            8 * (packlen - 8) - 8 * (j - (i + 7)))
        ttype = (btransaction >> 96) & 3
        iddata = (btransaction >> 64) & (2 ** 32 - 1)
        sumdata = btransaction & (2 ** 64 - 1)
        if ttype:
            transaction = ttype, iddata, sumdata
        else:
            transaction = ttype, sumdata
    return transaction, date


class Transaction():
    def __init__(self, transaction, date=datetime.now()):
        self.date = date
        self.ttype = transaction[0]
        self.packlen = 6

        if self.ttype == 0:
            self.packlen += 1
            self.tdata = transaction[1]
            self.type_descr = 'Сервисная транзакция'
            if self.tdata == 0:
                self.tdata_descr = '{}: включение'.format(self.type_descr)
            elif self.tdata == 1:
                self.tdata_descr = '{}: перезагрузка'.format(self.type_descr)
            elif self.tdata == 2:
                self.tdata_descr = '{}: выключение'.format(self.type_descr)
            elif self.tdata == 3:
                self.tdata_descr = '{}: активация датчика X' \
                    .format(self.type_descr)
            elif self.tdata == 4:
                self.tdata_descr = '{}: блокировка, требуется инкассация' \
                    .format(self.type_descr)
            else:
                raise TypeError('Недопустимое значение данных транзакции')

        elif self.ttype == 1:
            self.packlen += 12
            self.tdata = (self.ttype << 96) | (transaction[1] << 64) | \
                         (transaction[2] & (2 ** 64 - 1))
            self.type_descr = 'Платёжная транзакция'
            self.tdata_descr = 'id организации для перевода средств: {}, ' \
                               'сумма транзакции в копейках: {}' \
                .format(transaction[1], transaction[2])

        elif self.ttype == 2:
            self.packlen += 12
            self.tdata = (self.ttype << 96) | (transaction[1] << 64) | \
                         (transaction[2] & (2 ** 64 - 1))
            self.type_descr = 'Инкассация'
            self.tdata_descr = 'id сотрудника-инкассатора: {}, ' \
                               'сумма инкассации в копейках: {}' \
                .format(transaction[1], transaction[2])

        else:
            raise TypeError('Недопустимое значение типа транзакции')

    def __str__(self):
        return 'Дата транзакции: {},  Тип транзакции: {}, Данные: {} ' \
            .format(self.date, self.type_descr, self.tdata_descr)

    def send(self):
        if self.ttype:
            return pack_to_bytes('z', 'z', self.packlen,
                                 date_trans(self.date), self.tdata)
        else:
            return pack_to_bytes('z', 'z', self.packlen,
                                 date_trans(self.date), 0, self.tdata)


# # c = Transaction((1, 236231, 1999999), datetime(2017, 5, 6, 15, 00, 00))
# d = Transaction((0, 3), )
# # print(c)
# # print(c.send())
# # # print(c.packlen)
# print(d)
# print(d.send())
# # print(d.packlen)
# print(decode(d.send()))
# f = Transaction(decode(d.send())[0], decode(d.send())[1])
# print(f)
#print(pack_to_bytes('a', 1024))