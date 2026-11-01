import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYears(self):
        anni= self._model.getYears()
        for year in anni:
            self._view._ddYear1.options.append(ft.dropdown.Option(year))
            self._view._ddYear2.options.append(ft.dropdown.Option(year))
        self._view.update_page()
    def handleBuildGraph(self, e):
        # RECUPERO GLI ANNI SELEZIONATI
        year1 = self._view._ddYear1.value
        year2 = self._view._ddYear2.value

        # COSTRUISCO IL GRAFO
        self._model.buildGraph(year1, year2)

        # SVUOTO I RISULTATI PRECEDENTI
        self._view._txt_result.controls.clear()

        self._view._txt_result.controls.append(
            ft.Text("Grafo correttamente creato:"))
        # MOSTRO IL NUMERO DI NODI E ARCHI
        self._view._txt_result.controls.append(
            ft.Text(f"Numero nodi: {self._model.getNumNodi()}")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"Numero archi: {self._model.getNumArchi()}")
        )


        # AGGIORNO LA PAGINA
        self._view.update_page()

    def handlePrintDetails(self, e):
        # PULISCO I RISULTATI PRECEDENTI
        self._view._txtGraphDetails.controls.clear()

        # RECUPERO I NODI DELLA COMPONENTE PIU' GRANDE E I RELATIVI PESI MASSIMI
        result = self._model.getGraphDetails()

        # AGGIUNGO IL TITOLO
        self._view._txtGraphDetails.controls.append(
            ft.Text("Stampa dettagli:")
        )

        # VISUALIZZO I NODI E I RELATIVI PESI MASSIMI
        for c, pesoMax in result:
            self._view._txtGraphDetails.controls.append(
                ft.Text(f"{c.name} -- Peso massimo: {pesoMax}")
            )

        # AGGIORNO LA PAGINA
        self._view.update_page()

    def handleCercaTeamSfortunati(self, e):
        pass
