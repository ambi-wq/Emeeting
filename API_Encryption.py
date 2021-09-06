import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pkcs7 import PKCS7Encoder

import json

class Encryption:

    def encryptString(self, s):
        #print("encrypt input ---->", s)

        plainTextBytes = bytearray(s, encoding="utf-8")
        #print(plainTextBytes)
        #print("plainTextBytes----->", [x for x in bytearray(s, "utf_8")])
        keyBytes = self.getKeyBytes("1234")
        encryptedString = self.encrypt1(plainTextBytes, keyBytes, keyBytes,s)
        print("encryptedString------------>",encryptedString)
        es = encryptedString.decode("utf-8")
        print("encrypt output------------->",es)
        #decryptString = self.decrypt1(es, keyBytes, keyBytes)
        return es

    def decryptString(self, enc):
        print("decrypt input ---->", enc)
        keyBytes = self.getKeyBytes("1234")
        decryptString = self.decrypt1(enc, keyBytes, keyBytes)
        print("decryptstring---------->",decryptString)
        ds = decryptString.decode("utf-8")
        print(" decrypt output------------->", ds)
        return ds

    def getKeyBytes(self, key):
        #print("+++++++++++++++++getKeyBytes+++++++++++++++++")
        #print("key===>", key)
        keyBytes = bytearray(16)
        #print("keyBytes------------->", [x for x in keyBytes])
        parameterKeyBytes = bytearray(key, encoding="utf-8")
        #print("parameterKeyBytes----->", [x for x in parameterKeyBytes])
        minval = min(len(parameterKeyBytes), len(keyBytes))
        keyBytes = self.array_copy(parameterKeyBytes, 0, keyBytes, 0, minval)
        #print("array copy of keyBytes------------->", [x for x in keyBytes])
        return keyBytes

    def array_copy(self,src: bytes, src_pos: int, dest: bytes, dest_pos: int, length: int) -> bytes:
        #print("+++++++++++++++++++array_copy+++++++++++++++++++++")
        # print("src-------->",src)
        # print("src_pos----->",src_pos)
        # print("dest----->",dest)
        # print("dest_pos---------->",dest_pos)
        # print("length-------->",length)
        #final = dest[:dest_pos] + src[src_pos:length] + dest[dest_pos + length:]
        #print("final----->",[x for x in final])
        return dest[:dest_pos] + src[src_pos:length] + dest[dest_pos + length:]

    def encrypt1(self,plainText, key, initialVector,raw):
        print("raw111:   ", raw)

        raw = PKCS7Encoder().encode(raw)
        print("raw:   ",raw)
        key = bytes(key)
        cipher = AES.new(key, AES.MODE_CBC, initialVector)
        #print(cipher)
        return base64.b64encode(cipher.encrypt(raw.encode("utf8")))


    def decrypt1(self,enc,key, initialVector):
        print("decrypt1")

        enc = base64.b64decode(enc)
        print("dec enc--> ",enc)
        key = bytes(key)
        cipher = AES.new(key, AES.MODE_CBC, initialVector)
        print("dec cypher--->",cipher)
        data = unpad(cipher.decrypt(enc),16)
        print(data)
        #return unpad(cipher.decrypt(enc),16)
        return data


