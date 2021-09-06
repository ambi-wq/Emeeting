from pyfcm import FCMNotification


apikey = 'AAAAbo5HtU0:APA91bFBxPMjJrBWYG5RDxSFmPwArPOmpLN5aCY66pFGTanuvacSWL_pIdvwYIBNopy6XmfuGxX9vATH6ZMtz15U3uyf0yofM0Krx6O-jmVDHnUyqCsou-CDJW9j1AGm4JCiFo6wOj8J'
deviceToken = ['dvSUHxkaTpWbL7hwHFvEfO:APA91bEaGfnvFG7JbjRlgssJWvpiiPl4231U0OroLOoHsMbiWvcxrQeEby_5U2v7Sr45CG1N1e6_koXXSXn9quGliNovw3SZqZUaIDEj3vb9r7MQcPBPrdFDjdUThAT5wG5Sj78TydWA']



push_service = FCMNotification(api_key=apikey)

# Send to single device.
def singleNotification(token,title,body):
    registration_id = token
    message_title = title
    message_body = body
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    print ("response from fcm--------------->",result)
    return result

# Send to multiple devices by passing a list of ids.
def multipleNotification(token,title,body):
    #registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
    registration_ids = token
    message_title = title
    message_body = body
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

    print("response from fcm------->",result)
    return result



multipleNotification(deviceToken,'emeet','test body')