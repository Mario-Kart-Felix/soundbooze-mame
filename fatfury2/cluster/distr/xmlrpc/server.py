from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/FF2',)

server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler)
server.register_introspection_functions()

server.register_function(pow)

# checkPKL()
# queueCluster()
# queueReduce()
# switchMeth()

def adder_function(x,y):
    return x + y

server.register_function(adder_function, 'add')

class MyFuncs:
    def div(self, x, y):
        return x // y

server.register_instance(MyFuncs())

server.serve_forever()
