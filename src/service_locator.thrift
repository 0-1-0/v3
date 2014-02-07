service TServiceLocator {
    list<string> get_runing_instances(1:string service_name),
}