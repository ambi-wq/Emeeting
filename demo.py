import base64
import calendar
import datetime
import io
import PyPDF2 as PyPDF2
from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter
from django.core.files.storage import FileSystemStorage
#from openpyxl.compat import file
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

#settings.configure()

# pdfarr = [{'agtitle': '1.Leave of Absence,for this meeting', 'agdoc': 'agenda_level0.pdf'},
#           {'ssagtitle': '1.(a)(i)Board Operating Procedures', 'ssagdoc': 'Userguide_level2.pdf'},
#           {'sagtitle': '2.(a)Quarterly Reports', 'sagdoc': 'main_level1.pdf'},
#           {'sagtitle': '2.(b)Monthly Reports', 'sagdoc': 'Userguide4_level1.pdf'}]
#
# pdffile = []
# indextitle = []
#
# for pdf1 in pdfarr:
#     for i in pdf1.keys():
#         if "agdoc" in i:
#             val = pdf1[i]
#             pdffile.append(val)
#         elif "sagdoc" in i:
#             pdffile.append(pdf1[i])
#         elif "ssagdoc" in i:
#             pdffile.append(pdf1[i])
#         elif "agtitle" in i:
#             indextitle.append(pdf1[i])
#         elif "sagtitle" in i:
#             indextitle.append(pdf1[i])
#         elif "ssagtitle" in i:
#             indextitle.append(pdf1[i])
#         else:
#             pass
#
# print(pdffile)
# print(indextitle)
#
# ######################  index page no part is complete ###########################################
#
# # page_no = []
# # for p in pdffile:
# #     reader = PyPDF2.PdfFileReader(open("D:/Emeeting/EmeetingApp/static/resources/Board Committee/1/"+p, 'rb'))
# #     NUM_OF_PAGES = reader.getNumPages()
# #     page_no.append(NUM_OF_PAGES)
# # print(page_no)
# #
# # count = 0
# # indexarr = []
# # for i in page_no:
# #     print(count)
# #     if count == 0:
# #         count += 1
# #         indexarr.append(count)
# #         count = count + i
# #     else:
# #         indexarr.append(count)
# #         count = count + i
# #
# # print(indexarr)
#
#
#
# # merger = PdfFileMerger()
#
# # merger.append(PdfFileReader(file("D:/Emeeting/EmeetingApp/static/resources/Board Committee/1/agenda_level0.pdf", "rb")))
# # merger.append(PdfFileReader(file("D:/Emeeting/EmeetingApp/static/resources/Board Committee/1/main_level1.pdf", "rb")))
#
# # basepath = "D:/Emeeting/EmeetingApp/"
# #
# #
# # fs = FileSystemStorage()
# # merger = PdfFileMerger()
# # for pdf in pdffile:
# #     merger.append(open(basepath+"static/resources/Board Committee/1/"+pdf, "rb"))
# #
# # with open(basepath+"static/resources/Board Committee/1/Merge.pdf", "wb") as fout:
# #     merger.write(fout)
#
# p = "Merge.pdf"
# reader = PyPDF2.PdfFileReader(open("D:/Emeeting/EmeetingApp/static/resources/Board Committee/1/"+p, 'rb'))
# NUM_OF_PAGES = reader.getNumPages()
# print(NUM_OF_PAGES)
#
# outputStream = open("D:/Emeeting/EmeetingApp/static/resources/Board Committee/1/FinalPagenumber.pdf", "wb")
# output = PdfFileWriter()
#
# for i in range(NUM_OF_PAGES):
#     page_no_pdf = i + 1
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=letter)
#     can.drawString(225, 20, "Page"+" "+str(page_no_pdf))
#     can.save()
#
#     packet.seek(0)
#     new_pdf = PdfFileReader(packet)
#     existing_pdf = PdfFileReader(open("D:/Emeeting/EmeetingApp/static/resources/Board Committee/1/"+p, "rb"))
#
#     page = existing_pdf.getPage(i)
#     page.mergePage(new_pdf.getPage(0))
#     output.addPage(page)
#
#     output.write(outputStream)
#
# outputStream.close()



import binascii
# import re
# from Crypto.Cipher import AES
#
#
# class AESCBC:
#     def __init__(self):
#         self.key = '3132333400000000'.encode('utf8') # defined key value
#         self.mode = AES.MODE_CBC
#         self.bs = 16  # block size
#         self.PADDING = lambda s: (s + bytes((self.bs - len(s) % self.bs)* chr(self.bs - len(s) % self.bs), 'utf-8') )
#
#         #self.PADDING = lambda s: bytes(s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs),'utf-8')
#         #lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
#
#     def encrypt(self, text):
#         print('text------->',text)
#         generator = AES.new(self.key, self.mode,self.key)  # The key here is the same as IV, which can be defined according to its own value.
#
#         #generator = generator1.encode('utf-8')
#         crypt = generator.encrypt(self.PADDING(text))
#         crypted_str = base64.b64encode(crypt) #outputBase64
#         #crypted_str = binascii.b2a_hex(crypt)  # output Hex
#
#
#         result = crypted_str.decode()
#         return result
#
#
#     def decrypt(self, text):
#         generator = AES.new(self.key, self.mode, self.key)
#         text += (len(text) % 4) * '='
#         decrpyt_bytes = base64.b64decode(text) #outputBase64
#         #decrpyt_bytes = binascii.a2b_hex(text)  # output Hex
#
#         meg = generator.decrypt(decrpyt_bytes)
#         # Remove the illegal characters after decoding
#         try:
#             result = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', meg.decode())
#         except Exception:
#             Result = 'Decoding failed, please try again!'
#         return result
#
# if __name__ == '__main__':
#     aes = AESCBC()
#
#     to_encrypt1 = 'prashant'
#     to_encrypt = to_encrypt1.encode('utf-8')
#     print('enc-----------> ',to_encrypt,type(to_encrypt))
#     enc_text = aes.encrypt(to_encrypt)
#     print("enc text----------> ",enc_text)
#
#     dec_text = aes.decrypt(enc_text)
#     print("dec text----------> ", dec_text,len(dec_text))
#
#     # dec_text1 = aes.decrypt(dec_text)
#     # print("dec text1----------> ", dec_text1)
#     #to_decrypt = '31f45bc15c28b3dffb7886d86ae0136d'
#     to_decrypt = 'XZ5PfVRHoOO7tVpkxc24eA=='
#     print(len(to_decrypt))
#     print("\n\n")

    # to_encrypt = '123456'
    # to_decrypt = '31f45bc15c28b3dffb7886d86ae0136d'

    # print("\n before encryption: {0}\n encrypted: {1}\n".format(to_encrypt ))
    # print("Before decryption: {0}\nafter decryption: {1}".format(to_decrypt, aes.decrypt(to_decrypt)))







