
from Crypto.Cipher import Blowfish
from Crypto import Random
from struct import pack
import binascii

bs = Blowfish.block_size
#print('bs=== ',bs)
key = b'04B915BA43FEB5B6'
iv = Random.new().read(bs)
print("iv ____________________ ",iv)

plaintext = b'Admin@123'
def encryption(raw_msg):
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    plen = bs - divmod(len(raw_msg),bs)[1]
    padding = [plen]*plen
    padding = pack('b'*plen, *padding)
    msg = iv + cipher.encrypt(raw_msg + padding)
    enc_msg = binascii.hexlify(msg)
    #print("enc_msg: ",enc_msg)
    return enc_msg

def decryption(raw_msg):
    # print('raw: ',raw_msg)
    ciphertext = binascii.unhexlify(raw_msg)
    #print(ciphertext)
    iv = ciphertext[:bs]
    ciphertext = ciphertext[bs:]
    cipher= Blowfish.new(key, Blowfish.MODE_CBC, iv)
    msg = cipher.decrypt(ciphertext)
    last_byte = msg[-1]
    msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]
    dec_msg = repr(msg)
    #print("dec_msg: ",dec_msg)
    return dec_msg

# enc = encryption(b'Sups@123')
# print("encp: ",enc)
# dec = decryption(b'c11ef9db14d6fb0ed19eb2349d11ad87')
# print("decp: ",dec)
#
# u = encryption(b'Prashant@2')
# print("u--->",u)
# print(decryption(u))
# p = decryption(b'70ef8635e577449d3bfbd33f60b64837')
# print("p--------->",p)

# username = mobitrail_user
# password =  mobi@123
enc = encryption(b'haris@123')
print("encrypt------->",enc)
print("decrpty------>"+decryption(enc))