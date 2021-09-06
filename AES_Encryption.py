import base64
import Crypto
from Crypto.Cipher import AES

key = 'A#d3454%&48t49*k'.encode('utf8')
#key = '1234'
#print(key)
BS = 16
pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
unpad = lambda s : s[0:-ord(s[-1:])]
def encrypt(raw):
    print('raw----> ',raw)
    raw = pad(raw) # iv = Random.new().read(AES.block_size) # iv= bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ,0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00]) # print(iv)
    print("key",key,type(key))
    cipher = AES.new(key, AES.MODE_CBC, key)
    return base64.b64encode(cipher.encrypt(raw))

def decrypt(enc):
    #print("enc1",enc)
    enc = base64.b64decode(enc)
    #print("enc2", enc)
    cipher = AES.new(key, AES.MODE_CBC, key)
    return (unpad(cipher.decrypt(enc)))

print(encrypt('{"platform":"web","userID":"101","password":"1234"}'))

# import hashlib
# from Crypto import Random
# from Crypto.Cipher import AES
#
# class AESCipher(object):
#
#     def __init__(self, key):
#         self.bs = 32
#         self.key = hashlib.sha256(key.encode()).digest()
#
#     def encrypt(self, raw):
#         raw = self._pad(raw)
#         iv = Random.new().read(AES.block_size)
#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return base64.b64encode(iv + cipher.encrypt(raw))
#
#     def decrypt(self, enc):
#         enc = base64.b64decode(enc)
#         iv = enc[:AES.block_size]
#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
#
#     def _pad(self, s):
#         return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
#
#     @staticmethod
#     def _unpad(s):
#         return s[:-ord(s[len(s)-1:])]

