class Node: 
    __nodeList = []
    __nodeCnt = 0
    
    @staticmethod
    def retrieveNodeFromId(id):
        if id >= Node.__nodeCnt:
            return None
        return Node.__nodeList[id]
    
    def __init__(self):
        self.__id = Node.__nodeCnt
        self.__nodeList.append(self)
        Node.__nodeCnt+=1
        
    def __str__(self):
        return f"[{self.__id}]"
        
    def getId(self):
        return self.__id