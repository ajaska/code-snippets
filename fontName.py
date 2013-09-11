import struct

def fontName(path):
    tags = {}
    ntoffset, offset, records = None, None, None
    with open(path, 'rb') as f:
        data = f.read()

    tables = struct.unpack_from('>H', data, 4)[0]
    for i in range(tables):
        tag = data[i*16 + 12:i*16 + 16]
        if tag == b"name":
            ntoffset = struct.unpack_from('>I', data, i*16 + 20)[0]
            offset = struct.unpack_from('>H', data, ntoffset + 4)[0]
            records = struct.unpack_from('>H', data, ntoffset + 2)[0]
            break

    if ntoffset is None:
        return tags

    storage = ntoffset + offset
    for i in range(records):
        id = struct.unpack_from('>H', data, ntoffset + i*12 + 12)[0]
        length = struct.unpack_from('>H', data, ntoffset + i*12 + 14)[0]
        offset = struct.unpack_from('>H', data, ntoffset + i*12 + 16)[0]
        value = data[storage + offset:storage + offset + length]
        value = ''.join([chr(x) for x in value if x != 0])
        tags[id] = value

    return tags[1] if 1 in tags else None
