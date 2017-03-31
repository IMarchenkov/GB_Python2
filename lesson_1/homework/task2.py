import hashlib

def get_hash(line, fhash):
    if fhash == 'sha1':
        h = hashlib.sha1()
    elif fhash == 'md5':
        h = hashlib.md5()
    elif fhash == 'sha512':
        h = hashlib.sha512()
    h.update(line)
    return h.hexdigest()

with open('need_hashes.csv', 'r', ) as f:
    for line in f:
        print(get_hash(line.split(';')[0].encode('cp1251'),
                       line.split(';')[1]))
