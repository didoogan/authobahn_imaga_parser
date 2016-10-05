
import redis
import json

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        super(MyServerProtocol, self).__init__()
        self.r = redis.StrictRedis()
        self.p = self.r.pubsub()

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        # else:
        #     print("Text message received: {0}".format(payload.decode('utf8')))

        # user_request = json.loads(payload.decode('utf8'))
        user_request = json.loads(payload)

        def handler(message):
            # items = json.dumps(message['data'])
            result = {'google': [], 'yandex': [], 'instagram': [], }
            socket_engines = json.loads(user_request['engines'])
            for engine in socket_engines:
                result[engine] = self.r.hget(user_request['query'], engine)
            self.sendMessage(json.dumps(result))
            self.onClose()

        # self.p.subscribe(flag=handler)
        flag = user_request['query']
        self.p.subscribe(**{flag: handler})
        thread = self.p.run_in_thread(sleep_time=0.01)

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
