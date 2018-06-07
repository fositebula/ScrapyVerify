import SimpleXMLRPCServer
from getVerifyListDaemon import scrapyVerify
#
# class MyObject:
#     def ScrapyVerify(self):
#         return scrapyVerify()

# obj = MyObject()
server = SimpleXMLRPCServer.SimpleXMLRPCServer(("10.0.70.104", 8088))
# server.register_instance(obj)
server.register_function(scrapyVerify)
print "Listening on port 8088"
server.serve_forever()