#
# from rijndael.cipher import crypt
# from rijndael.cipher.blockcipher import MODE_CBC
# from pkcs7 import PKCS7Encoder
#
#
# class Rijndael():
#         def __init__(self, key, iv):
#             self.KEY = key
#             self.IV = iv
#             #self.BLOCKSIZE = 32
#             self.BLOCKSIZE = 16
#
#         def encrypt(self, plain_text):
#             print('plain text-------',plain_text)
#             rjn = crypt.new(self.KEY, MODE_CBC, self.IV, blocksize=self.BLOCKSIZE)
#             encoder = PKCS7Encoder()
#             #text = plain_text.decode('utf8')
#             pad_text = encoder.encode(plain_text)
#             print('p-------',pad_text)
#             temp = rjn.encrypt(pad_text)
#             print("================",temp)
#             return rjn.encrypt(pad_text).encode()
#
#         def decrypt(self, cipher_text):
#             rjn = crypt.new(self.KEY, MODE_CBC, self.IV, blocksize=self.BLOCKSIZE)
#             cipher_text = cipher_text.decode()
#             return rjn.decrypt(cipher_text)
#
#
# r = Rijndael(b'4950515200000000',
#                  b'4950515200000000')
# test_text = b"this is a test"
#
#
#
#
# encrypt = r.encrypt(test_text)
# decrypt = r.decrypt(encrypt)
# print(test_text)
# print('enc: ',encrypt)
# print('dec: ',decrypt)


# print("=======================================================================================================")
# from pkcs7 import PKCS7Encoder
from Crypto.Cipher import AES
# import codecs
#
# secret_text = 'vedanti'.encode('utf8')
# #key = '3132333400000000'
mode = AES.MODE_CBC
#iv = bytes(('\x00' * 16),encoding='utf8')


# iv1 = "1234".encode('utf8')
# iv = (codecs.encode(iv1, 'hex_codec'))
# iv11 = iv.decode('utf8')
# iv11 = iv11+'00000000'
# iv = iv11.encode('utf8')
# print('iv1: ',iv)
#
# key1 = "1234".encode('utf8')
# key = (codecs.encode(key1, 'hex_codec'))
# key11 = key.decode('utf8')
# key11 = key11+'00000000'
# key = key11.encode('utf8')
# print('key: ',key)


#
# print("\n")
#
# key = '4950515200000000'.encode('utf8')
# iv =  '4950515200000000'.encode('utf8')
#
# encoder = PKCS7Encoder()
# padded_text = encoder.encode(secret_text)
#
# e = AES.new(key, mode, iv)
#
# cipher_text = e.encrypt(padded_text)
# #nELZ2aApVv/oPhhxuNrEcg==
#
#
# #cipher_text1 = e.decrypt(cipher_text)
#
#
# print('enc--------->  ',base64.b64encode(cipher_text))


#print('dec--------->  ',base64.b64encode(cipher_text1))




print("="*50)





#
# import base64
#
# from Crypto.Cipher import AES
# from Crypto.Protocol.KDF import PBKDF2
# from Crypto.Util.Padding import pad
#
#
# class AESCipher(object):
#
#     def __init__(self, key, interactions=1000):
#         self.bs = AES.block_size
#         self.key = key
#         self.interactions = interactions
#
#     def encrypt(self, raw):
#         nbytes = [0x49, 0x76, 0x61, 0x6e, 0x20, 0x4d, 0x65, 0x64, 0x76,
#                   0x65, 0x64, 0x65, 0x76]
#
#         salt = bytes(nbytes)
#         keyiv = PBKDF2(self.key, salt, 48, self.interactions)
#         key = keyiv[:32]
#         iv = keyiv[32:48]
#
#         cipher = AES.new(key, AES.MODE_CBC, iv)
#
#         encoded = raw.encode('utf-16le')
#         encodedpad = pad(encoded, self.bs)
#
#         ct = cipher.encrypt(encodedpad)
#
#         cip = base64.b64encode(ct)
#         return self._base64_url_safe(str(cip, "utf-8"))
#
#     def _base64_url_safe(self, s):
#         return s.replace('+', '-').replace('/', '_').replace('=', '')
#
# enc = AESCipher("1234")
# dec = enc.encrypt("vedanti")
# print('enc ---->', dec)

#nELZ2aApVv/oPhhxuNrEcg==
a = 2,3
print(a)