# jsonbin - domain specific JSON compression

A simple approach to JSON compression when the keys are known in advance.

This is only intended for low bandwidth situations where you want compression
"on the wire", e.g. communicating with a PyBoard over a radio link:

```python
# sender
radio.write(jb.compress(my_data))

# receiver
data = jb.decompress(radio1.read())
```

I.e. the compressed format's not intended for writing to a file
or anything other than transient tranmission.

It's “domain specific” because it requires both ends have a
synchronized list of fields like this:

```python
KEY_INFO = {
    # compress these by changing '"45.123456"' to '45.1234'
    # no need to decompress the compressed value, hence None
    'lat': (lambda x: float("%.4f" % float(x)), None),
    'lon': (lambda x: float("%.4f" % float(x)), None),
}
# keys to compress with unmodified values
for key in 'name msg tmp cnd dnhdop cnd_tmp_n'.split():
    KEY_INFO[key] = None
```

In the test example it gets about 50% compression:
```
182 bytes: {"lon": "-92.003145", "gpstime": "2017-09-23 10:24:15", "lat": "46.839547",
  "dnhdop": "3,8,1.26", "cnd_tmp_n": 21, "tmp": 1584.524, "msg": "BAD LINE: ",
  "cnd": 1709.571, "name": "o"}
96 bytes: b'1709.571\x0021\x00"3,8,1.26"\x0046.8395\x00-92.0031\x00"BAD LINE: "\x00
  "o"\x001584.524\x00gpstime\x00"2017-09-23 10:24:15"\x00'
```

It would be 89 bytes but the gpstime key was deliberately treated as an unknown
key for testing purposes.
