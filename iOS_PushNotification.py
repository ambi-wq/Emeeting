import ssl
import json
import socket
import struct
import binascii
import codecs

basepath = "D:/Workspace/Python Workspace/emeetingadminpythonfiles_V/Emeeting/EmeetingApp/"
#token_hex = 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87'
#deviceToken = '9cdcb815 d93e11ce 52baaf6c 14e27cc8 31d5ce62 2e51ce6d f75692c2 3617cadb'


class IOSPNotificationSender(object):

    def __init__(self, host, port, certificate_path):
        self.host = host
        self.port = port
        self.certificate = certificate_path

    def send_push_notification(self, token, payload):

        #the certificate file generated from Provisioning Portal
        #certfile = '../certificate/sample.pem'
        certfile = self.certificate

        # APNS server address (use 'gateway.push.apple.com' for production server)
        #apns_address = ('gateway.sandbox.push.apple.com', 2195)
        apns_address = (self.host, self.port)

        data = json.dumps(payload)

        # Clear out spaces in the device token and convert to hex
        deviceToken = token.replace(' ', '')

        byteToken = bytes.fromhex(deviceToken) # Python 3
        # byteToken = deviceToken.decode('hex') # Python 2
        print("bytetoken-------->",byteToken,type(byteToken))

        theFormat = '!BH32sH%ds' % len(data)
        theNotification = struct.pack(theFormat, 0, 32, byteToken, len(data), bytes(data,'utf-8'))

        # Create our connection using the certfile saved locally
        ssl_sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), certfile=certfile)
        ssl_sock.connect(apns_address)

        # Write out our data
        ssl_sock.write(theNotification)

        # Close the connection -- apple would prefer that we keep
        # a connection open and push data as needed.
        ssl_sock.close()

if __name__ == '__main__':

    token = '740f4707 bebcf74f 9b7c25d4 8e335894 5f6aa01d a5ddb387 462c7eaf 61bb78ad'
    payload = {
       'aps': {
            'alert':'Bitcoin price going down as -2.03%',
            'sound':'default_received.caf',
            'badge':1,
            },
            'Latest_news': { 'Bitcoin': ' The bit coin as of now down -2.03%' },
       }
    #ios_notifier = IOSPNotificationSender('gateway.sandbox.push.apple.com', 2195, basepath+'certificate/eMeetingPushCertificates.p12')
    #ios_notifier.send_push_notification(token, payload)

# -------------------------------------------------------------------------------------------------------------------------------------

from pushjack import APNSClient

client = APNSClient(certificate=basepath+'certificate/eMeetingPushCertificates.p12',
                    default_error_timeout=10,
                    default_expiration_offset=2592000,
                    default_batch_size=100,
                    default_retries=5)

def sendiOSNotification(token,alert,title,badge):
    res = client.send(token,
                      alert,
                      badge=badge,
                      sound="noti.aiff",
                      content_available=True,
                      title=title,
                     )
    # List of all tokens sent.
    print(res.tokens)

    # List of errors as APNSServerError objects
    print(res.errors)

    # Dict mapping errors as token => APNSServerError object.
    print(res.token_errors)
    expired_tokens = client.get_expired_tokens()
    client.close()


#sendiOSNotification("b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87","test","test",1)

#---------------------------------------------------------------------------------------------------------------------------------------------------

import ssl
import json
import socket
import struct
import binascii


def send_push_message(token, payload):
    # the certificate file generated from Provisioning Portal
    #certfile = 'my_app_apns_certificate.pem'
    certfile = basepath+'certificate/eMeetingPushCertificates.p12'
    # APNS server address (use 'gateway.push.apple.com' for production server)
    apns_address = ('gateway.sandbox.push.apple.com', 2195)

    # create socket and connect to APNS server using SSL
    s = socket.socket()
    #sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=certfile)
    sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), certfile=certfile)
    sock.connect(apns_address)

    # generate APNS notification packet
    token = binascii.unhexlify(token)
    fmt = "!cH32sH{0:d}s".format(len(payload))
    cmd = '\x00'
    msg = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
    sock.write(msg)
    sock.close()


if __name__ == '__main__':
    payload = {"aps": {"alert": "You got your emails.", "badge": 9, "sound": "bingbong.aiff"}}
    #send_push_message("REGISTERED_DEVICE_PUSH_TOKEN_IN_HEX", json.dumps(payload))
    deviceToken = '9cdcb815 d93e11ce 52baaf6c 14e27cc8 31d5ce62 2e51ce6d f75692c2 3617cadb'
    print("str to hex------->", deviceToken.encode().hex())
    send_push_message(deviceToken.encode().hex(), json.dumps(payload))