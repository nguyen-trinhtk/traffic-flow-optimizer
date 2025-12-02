class Path:
    __pathId = 0
    __pathList = []
    
    @staticmethod
    def retrievePathFromId(id):
        if id >= Path.__PathCnt:
            return None
        return Path.__PathList[id]
    
    def __init__(self, edges):
        self.__id = Path.__pathId
        self.__pathList.append(self)
        Path.__pathId += 1
        self.__edges = edges
        
    def __str__(self):
        return " ---> ".join(f"({str(l)})" for l in self.__edges)
    
    def getId(self):
        return self.__id
    
    def getEdges(self):
        return self.__edges