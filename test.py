# qs_json =[{'fid': 1, 'fname': 'Board Committee', 'fn': 'board', 'stat': 'True', 'company_id': '1', 'approved': 'approved', 'inchargeid': None, 'presentor': 'vikas'},
#           {'fid': 2, 'fname': 'Audit Committee', 'fn': 'audit', 'stat': 'true', 'company_id': '1', 'approved': 'approved', 'inchargeid': None, 'presentor': None},
#           {'fid': 3, 'fname': 'HR Committee', 'fn': 'hr', 'stat': 'true', 'company_id': '1', 'approved': 'approved', 'inchargeid': None, 'presentor': None}]
#
# final_presentor = [{'presenter': ['prashant', 'mayur', 'supriya', 'vikas', 'haris']}, {'presenter': ['mayur', 'supriya', 'vikas']}, {'presenter': ['mayur', 'supriya', 'vikas']}]
# a= []
#
# for ele,ele1 in zip(qs_json,final_presentor):
#
#     ele.update(ele1)
#     a.append(ele)
# print(a)

# import json
#
# # Creating a dictionary
# Dictionary = ['{"mid": "1", "title": "First Board Meeting - Draft MOM v2", "mom": "D:/project_bk_zips/emeetingadminpythonfiles_V/emeetingadminpythonfiles_V/Emeeting/EmeetingApp/static/resources/Board Committee/1/Sample_Document_20201013195329623.pdf", "version": "2", "momId": 2, "ExpiryDate": "10/13/2020 19:53:30"}', '{"mid": "2", "title": "Second Board Meeting - Draft MOM v1", "mom": "D:/project_bk_zips/emeetingadminpythonfiles_V/emeetingadminpythonfiles_V/Emeeting/EmeetingApp/static/resources/Board Committee/2/Sample_Document_20201013195444531.pdf", "version": "1", "momId": 3, "ExpiryDate": "10/13/2020 19:54:44"}']
#
#
# # Converts input dictionary into
# # string and stores it in json_string
# json_string = json.dumps(Dictionary)
# print('Equivalent json string of input dictionary:',
# 	json_string)
# print("	 ")
#
# # Checking type of object
# # returned by json.dumps
# print(type(json_string))
#
# import requests
# from requests import Session
# from signalr import Connection
#
# requests.adapters.DEFAULT_RETRIES = 5
# requests.session().keep_alive = False
#
# with Session() as session:
#
#     #create a connection
#     print("session---> ",session)
#     connection = Connection('http://localhost:5000/signalr', session)
#
#     #get chat hub
#     chat = connection.register_hub('chat')
#     print("chat--->",chat)
#
#     #start a connection
#     connection.start()
#     print("conn started")
#     #create new chat message handler
#     def print_received_message(data):
#         print('received: ', data)
#
#     #create new chat topic handler
#     def print_topic(topic, user):
#         print('topic: ', topic, user)
#
#     #create error handler
#     def print_error(error):
#         print('error: ', error)
#
#     #receive new chat messages from the hub
#     chat.client.on('newMessageReceived', print_received_message)
#
#     #change chat topic
#     chat.client.on('topicChanged', print_topic)
#
#     #process errors
#     connection.error += print_error
#
#     #start connection, optionally can be connection.start()
#     with connection:
#         print("in with conn")
#
#         #post new message
#         chat.server.invoke('send', 'Python is here')
#
#         #change chat topic
#         chat.server.invoke('setTopic', 'Welcome python!')
#
#         #invoke server method that throws error
#         chat.server.invoke('requestError')
#
#         #post another message
#         chat.server.invoke('send', 'Bye-bye!')
#
#         #wait a second before exit
#         connection.wait(1)



"""
str----> <info><id title="First Board Meeting" date="None" venue="mumbai" forum=
"Board Committee" time="00:20:20"></id><id title="Second Board Meeting" date="No
ne" venue="Mumbai" forum="Board Committee" time="00:20:20"></id><id title="3rd b
oard meeting" date="None" venue="mumbai" forum="Board Committee" time="00:20:20"
></id><id title="1st Audit Meeting" date="None" venue="Mumbai" forum="Audit Comm
ittee" time="00:20:20"></id><id title="2nd Audit Meeting" date="None" venue="Mum
bai" forum="Audit Committee" time="00:20:20"></id><id title="3rd audit meeting"
date="None" venue="mumbai" forum="Audit Committee" time="00:20:20"></id><id titl
e="Cal meet 1" date="None" venue="mumbai" forum="Audit Committee" time="00:20:20
"></id><id title="1st HR Meeting" date="None" venue="Mumbai" forum="HR Committee
" time="00:20:20"></id><id title="2nd hr meeting" date="None" venue="mumbai" for
um="HR Committee" time="00:20:20"></id></info>
encrypt output-------------> q1XBc1kpDMgwdF80wXzWUeNDJ3vSfnEjUZudti1c6R6udYFk4XN
"""


import asyncio
import websockets
connected = set()
async def server(websocket, path):
        # Register.
        connected.add(websocket)
        try:
            async for message in websocket:
                for conn in connected:
                    if conn != websocket:
                        await conn.send(f'Got a new MSG FOR YOU: {message}')
        finally:
            # Unregister.
            connected.remove(websocket)


start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



