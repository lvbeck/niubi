from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

class PlogXMLRPCDispatcher(SimpleXMLRPCDispatcher):
	def __init__(self, funcs):
		SimpleXMLRPCDispatcher.__init__(self, True, 'utf-8')
		self.funcs = funcs  