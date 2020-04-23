from app.components.clusternode import ClusterNode
nodes=[]
for i in range(200,208):
    nodes.append(ClusterNode('192.168.1.'+str(i)))

for node in nodes:
    if node.getpingresult():
        print(node.ip_address + ': Online')
    else:
        print(node.ip_address + ': Offline')