def main1():
    object = Encryption()

    # print("\n")
    #enc1 = object.encryptString('{"response":"<info><agenda name=\"1.sample agenda\" pdf=\"\" url=\"\" level=\"0\" desc=\"\" id=\"95\" v=\"0\" srno=\"1\" colorname=\"\" colorcode=\"\"><sagenda name=\"a) test subagenda\" pdf=\"\" url=\"\" level=\"1\" desc=\"\" id=\"104\" v=\"0\" srno=\"1\" colorname=\"\" colorcode=\"\"><ssagenda name=\"(i) document\" pdf=\"\" url=\"\" level=\"2\" colorname=\"\" colorcode=\"\" desc=\"\" id=\"103\" v=\"0\" srno=\"1.a\"></ssagenda></sagenda></agenda></info>","token":"supriya_yQrUy4Zv2EiCrUY1hUOuRLY23yNlOKOtW"}')
    # enc1= "blK3AdZLgJlWslximxZLvV1iZkKUoNPhfmhTdJ50Y9QPk9MpOBwBeakv8eWJxrEfk3CEDG4aTowYU68y9z5BqGhAhiTJfQBrGbkXxvJ+D7pO27vs+52e+PYZ0Uq9PVpRXle67aejVyRFapqEYrslPcI57agYoa/+o7OleTgBaUBRpf52t5jDj0LIlu+vundd"
    #object.decryptString(enc1)
   # object.encryptString("{"token":"supriya_yQrUy4Zv2EiCrUY1hUOuRLY23yNlOKOtW","response":["{"mid": "1", "title": "First Board Meeting - Draft MOM v2", "mom": "D:/project_bk_zips/emeetingadminpythonfiles_V/emeetingadminpythonfiles_V/Emeeting/EmeetingApp/static/resources/Board Committee/1/Sample_Document_20201013195329623.pdf", "version": "2", "momId": 2, "ExpiryDate": "10/13/2020 19:53:30"}","{"mid": "2", "title": "Second Board Meeting - Draft MOM v1", "mom": "D:/project_bk_zips/emeetingadminpythonfiles_V/emeetingadminpythonfiles_V/Emeeting/EmeetingApp/static/resources/Board Committee/2/Sample_Document_20201013195444531.pdf", "version": "1", "momId": 3, "ExpiryDate": "10/13/2020 19:54:44"}"]}")
#     object.decryptString("q1XBc1kpDMgwdF80wXzWUeNDJ3vSfnEjUZudti1c6R6udYFk4XN7MyY+NfdmATbEKK020kX7UiuoxHNxsPLuyPCjFLi3YE3Bodv/tMuBGRbKDhGVDitv+gsCuHJdu2e5fPl4mA0ynE9mwnQ/JzZqzgkCCwwLJ84WBHZXwtdi28gz0X/tZiHqpjeAX4AYl6679Tt1Ca6ddT1Die5H+OBHmQgPf3CJu362W+w6BxmfAZSGzmJmxNUFhr7xNMmt+3PhL1Iwm8559EipI/AW/oVvNIKDyoDoA51zUWnR7iSYwFDllwQEv2g8UTxHawntkAGR8VoQODj1nNyzE1ehEDhveLY1q+hXtWOp6+4NXgLWzLMCw1GDXBoozoRFH2J8ldlk9ytWmg5/5pLTNp9G+cUEwd5TxRBPpgoi/lKdXvzg+BiY37BsltJEid04Zg9pneKlhM+Q+9Kx56Rrfmvg895AESwhARSbxSz8ukc8mjzjlr+0kLIJ3EoJt06OCqYsn4N89RCMzpC9alKWUt+MdJrduycLkHARfDaVjlh1WxXj9U4MItde4hQ2OWG6NDEtl8/KHp5rZg3sTwdMXQVBTzujzhd8am8L5Oj+2rTo/5ip6cyMmS9L5p5+v5jDtOY78krWFTsvJStU0l2zHLp+e8ACO0lgI/VUozWaAa4V7feU1hKuySwRyqOvZ8kdNeLuAJogfFDmlDFRi/HVpzR15JWcfVWSkRGQsaUQ5NyHCdkz7OMfNrwugsulcg0FJf4uZbrveE80UYOpI8J0DIQ7QBWNsE8IPgIBNYSOjgKj9fODSILEQqjT0uVrVhkf4MlItH33PH6vx6vNWQ4mLvx2Fy6AK0pcWFZxsCRkbpAIPOLAxis41DeJfOxQTBPxjYHo6f5mkIvNHNM3UO4KKendMh9ipg==")
    #object.decryptString("K9jBE0+0ulCGDZGash95IqpIARrvKS7shueo5qoWqDnKvqr9UIQ0cpHGo+RFcbPiqhVcp5Fs7HvKgXVked1qv5wZrgQDyeyW0HzRm7/kU/nmn6EgCZLaQRLJ4Zqt0ee+Q9sJpWlGINGpzUUnYd4KeWIgoLWxVtmDekkmLgn138Qz6K4QO77E2Ylnos3L2u34hQxF0EinDQi5bsECbdh9ZSYOmaI0AxsL9U5li3+3NKBLH/SFd7D7zN95wzfm84CsUvvO3na7RFVR8UyEKcXdmy062ZUfGQQCKsemOxQ7bwZELqaWWY9fec7MHGTPC4nEjCFxpLr8kdoZFfJFOuRyeClCRhSl52BsWYgfRWV0bYwfScZXKJ5KJ9aJHEH9+o4rk3FEuWmE1G3NzS/hJ/yyue69n1cTK4bg0ffBSUz3lkrwAxSF59q0fBhJQ47GVMFwNCV2+6FN3Y6SvnLz6d8+SbDZmvYVb05hKwgh1VJh3xMvJlLVtFfzhx06iKLFMSD4NYRb/HazmTCZfhFkf7qmEcjFOZIn/cq4WtEoqgyZGXypxeWrcuRDP4FQru0zW1lGEcVRLIVXbTa8YEm/Unqb5ISy5awiEF3Cj3cR+Pwn9gkupAcJsdNu/Ryy108XwiovPCMb4InSoOM9B7fBaKUaUAliI27RKyLKXvxKnpTwi1K3h2YJ+HK6dIbXaKdj25c6KSwLpmsiEgWV1dx7SvWZFSrU1CNks4ihMWgARul34+t4iEJVbPUhvkYFo4y+r2LqPuni57TEpZAkDnUJ1y5Rczsx6MWt/FAaz+XyU7MGhyTWv6EUzwHkZMcuounP5v5j8mpJgcAI3n3jIDfEZvDfmNOEtjl6YdrkgIKH+V5J+Nvjpg9JMw36VMPqOiX9mhdHd9rsEykGdzgJDgIotwRkrQ==")
