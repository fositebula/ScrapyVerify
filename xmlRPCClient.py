import xmlrpclib


server = xmlrpclib.ServerProxy("http://10.0.70.104:8088")

words = server.scrapyVerify()

print words