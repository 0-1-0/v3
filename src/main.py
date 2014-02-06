from tornado import web, gen, ioloop
import docker
import json
import networkx as nx
from settings import *

class Service(object):
    def __init__(self, container_id, image, cmd, ports):
        self.id = container_id
        self.image = image
        self.ports = ports
        self.cmd = cmd

    def __str__(self):
        return """\n id:{0}\n desc:{1}\n port(s):{2}
            """.format(
                self.id,
                self.image + '.' + self.cmd,
                '; '.join(
                        map(
                            lambda x: '->'.join(
                                map(
                                    str, [x['PublicPort'], x['PrivatePort']]
                                    )
                                ), 
                            filter(
                                lambda x: x['PrivatePort'] != 0, self.ports)
                        )
                    )
                )

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
        return [Service(s.Id, s.Image, s.Command, s.Ports) for s in services]


class NodeController(object):

    def __init__(self):
        self._locator = ServiceLocator()
        self._client = self._locator._client
        self.config_plain = open(CONFIG_PATH).read()
        self.config = json.loads(self.config_plain)

    @property
    def services(self):
        return self._locator.services()

    @property
    def available_services(self):
        return self.config.keys()

    def start_service(self, service_name):
        cnf = self.config[service_name]
        cid = self._client.create_container(
            image=cnf['image'],
            ports=cnf['ports'],
            detach=True,
            command=cnf['cmd'])
        self._client.start(cid, port_bindings=cnf['port_bindings'])

    def stop_service(self, cid):
        self._client.kill(cid)

    def restart_service(self, cid):
        self._client.restart(cid)

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
            node_config=self._nc.config_plain,
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
