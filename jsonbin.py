import json

MARK = b'\x00'
class JSONBin(object):
    """JSONBin - Domain specific JSON<->binary compression"""

    def __init__(self, key_info):
        """
        Args:
            key_info (dict): info. on known keys, value is function to compress/decompress, or None
            """
        self.key_info = key_info
        self.keys = sorted(key_info)

    def compress(self, data):
        """compress - compress dict or json

        Args:
            data (dict|str): data to compress
        Returns:
            bytes: compressed data
        """
        if not hasattr(data, 'keys'):
            data = json.loads(data)
        ans = []
        for key in self.keys:
            if key in data:
                if self.key_info[key] is not None:
                    value = self.key_info[key][0](data[key])
                else:
                    value = data[key]
                value = json.dumps(value)
                ans.append(value.encode('ascii'))
            ans.append(MARK)
        for key in data:
            if key in self.keys:
                continue
            ans.extend([
                key.encode('ascii'),
                MARK,
                json.dumps(data[key]).encode('ascii'),
                MARK
            ])
        return b''.join(ans)
    def decompress(self, data, return_dict=False):
        """compress - compress dict or json

        Args:
            data bytes: data to decompress
        Returns:
            dict|str: decompressed data as dict or JSON
        """
        ans = {}
        for key in self.keys:
            if not data.startswith(MARK):
                value = json.loads(data[:data.index(MARK)])
                if self.key_info[key] is not None and self.key_info[key][1] is not None:
                    value = self.key_info[key][1](value)
                ans[key] = value
            data = data[data.index(MARK)+1:]
        while data:
            key = data[:data.index(MARK)].decode('ascii')  # or utf-8?
            data = data[data.index(MARK)+1:]
            ans[key] = json.loads(data[:data.index(MARK)])
            data = data[data.index(MARK)+1:]
        if return_dict:
            return ans
        return json.dumps(ans)


