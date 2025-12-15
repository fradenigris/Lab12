import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        """Callback per il pulsante 'Crea Grafo'."""
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_archi(self, e):
        """Callback per il pulsante 'Conta Archi'."""
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {soglia}: {minori}, Archi > {soglia}: {maggiori}"))
        self._view.page.update()

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def handle_cammino_minimo(self, e):
        self._view.lista_visualizzazione_3.controls.clear()

        grafo = self._model.G

        if grafo.number_of_edges() == 0 and grafo.number_of_nodes() == 0:
            self._view.show_alert("Creare prima il grafo.")
            return

        if len(self._view.txt_soglia.value) == 0:
            self._view.show_alert("Inserire un valore per la soglia prima di calcolare il cammino minimo.")
            return

        soglia = float(self._view.txt_soglia.value)
        result = self._model.cammino_minimo(soglia)

        self._view.lista_visualizzazione_3.controls.append(ft.Text("Cammino minimo:"))
        for i in range(len(result)-1):
            if result[i] != result[-1]:
                self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{result[i]} --> {result[i+1]} [peso: {grafo[result[i]][result[i+1]]['weight']}]"))

        self._view.page.update()
