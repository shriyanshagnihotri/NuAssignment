import socket
import sys
import udpConversation_pb2 as udpCon
import uuid
import src.protobuf_json as pj

def cmd_format():
	print "cmd format is:\npython NuIMDB <add/update/find_by{genre, directors, actors}/list/delete data_in_json"

if len(sys.argv) != 3:
	print "Invalid command"
	cmd_format()
	sys.exit(-1)

req = udpCon.Request()
req.id = str(uuid.uuid4())
req.cmd = sys.argv[1]
req.data = sys.argv[2]
HOST, PORT = "localhost", 60000

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
data = req.SerializeToString()
print "Sent:     {}".format(pj.pb2json(req))
sock.sendto(data, (HOST, PORT))
received = sock.recv(16384)
res = udpCon.Response()
res.ParseFromString(received)

sock.close()

print "Received: {}".format(pj.pb2json(res))
