import networkx as nx
from database.DAO import DAO


class Model:

    def __init__(self):
        # CREO UN GRAFO SEMPLICE E NON ORIENTATO
        self._graph = nx.Graph()
    def getYears(self):
        return DAO.getAllYears()

    def buildGraph(self, year1, year2):
        # SVUOTO IL GRAFO PRIMA DI RICOSTRUIRLO
        self._graph.clear()
        # RECUPERO TUTTI I COSTRUTTORI CHE HANNO PARTECIPATO
        costruttori = DAO.getAllConstructors()

        # AGGIUNGO TUTTI I COSTRUTTORI COME NODI
        self._graph.add_nodes_from(costruttori)

        # CREO UNA MAPPA PER RISALIRE DALL'ID ALL'OGGETTO COSTRUTTORE
        cMap = {}
        for c in costruttori:
            cMap[c.constructorId] = c

        # RECUPERO LE COPPIE DI COSTRUTTORI E I RELATIVI PESI
        archi = DAO.getEdges(year1, year2)

        # AGGIUNGO GLI ARCHI AL GRAFO
        for c1, c2, peso in archi:

            # RECUPERO GLI OGGETTI COSTRUTTORE CORRISPONDENTI AGLI ID
            costruttore1 = cMap[c1]
            costruttore2 = cMap[c2]

            # AGGIUNGO L'ARCO CON IL RELATIVO PESO
            self._graph.add_edge(costruttore1, costruttore2, weight=peso)

    def getNumNodi(self):
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        return self._graph.number_of_edges()

    def getPesoMax(self, nodo):
        # RECUPERO IL PESO MAX TRA TUTTI GLI ARCHI INCIDENTI AL NODO
        pesoMax= max(
                 self._graph.get_edge_data(nodo, i)['weight']
                 for i in self._graph.neighbors(nodo)
                  )
        print(pesoMax)
        return pesoMax

    def getGraphDetails(self):
        # RECUPERO TUTTE LE COMPONENTI CONNESSE DEL GRAFO
        connComps = list(nx.connected_components(self._graph))

        # SCELGO LA COMPONENTE CON IL MAGGIOR NUMERO DI NODI
        MaxConnessa = max(connComps, key=len)

        # ASSOCIO A OGNI NODO IL SUO PESO MASSIMO
        res = []
        for c in MaxConnessa:
            res.append((c, self.getPesoMax(c)))

        # ORDINO I NODI IN BASE AL PESO MASSIMO DECRESCENTE
        res.sort(key=lambda x: x[1], reverse=True)

        # RESTITUISCO LA LISTA DEI NODI CON I RELATIVI PESI MASSIMI
        print(res)
        return res
