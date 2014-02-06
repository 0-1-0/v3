from tornado import web, gen, ioloop
import docker
import json
import networkx as nx
from settings import *

class Service(object):
    def __init__(self, container_id, name, image, cmd, ports, status='RUN'):
        self.ip = HOST_IP
        self.id = container_id
        self.name = name
        self.image = image
        self.ports = ports
        self.status = status
        self.cmd = cmd
        self.name

    def __str__(self):
        return """id:{0}, desc:{1}, port(s):{2}, status:{3}
            """.format(
                self.id, 
                ':'.join([self.name, self.image, self.cmd]), 
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
        
    def services(self, callback):
        services = map(h2o, self.client.containers())
        res = {}
        for s in services:
            res[s.Names[0]] = Service(
                    s.Id, s.Names[0], s.Image, s.Command, 
                    s.Ports, s.Status.split()[0])
        return res


class NodeController(object):

    def __init__(self):
        self._locator = ServiceLocator()
        self._client = self._locator._client
        self.config = json.load(open(CONFIG_PATH))
        for service,config in self.config:
            self.config[service] = h2o(config)             

    def available_services(self):
        return self.config.keys()

    def start_service(self, service):
        cnf = self.config[service]
        cid = self._client.create_container(
            image=cnf.image, 
            ports=cnf.ports, 
            detach=True, 
            command=cnf.cmd,
            name=service)
        self.start_service(cid, cnf.port_bindings)

    def start_service(self, cid, pb=None):
        self._client.start(cid, port_bindings=pb)

    def stop_service(self, cid):
        self._client.stop(cid)

    def kill_service(self, cid):
        self._client.kill(cid)

    def launch_configured(self):
        g = nx.DiGraph()
        for service, config in self.config:
            for dependecy in config.deps:
                g.add_edge(service, dependecy)

        for service in nx.topological_sort(g):
            self.start_service(service)



class MainHandler(web.RequestHandler):
    def get(self):
        self.write("")

application = web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(HTTP_PORT)
    ioloop.IOLoop.instance().start()
