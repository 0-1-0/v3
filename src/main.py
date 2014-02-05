from tornado import web, gen, ioloop
from locator import ServiceLocator
import docker

class Service(object):
    def __init__(self, container_id, name, cmd, ports, status='RUN'):
        self.ip = HOST_IP
        self.id = container_id
        self.service = name
        self.ports = ports
        self.status = status
        self.cmd = cmd

    def __str__(self):
        return """id:{0}, desc:{1}, port(s):{2}, status:{3}
            """.format(
                self.id, 
                self.service_name + self.cmd, 
                self.ports, 
                self.status)
    def __repr__(self):
        return self.__str__()


def h2o(x):
    if isinstance(x, dict):
        return type('jo', (), {k: h2o(v) for k, v in x.iteritems()})
    else:
        return x


class ServiceLocator(object):

    def __init__(self):
        self.client = docker.Client(
            base_url=DOCKER_SOCK,
            version=DOCKER_V, 
            timeout=TIMEOUT)
        
    @gen.engine
    def services(self, callback):
        services = map(h2o, self.client.containers())
        callback([
            Service(x.Id, x.Image, X.Command, x.Ports, x.Status.split()[0]) \
            for x in services
        ])


class NodeController(object):

    def __init__(self):
        self._locator = ServiceLocator()
        self._client = self._locator._client

    #TODO: implement matching, based on config file
    def get_launch_command(self, service_name):
        pass 

    @gen.engine
    def services(self, callback):
        services = yield gen.Task(str(self._locator.services))
        callback(services)

    def start_service(self, service_name):
        self._client.create_container(
            name, command=self.get_launch_command(service_name))

    def start_service(self, id):
        pass

    def stop_service(self, id):
        self._client.start(id)

    def kill_service(self, id):
        self._client.kill(id)




class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(HTTP_PORT)
    ioloop.IOLoop.instance().start()
