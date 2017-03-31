
import os
import hashlib
from zipfile import ZipFile
#import magic    не встала

def unpack():
    for file in os.listdir('files'):
        if str(file[-3:]) == 'zip':
            dir = 'files/' + str(file)
            with ZipFile(dir, 'r') as ziparc:
                for filename in ziparc.filelist:
                    fname = filename.filename
                    if fname.split('/')[1]:
                        if fname.split('/')[1] == 'parts.md5':
                            data = ziparc.read(fname)
                            with open('files/{}'.format(fname.split('/')[1]),
                                      'ab') as outF:
                                outF.write(data)
                        elif not os._exists(fname):
                            data = ziparc.read(fname)
                            with open('files/{}'.format(fname.split('/')[1]),
                                      'wb') as outF:
                                outF.write(data)

def get_list():
    list = []
    for file in os.listdir('files'):
        if not file.startswith('parts'):
            path = 'files/{}'.format(file)
            with open(path, 'rb') as f:
                data = f.readline()
                h = hashlib.md5()
                h.update(data)
                hash = h.hexdigest()
                list.append((path, hash, data))
    return list


def collect():
    with open('files/parts.md5', 'r') as f:
        for line in f:
            for l in get_list():
                if l[1] == line.strip():
                    with open('!file', 'ab') as f:
                        f.write(l[2])


# def destroy(name, length):
    # print(os.path.getsize(name))
    # with open(name, 'rb') as f:
    #     print(len(f.read()))
    #     # for i in range(len(f.read())):
    #     #     print(f.read(i))
    #     # while os.stat(name).st_size < length:
    #     #         f.write(b'Hi')

# print(magic.from_file(collect()))

unpack()
collect()
#destroy('!file', 1024)





