import json
import pytest
from jsonbin import JSONBin, MARK

KEY_INFO = {
    # compress these by changing '"45.123456"' to '45.1234'
    # no need to decompress the compressed value, hence None
    'lat': (lambda x: float("%.4f" % float(x)), None),
    'lon': (lambda x: float("%.4f" % float(x)), None),
}
# keys to compress with unmodified values
for key in 'name msg tmp cnd dnhdop cnd_tmp_n'.split():
    KEY_INFO[key] = None
# gpstime deliberately excluded to test unknown keyhandling
DEMO_JSON = {
    "lon": "-92.003145", "gpstime": "2017-09-23 10:24:15", "lat": "46.839547",
    "dnhdop": "3,8,1.26", "cnd_tmp_n": 21, "tmp": 1584.524, "msg": "BAD LINE: ",
    "cnd": 1709.571, "name": "o"
}

@pytest.fixture
def jb():
    return JSONBin(key_info=KEY_INFO)

@pytest.fixture
def answer():
    return MARK*len(KEY_INFO) + b'T' + MARK + b'2' + MARK

def test_compress_dict(jb, answer):
    """test_compress - test compression"""
    assert jb.compress({'T':2}) == answer

def test_compress_json(jb, answer):
    """test_compress - test compression"""
    compressed = jb.compress(json.dumps({'T':2}))
    assert compressed == answer

def test_compress_key(jb, answer):
    """test_compress - test compression"""
    key = sorted(KEY_INFO)[2]
    compressed = jb.compress(json.dumps({'T':2, key: 4.77}))
    answer = answer[:2] + '4.77'.encode('ascii') + answer[2:]
    assert compressed == answer

def test_decompress_dict(jb):
    """test_compress - test compression"""
    for key in DEMO_JSON:
        if key in KEY_INFO and KEY_INFO[key]:
            DEMO_JSON[key] = KEY_INFO[key][0](DEMO_JSON[key])
    assert jb.decompress(jb.compress(DEMO_JSON), return_dict=True) == DEMO_JSON

def test_init(jb):
    """test_init - test making a JSONBin object"""
    keys = sorted(KEY_INFO)
    assert jb.keys.index(keys[2]) == 2

def main():
    print(len(json.dumps(DEMO_JSON)))
    print(len(jb().compress(DEMO_JSON)))
    print(json.dumps(DEMO_JSON))
    print(jb().compress(DEMO_JSON))
    print(jb().decompress(jb().compress(DEMO_JSON)))

if __name__ == '__main__':
    main()
