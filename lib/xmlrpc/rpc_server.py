import SimpleXMLRPCServer

class MyObject:
    def sayHello(self):
        return "hello xmlprc"

obj = MyObject()
#server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8088))
server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8080))
server.register_instance(obj)

print "Listening on port 8080"
server.serve_forever()