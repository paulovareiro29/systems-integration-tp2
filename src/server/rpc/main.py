import signal
import sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.queries import fetchAirbnbs, fetchAreas, fetchTypes, countAirbnbs, fetchByArea, fetchByType, fetchByPriceHigherThen, fetchByPriceLowerThen

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...
            print("exiting, gracefully")
            sys.exit(0)

        # signals
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # register both functions
        server.register_function(fetchAirbnbs)
        server.register_function(fetchAreas)
        server.register_function(fetchTypes)
        server.register_function(countAirbnbs)
        server.register_function(fetchByArea)
        server.register_function(fetchByType)
        server.register_function(fetchByPriceLowerThen)
        server.register_function(fetchByPriceHigherThen)

        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
