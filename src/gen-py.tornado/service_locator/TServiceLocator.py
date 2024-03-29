#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:tornado
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None

from tornado import gen
from tornado import stack_context

class Iface(object):
  def get_runing_instances(self, service_name, callback):
    """
    Parameters:
     - service_name
    """
    pass

  def get_running_instance(self, service_name, callback):
    """
    Parameters:
     - service_name
    """
    pass


class Client(Iface):
  def __init__(self, transport, iprot_factory, oprot_factory=None):
    self._transport = transport
    self._iprot_factory = iprot_factory
    self._oprot_factory = (oprot_factory if oprot_factory is not None
                           else iprot_factory)
    self._seqid = 0
    self._reqs = {}

  @gen.engine
  def recv_dispatch(self):
    """read a response from the wire. schedule exactly one per send that
    expects a response, but it doesn't matter which callee gets which
    response; they're dispatched here properly"""

    # wait for a frame header
    frame = yield gen.Task(self._transport.readFrame)
    tr = TTransport.TMemoryBuffer(frame)
    iprot = self._iprot_factory.getProtocol(tr)
    (fname, mtype, rseqid) = iprot.readMessageBegin()
    method = getattr(self, 'recv_' + fname)
    method(iprot, mtype, rseqid)

  def get_runing_instances(self, service_name, callback):
    """
    Parameters:
     - service_name
    """
    self._seqid += 1
    self._reqs[self._seqid] = callback
    self.send_get_runing_instances(service_name)
    self.recv_dispatch()

  def send_get_runing_instances(self, service_name):
    oprot = self._oprot_factory.getProtocol(self._transport)
    oprot.writeMessageBegin('get_runing_instances', TMessageType.CALL, self._seqid)
    args = get_runing_instances_args()
    args.service_name = service_name
    args.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def recv_get_runing_instances(self, iprot, mtype, rseqid):
    callback = self._reqs.pop(rseqid)
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      callback(x)
      return
    result = get_runing_instances_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.success is not None:
      callback(result.success)
      return
    callback(TApplicationException(TApplicationException.MISSING_RESULT, "get_runing_instances failed: unknown result"))
    return

  def get_running_instance(self, service_name, callback):
    """
    Parameters:
     - service_name
    """
    self._seqid += 1
    self._reqs[self._seqid] = callback
    self.send_get_running_instance(service_name)
    self.recv_dispatch()

  def send_get_running_instance(self, service_name):
    oprot = self._oprot_factory.getProtocol(self._transport)
    oprot.writeMessageBegin('get_running_instance', TMessageType.CALL, self._seqid)
    args = get_running_instance_args()
    args.service_name = service_name
    args.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def recv_get_running_instance(self, iprot, mtype, rseqid):
    callback = self._reqs.pop(rseqid)
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(iprot)
      iprot.readMessageEnd()
      callback(x)
      return
    result = get_running_instance_result()
    result.read(iprot)
    iprot.readMessageEnd()
    if result.success is not None:
      callback(result.success)
      return
    callback(TApplicationException(TApplicationException.MISSING_RESULT, "get_running_instance failed: unknown result"))
    return


class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["get_runing_instances"] = Processor.process_get_runing_instances
    self._processMap["get_running_instance"] = Processor.process_get_running_instance

  @gen.engine
  def process(self, transport, iprot_factory, oprot, callback):
    # wait for a frame header
    frame = yield gen.Task(transport.readFrame)
    tr = TTransport.TMemoryBuffer(frame)
    iprot = iprot_factory.getProtocol(tr)

    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
    else:
      yield gen.Task(self._processMap[name], self, seqid, iprot, oprot)
    callback()

  @gen.engine
  def process_get_runing_instances(self, seqid, iprot, oprot, callback):
    args = get_runing_instances_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = get_runing_instances_result()
    result.success = yield gen.Task(self._handler.get_runing_instances, args.service_name)
    oprot.writeMessageBegin("get_runing_instances", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()
    callback()

  @gen.engine
  def process_get_running_instance(self, seqid, iprot, oprot, callback):
    args = get_running_instance_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = get_running_instance_result()
    result.success = yield gen.Task(self._handler.get_running_instance, args.service_name)
    oprot.writeMessageBegin("get_running_instance", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()
    callback()


# HELPER FUNCTIONS AND STRUCTURES

class get_runing_instances_args:
  """
  Attributes:
   - service_name
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'service_name', None, None, ), # 1
  )

  def __init__(self, service_name=None,):
    self.service_name = service_name

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.service_name = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('get_runing_instances_args')
    if self.service_name is not None:
      oprot.writeFieldBegin('service_name', TType.STRING, 1)
      oprot.writeString(self.service_name)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class get_runing_instances_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.LIST, 'success', (TType.STRUCT,(ServiceInstance, ServiceInstance.thrift_spec)), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.LIST:
          self.success = []
          (_etype12, _size9) = iprot.readListBegin()
          for _i13 in xrange(_size9):
            _elem14 = ServiceInstance()
            _elem14.read(iprot)
            self.success.append(_elem14)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('get_runing_instances_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.LIST, 0)
      oprot.writeListBegin(TType.STRUCT, len(self.success))
      for iter15 in self.success:
        iter15.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class get_running_instance_args:
  """
  Attributes:
   - service_name
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'service_name', None, None, ), # 1
  )

  def __init__(self, service_name=None,):
    self.service_name = service_name

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.service_name = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('get_running_instance_args')
    if self.service_name is not None:
      oprot.writeFieldBegin('service_name', TType.STRING, 1)
      oprot.writeString(self.service_name)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class get_running_instance_result:
  """
  Attributes:
   - success
  """

  thrift_spec = (
    (0, TType.STRUCT, 'success', (ServiceInstance, ServiceInstance.thrift_spec), None, ), # 0
  )

  def __init__(self, success=None,):
    self.success = success

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRUCT:
          self.success = ServiceInstance()
          self.success.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('get_running_instance_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRUCT, 0)
      self.success.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
