from .node import Node

class Edge: 
    __edgeList = []
    __edgeCnt = 0
    
    @staticmethod
    def retrieveEdgeFromId(id):
        if id >= Edge.__edgeCnt:
            return None
        return Edge.__edgeList[id]
    
    def __init__(self, src: Node, sink: Node, capacity=1):
        self.__id = Edge.__edgeCnt
        self.__src = src
        self.__sink = sink
        self.__capacity = capacity
        Edge.__edgeList.append(self)
        Edge.__edgeCnt += 1  
              
    def __str__(self):
        return f"{str(self.__src)}->{str(self.__sink)}"
    
    def getId(self):
        return self.__id
    
    def getSrcNode(self):
        return self.__src
    
    def getSinkNode(self):
        return self.__sink
    
    def getSrcId(self):
        return self.__src.getId()
    
    def getSinkId(self):
        return self.__sink.getId()
    
    def getCapacity(self):
        return self.__capacity
        