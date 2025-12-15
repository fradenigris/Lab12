import networkx as nx
from numpy.ma.core import innerproduct

from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO

        self.G = nx.Graph()
        self._nodes = None
        self._edges = None

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO

        self.G.clear()

        self._edges = DAO.get_connessioni_filtrate(year)
        self._nodes = set()
        rifugi = DAO.get_all_rifugi()

        for rif in rifugi:
            for conn in self._edges:
                if rif.id == conn.id_rifugio1 or rif.id == conn.id_rifugio2:
                    self._nodes.add(rif)

        self.G.add_nodes_from(self._nodes)

        for rif1 in self._nodes:
            for rif2 in self._nodes:
                if rif1.id != rif2.id:
                    for conn in self._edges:
                        if ((rif1.id == conn.id_rifugio1 and rif2.id == conn.id_rifugio2) or
                                (rif1.id == conn.id_rifugio2 and rif2.id == conn.id_rifugio1)):
                            peso = conn.distanza * conn.fattore_difficolta
                            self.G.add_edge(rif1, rif2, weight = peso)
                            conn.id_rifugi.add(rif1)
                            conn.id_rifugi.add(rif2)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO

        # Restituisce una tupla (min, max)

        diz = nx.get_edge_attributes(self.G, 'weight')

        return min(diz.values()), max(diz.values())

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO

        diz = nx.get_edge_attributes(self.G, 'weight')

        count_min = 0
        count_max = 0
        for peso in diz.values():
            if peso < soglia:
                count_min += 1
            if peso > soglia:
                count_max += 1

        return count_min, count_max

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def cammino_minimo(self, soglia):

        a = self.cm_nx(soglia)
        b = self.cm_recursive(soglia)

        return a

    def cm_nx(self, soglia : float):

        newG = self.G.copy()
        for u, v, dati in list(newG.edges(data=True)):
            if dati['weight'] <= soglia:
                newG.remove_edge(u, v)

        if newG.number_of_edges() < 2:
            return []

        min_peso_totale = None
        miglior_percorso = []

        for nodo in newG.nodes():
            vicini = newG.neighbors(nodo)

            for vic in vicini:
                peso1 = newG[nodo][vic]['weight']
                vicini_di_vicini = newG.neighbors(vic)

                for vic_di_vic in vicini_di_vicini:
                    if vic_di_vic == nodo:
                        continue

                    peso2 = newG[vic][vic_di_vic]['weight']

                    peso_tot = peso1 + peso2

                    if min_peso_totale is None or peso_tot < min_peso_totale:
                        min_peso_totale = peso_tot

                        miglior_percorso = [nodo, vic, vic_di_vic]

        return miglior_percorso

    def cm_recursive(self, soglia):
        pass
