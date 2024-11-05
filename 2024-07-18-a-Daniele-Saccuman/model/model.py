import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes = []
        self._edges = []
        self.graph = nx.DiGraph()

        self._listChromo = []
        self._listConnectedGenes = []
        self._listGenes = []
        self._idMap ={}
        self.listaUscenti = []
        self.listaBest = []



    def getChromosome(self):
        self._listChromo = DAO.getAllChromosome()
        return self._listChromo

    def build_graph(self, minimo, massimo):

        self._listGenes = DAO.get_all_genes(minimo, massimo)
        self.graph.add_nodes_from(self._listGenes)
        for g in self._listGenes:
            self._idMap[(g.GeneID, g.Function)] = g

        self._listConnectedGenes = DAO.getAllConnectedGenes(minimo, massimo)
        for c in self._listConnectedGenes:
            codiceGeneFunzione1 = (c[0], c[1])
            codiceGeneFunzione2 = (c[3], c[4])
            gene1 = self._idMap[codiceGeneFunzione1]
            gene2 = self._idMap[codiceGeneFunzione2]
            if c[2] < c[5]:
                self.graph.add_edge(gene1, gene2, weight=c[6])
            elif c[2] > c[5]:
                self.graph.add_edge(gene2, gene1, weight=c[6])
            elif c[2] == c[5]:
                self.graph.add_edge(gene1, gene2, weight=c[6])
                self.graph.add_edge(gene2, gene1, weight=c[6])

        '''for c in self._listConnectedGenes:
            cr1 = c[0]
            cr2 = c[1]
            peso = c[2]
            self.graph.add_edge(cr1, cr2, weight=peso)'''

    def archiUscentiMaggiori(self):
        listaUscenti = []
        listaBest = []
        for g in self._listGenes:
            pesoComplessivo = 0
            numSuccessori = 0
            for uscente in self.graph.successors(g):
                numSuccessori += 1
                pesoComplessivo += self.graph[g][uscente]["weight"]
            listaUscenti.append((g, numSuccessori, pesoComplessivo))
        listaUscenti.sort(key=lambda x: x[1], reverse=True)
        conta = 0
        for g in range(0, len(listaUscenti)):
            if conta <= 4:
                listaBest.append(listaUscenti[g])
                conta = conta + 1
        print(len(listaBest))
        return listaBest

    def archiEntrantiMaggiori(self):
        listaEntranti = []
        listaBest = []
        for g in self._listGenes:
            pesoComplessivo = 0
            numPredecessori = 0
            for entrante in self.graph.predecessors(g):
                numPredecessori += 1
                pesoComplessivo += self.graph[entrante][g]["weight"]
            listaEntranti.append((g, numPredecessori, pesoComplessivo))
        listaEntranti.sort(key=lambda x: x[1], reverse=True)
        conta = 0
        for g in range(0, len(listaEntranti)):
            if conta <= 4:
                listaBest.append(listaEntranti[g])
                conta = conta + 1
        print(len(listaBest))
        return listaBest

    def get_weakly_connected_components(self):
        # Ottiene le componenti debolmente connesse del grafo
        components = list(nx.weakly_connected_components(self.graph))
        return components

    def get_nodes(self):
        return self.graph.nodes()

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def get_num_of_nodes(self):
        return self.graph.number_of_nodes()

    def get_num_of_edges(self):
        return self.graph.number_of_edges()