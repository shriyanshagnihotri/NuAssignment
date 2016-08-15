import socket
import threading
import SocketServer
from src.view.movieView import movieView
import udpConversation_pb2 as udpCon

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        def bail(a):
            return "Nothing", "Nothing" 
        a = movieView()
        req = udpCon.Request()
        req.ParseFromString(data)
        functions = {'add': a.perform_add_pro, 'update': a.perform_update_pro,
                     'find_by_genre': a.perform_find_genre, 'find_by_director':
                      a.perform_find_director, 
                     'find_by_actor': a.perform_find_actor, 'delete':
                      a.perform_delete, 
                     'list_movies': a.perform_list, 'bail': bail, 
                     'get_movie': a.perform_get_movie}
        op, action = functions.get(req.cmd, bail)(req.data)
        res = udpCon.Response()
        res.id = req.id + "-response"
        res.data = op
        res.result = action
        senddata = res.SerializeToString()
        socket.sendto(senddata, self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 60000

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

    k = raw_input("Press any key and return to exit")

#    client(ip, port, "Hello World 1")
#    client(ip, port, "Hello World 2")
#    client(ip, port, "Hello World 3")
    print "die"
    server.shutdown()
    server.server_close()
