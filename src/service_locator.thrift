struct ServiceInstance {
    1:string ip;
    2:map<i32,i32> ports;
}

service TServiceLocator {
    list<ServiceInstance> get_runing_instances(1:string service_name),
    ServiceInstance get_running_instance(1:string service_name)
}