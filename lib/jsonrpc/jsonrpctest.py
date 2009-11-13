#! /usr/bin/env python
"""
cgi test script for SimpleJSONRPCServer
"""

from SimpleJSONRPCServer import CGIJSONRPCRequestHandler

class MyFuncs:
    def div(self, x, y) : return div(x,y)
    def subtract(self, x, y) : return x - y

handler = CGIJSONRPCRequestHandler()
handler.register_function(pow)
handler.register_function(lambda x,y: x+y, 'add')
handler.register_introspection_functions()
handler.register_instance(MyFuncs())
handler.handle_request()

