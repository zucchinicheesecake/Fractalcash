import hashlib

class FractalHash:
    def __init__(self):
        pass

    def compute(self, data: bytes) -> str:
        # Dummy implementation: SHA256 of SHA1 of MD5
        md5 = hashlib.md5(data).digest()
        sha1 = hashlib.sha1(md5).digest()
        final = hashlib.sha256(sha1).hexdigest()
        return final
