from tornado import web, gen, ioloop
import docker
import json
import networkx as nx
from settings import *

class Service(object):
    def __init__(self, container_id, name, image, cmd, ports, status='UP'):
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
        self._client = docker.Client(
            base_url=DOCKER_SOCK,
            version=DOCKER_V, 
            timeout=TIMEOUT)
        
    def services(self):
        services = map(h2o, self._client.containers())
        return [Service(
                    s.Id, s.Names[0], s.Image, s.Command, 
                    s.Ports, s.Status.split()[0]) \
                for s in services]


class NodeController(object):

    def __init__(self):
        self._locator = ServiceLocator()
        self._client = self._locator._client
        self.config = json.load(open(CONFIG_PATH))
        for service,config in self.config.items():
            self.config[service] = h2o(config)

    @property
    def services(self):
        return self._locator.services()             

    @property
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

class BaseHandler(web.RequestHandler):
    _nc = NodeController()

class MainHandler(BaseHandler):

    @web.asynchronous
    @gen.engine
    def get(self):
        self.render(
            'index.html', 
            services=self._nc.services, 
            available_services=self._nc.available_services, 
            ip=HOST_IP)

class ServiceHandler(BaseHandler):

    @web.asynchronous
    @gen.engine
    def post(self):
        cid = self.get_argument('id')
        if cid:
            method_name = self.request.uri.split('/')[2] + '_service'
            getattr(self._nc, method_name).__call__(cid)

        self.redirect('/')


application = web.Application(
    handlers=[
        (r"/", MainHandler),
        (r"/service/.*", ServiceHandler),
    ],
    template_path=os.path.join(APP_ROOT, 'views')
)

if __name__ == "__main__":
    application.listen(HTTP_PORT)
    ioloop.IOLoop.instance().start()
