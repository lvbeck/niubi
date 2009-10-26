import sys
import xmlrpclib
rpc_srv = xmlrpclib.ServerProxy("http://localhost:8080/xmlrpc/")
#result = rpc_srv.multiply( int(sys.argv[1]), int(sys.argv[2]))
result = rpc_srv.multiply( int(2), int(3))
#print "%d * %d = %d" % (sys.argv[1], sys.argv[2], result)
print "%d * %d = %d" % (2, 3, result)
