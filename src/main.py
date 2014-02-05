from tornado import web, gen, ioloop

class Service(object):
    def __init__(self, container_id, name, port, status='RUN'):
        self.id = container_id
        self.service_name = name
        self.port = port
        self.status = status

    def __str__(self):
        return """id:{0}, name:{1}, port(s):{2}, status:{3}
            """.format(self.id, self.service_name, self.status)
    def __repr__(self):
        return self.__str__()

class NodeController(object):
    def __init__(self):
        self._services = []

    def services(self):
        return str(self._services)

    def start_service(self, name):
        pass

    def start_service(self, id):
        pass

    def stop_service(self, id):
        pass

    def kill_service(self, id):
        pass




class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8891)
    tornado.ioloop.IOLoop.instance().start()