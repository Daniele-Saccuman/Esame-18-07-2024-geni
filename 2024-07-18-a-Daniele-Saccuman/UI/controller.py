import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listChromo = []
        self._chromo = None
        self.min = None
        self.max = None
        self.listaBest = []
        self.listaBest2 = []

    def handle_graph(self, e):
        minimo = self._view.dd_min_ch.value
        massimo = self._view.dd_max_ch.value

        if minimo is None:
            self._view.create_alert("Minimo non inserito")
            return
        if massimo is None:
            self._view.create_alert("Massimo non inserito")
            return
        if minimo >= massimo:
            self._view.create_alert("Il minimo non può essere maggiore del massimo")
            return

        self._model.build_graph(minimo, massimo)
        self._view.txt_result1.controls.append(ft.Text(
            f"Numero di vertici: {self._model.get_num_of_nodes()} Numero di archi: {self._model.get_num_of_edges()}"))

        listaBest = self._model.archiUscentiMaggiori()
        self._view.txt_result1.controls.append(ft.Text(
            f"Archi uscenti:"))
        for vertice in listaBest:
            self._view.txt_result1.controls.append(ft.Text(f"{vertice[0]} | archi uscenti: {vertice[1]} | peso totale: {vertice[2]}"))

        listaBest2 = self._model.archiEntrantiMaggiori()
        self._view.txt_result1.controls.append(ft.Text(
            f"Archi entranti:"))
        for vertice in listaBest2:
            self._view.txt_result1.controls.append(
                ft.Text(f"{vertice[0]} | archi entranti: {vertice[1]} | peso totale: {vertice[2]}"))

        components = self._model.get_weakly_connected_components()
        num_components = len(components)
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero totale di componenti debolmente connesse: {num_components}"))

        # 2. Identificare la componente di dimensione maggiore
        largest_component = max(components, key=len)
        largest_size = len(largest_component)

        self._view.txt_result1.controls.append(
            ft.Text(f"La componente più grande contiene {largest_size} nodi."))
        self._view.txt_result1.controls.append(
            ft.Text(f"Nodi della componente più grande: {largest_component}"))

        # 3. Stampare tutte le componenti (opzionale)
        #for idx, component in enumerate(components):
            #self._view.txt_result1.controls.append(
                #ft.Text(f"Component {idx + 1}: {component}"))
        self._view.update_page()



    def handle_path(self, e):
        pass

    def fillDD(self):
        self._listChromo = self._model.getChromosome()
        for c in self._listChromo:
            self._view.dd_min_ch.options.append(ft.dropdown.Option(c))
            self._view.dd_max_ch.options.append(ft.dropdown.Option(c))
        self._view.update_page()

    def read_chromo(self, e):
        if e.control.value is None:
            self._chromo = None
        else:
            self._chromo = e.control.value

