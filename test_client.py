import socket, ssl, json, struct

# Initially pulled from Stack Overflow, modified for version 2 of APNS

deviceToken = 'aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa' 

data = json.dumps({
     'aps': {
          'alert':'Alert body',
          'sound':'alarm.caf',
          'badge':3,
          },
     'test_data': { 'foo': 'bar' },
     })

byteToken = bytes.fromhex(deviceToken.replace(' ',''))

notification_id = b'asdf'

frame_length = len(byteToken) + 3 + len(data) + 3 + len(notification_id) + 3

fmt = '!BLBH%dsBH%dsBH4s' % (len(byteToken), len(data))
theNotification = struct.pack(fmt, 2, frame_length,
                              1, len(byteToken), byteToken,
                              2, len(data), bytes(data, "ascii"),
                              3, len(notification_id), notification_id)

# Create our connection using the certfile saved locally
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8889))

# Write out our data
sock.send(theNotification)

# Close the connection -- apple would prefer that we keep
# a connection open and push data as needed.
sock.close()
