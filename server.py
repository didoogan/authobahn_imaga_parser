
import redis
import json

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        self.r = redis.StrictRedis()
        self.p = self.r.pubsub()

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        # def handler(message):
        #     # items = json.dumps(message['data'])
        #     # self.sendMessage(items)
        #     # self.sendMessage(message['data'])
        #     print 'FUCK'
        #
        # def handler_chanel(message):
        #     print 'from handler_chanel ', message
        #     # items = json.dumps(message['data'])
        #     # self.sendMessage(items)
        #     self.sendMessage(message['data'])
        # self.p.subscribe(**{'flag': handler, 'chanel': handler_chanel})
        # thread = self.p.run_in_thread(sleep_time=0.01)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        user_request = payload.decode('utf8')

        def handler(message):
            # items = json.dumps(message['data'])

            self.sendMessage(self.r.hgetall(user_request))
            # print 'FUCK', message['data']
            # pass

        def handler_chanel(message):
            print 'from handler_chanel ', message
            # items = json.dumps(message['data'])
            # self.sendMessage(items)
            # self.sendMessage(message['data'])
            # print 'FUCK!!!!'
            pass
        self.p.subscribe(**{'flag': handler, user_request: handler_chanel})
        thread = self.p.run_in_thread(sleep_time=0.01)

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    # note to self: if using putChild, the child must be bytes...

    reactor.listenTCP(9000, factory)
    reactor.run()
