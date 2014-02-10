from tornado import web, gen, ioloop
import docker
import json
import networkx as nx
import random
from settings import *

import sys
sys.path.append(THRIFT_PATH)

from service_locator import *
from service_locator.ttypes import *

from thrift import TTornado
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

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


class NodeController(object):

    def __init__(self):
        self._client = docker.Client(
            base_url=DOCKER_SOCK,
            version=DOCKER_V,
            timeout=TIMEOUT)
        self.config_plain = open(CONFIG_PATH).read()
        self.config = json.loads(self.config_plain)

    def image_name_for(self, service_name):
        if service_name in self.config:
            return self.config[service_name]['image']
        else:
            return None

    @property
    def services(self):
        services = map(h2o, self._client.containers())
        return [Service(s.Id, s.Image, s.Command, s.Ports) for s in services]

    @property
    def available_services(self):
        return self.config.keys()

    def start_service(self, service_name, callback):
        cnf = self.config[service_name]
        cid = self._client.create_container(
            image=cnf['image'],
            ports=cnf['ports'],
            detach=True,
            command=cnf['cmd'])
        self._client.start(cid, publish_all_ports=True)
        callback()

    def stop_service(self, cid, callback):
        self._client.kill(cid)
        callback()


NController = NodeController()


class ServiceLocator(object):

    def __init__(self):
        self._nc = NController

    @gen.engine
    def get_running_instances(self, service_name, callback, attempts=0):
        img = self._nc.image_name_for(service_name)
        if img == None:
            callback([])
        services = filter(lambda s: img in s.image, self._nc.services)
        running_instances = []
        for service in services:
            instance = ServiceInstance(ports={})
            for port in service.ports:
                private_port = port['PrivatePort']
                info = self._nc._client.port(service.id, private_port)[0]
                instance.ip = info['HostIp']
                instance.ports[int(private_port)] = int(info['HostPort'])
            running_instances.append(instance)

        if running_instances == [] and attempts < MAX_ATTEMPTS:
            yield gen.Task(self._nc.start_service, service_name)
            running_instances = yield gen.Task(
                self.get_running_instances,
                service_name, attempts=attempts+1)

        callback(running_instances)

    @gen.engine
    def get_running_instance(self, service_name, calback):
        instances = yield gen.Task(self.get_running_instances, service_name)
        callback(random.choice(instances))


class BaseHandler(web.RequestHandler):
    _nc = NController

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
            method = getattr(self._nc, method_name)
            yield gen.Task(method, cid)

        self.redirect('/')

class TLocatorServer(TTornado.TTornadoServer):

    def __init__(self):
        handler = ServiceLocator()
        processor = TServiceLocator.Processor(handler)
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        super(TLocatorServer, self).__init__(processor, pfactory)


application = web.Application(
    handlers=[
        (r"/", MainHandler),
        (r"/service/.*", ServiceHandler),
    ],
    template_path=os.path.join(APP_ROOT, 'views')
)

if __name__ == "__main__":
    application.listen(HTTP_PORT)
    tserver = TLocatorServer()
    tserver.bind(THRIFT_PORT)
    tserver.start(1)

    ioloop.IOLoop.instance().start()