# q1XBc1kpDMgwdF80wXzWUeNDJ3vSfnEjUZudti1c6R6udYFk4XN7MyY+NfdmATbEKK020kX7UiuoxHNxsPLuyNSRsPxMtVuNWnX0mSBCWmj6iqXJt9kkrHCPHqm0XXy3DL8ZFJaajNDV2PN97cYd3WWvJwqcq8gPggrKClQF+GY4jpa7VJxOw0lbz9ptYU+2RQg7QsdUMT4zztz4peAF3y9I1IkVNjXSYbAVjiQ8bUHiMXqLQ413Yo0m3oORaehqHIVlwTJEMXfn/w7bXkgeUiT9W3oyxxH635pNbpa5/Qtzk76dl0OqlfUWgAPH9itthNs5LAFsmnL9Kr/8TeQRocxn5YxaNhXBLZoLm3V8rCDKBWDXCj7R+c166QuVSEsx8+E7w5+1lOQQGH1IV05eRxqOc7nn3eF4xBgKyJfoNgQNQ+7bzPI8aqmOkh4j2cN3ooPMaWKpCvZqg1nNNVaLygr7gUShO+eLS60WlYxYGqYygYL6ublF3Ox8PE8+A1qkqeW9BDkOnf2m/4ucNAthcDsJdrGIBT25cC4oD8BHAyctsPSvIMM/zRABNzbbMpMLU3WkTANDElHTrmW7BKW+X9ei6d6XTaRvQbdSq9UvyIds8drJmeZHa5hukjdXXCwAlSY6f/9rKzMASbpNXcvubtFwzgyYG1j5xe1KXcy3RRJgFkJL0wLhg8ooz4ue3dZpVR/LyAcMfylkFFFdqIHyVr9a4d5Bey72PWNrsTF2MoH3oOvcLqpid2wzUjlTTLisTgXddxxJ5F2+SpjhV5FQow==
res = main1()
# print(res)