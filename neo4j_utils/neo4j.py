from py2neo import *


class Neo4j:
    def __init__(self):
        try:
            self.graph = Graph("http://localhost:7474", auth=("neo4j", "1111"))
            self.matcher = NodeMatcher(self.graph)
        except:
            print('*-- 请打开neo4j服务 --*')

    def insertNeo4j(self, doubles):
        # 保存到neo4j，参数是一个二维的列表
        try:
            covid = self.matcher.match('covid', name='COVID-19').first()
            if not covid:
                covid = Node('covid', name='COVID-19')
                self.graph.create(covid)
            for dou in doubles:
                # B结点建立
                nodeB = self.matcher.match(dou[2], name=dou[3]).first()
                if not nodeB:
                    nodeB = Node(dou[2], name=dou[3])
                # A结点建立
                if dou[0] == 'covid':
                    rel = Relationship(covid, '有关', nodeB)
                    s = covid | nodeB | rel
                    self.graph.create(s)
                else:
                    nodeA = self.matcher.match(dou[0], name=dou[1]).first()
                    if not nodeA:
                        nodeA = Node(dou[0], name=dou[1])
                    rel = Relationship(nodeA, '有关', nodeB)
                    s = nodeA | nodeB | rel
                    self.graph.create(s)
        except:
            return False
        return True


if __name__ == '__main__':
        neo = Neo4j()
        list=[
            ['covid','COVID-19','gene','ACE'],
            ['gene','ACE','phen','发热']
        ]
        neo.insertNeo4j(list)