from datetime import datetime
import pytest

import transaction

# a = [1, 2, 3]
# for i in range(len(a)):
#     @pytest.mark.parametrize("data, expected", [a[i]])

@pytest.mark.parametrize("data, expected",
                         [('a', b'a'),
                          (('a', 1024), b'a\x04\x00')])
def test_pack_to_bytes(data, expected):
    if type(data) == tuple:
        assert transaction.pack_to_bytes(data[0], data[1]) == expected, \
            'Ошибка упаковки данных'
    else:
        assert transaction.pack_to_bytes(data) == expected, \
            'Ошибка упаковки данных'


@pytest.mark.parametrize("date, expected",
                         [(datetime(2017, 5, 6, 15, 00, 00), 148813959920)])
def test_date_trans(date, expected):
    assert transaction.date_trans(date) == expected, 'Ошибка обработки даты'


i1 = transaction.Transaction((0, 3), )
i2 = transaction.Transaction((1, 236231, 1999999),
                             datetime(2017, 5, 6, 15, 0, 0))


@pytest.mark.parametrize("pack, expected",
                         [(i1.send(), (transaction.decode(i1.send())[0],
                                       transaction.decode(i1.send())[1])),
                          ((i2.send(), (transaction.decode(i2.send())[0],
                                        transaction.decode(i2.send())[
                                            1])))]
                         )
def test_decode(pack, expected):
    assert transaction.decode(pack) == expected, 'Ошибка раскодирования'
