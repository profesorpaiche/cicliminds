import os
import json

from ipywidgets import Label, VBox, HBox, Button, Select

import cdsapi
import tarfile

# from cicliminds.widgets.common import ObserverWidget

class DownloadWidget:
    FILTER_FIELDS = ["model", "scenario", "init_params", "frequency", "timespan", "variable"]
    DISABLED_FIELDS = []

    def __init__(self, datapath, cds_list):
        self.datapath = datapath
        self.cds_list = self._get_cds_list(cds_list)
        self.download_widgets = self._create_filter_widgets()
        self.download_button = self._create_download_button()

    # Getting information from lists
    # ======================================================================== #

    @staticmethod
    def _get_cds_list(path):
        file = open(path)
        dictionary = json.load(file)
        return dictionary

    # Creating widgets
    # ======================================================================== #

    def _create_filter_widgets(self):
        filter_widgets = {}
        for field in self.FILTER_FIELDS:
            widget = Select(
                options = [],
                layout = {"width": "auto", "margin": "0 20px 0 0"},
                rows = 10)
            filter_widgets[field] = widget
        return filter_widgets

    def _create_download_button(self):
        download_button = Button(description = "Request data", icon = "download")
        download_button.on_click(self._click_download)
        return download_button

    # Action of download
    # ------------------------------------------------------------------------ #

    def _click_download(self, click):
        download_file = self.datapath + "download.tar.gz"
        c = cdsapi.Client()
        c.retrieve("sis-extreme-indices-cmip6", self.create_data_request(), download_file)
        file = tarfile.open(download_file)
        file.extractall(self.datapath)
        file.close()
        os.remove(download_file)

    # Download data
    # ........................................................................ #

    def create_data_request(self):
        data_request = {
            "version": "2_0",
            "format": "tgz",
            "model": self.widgets["model"].value.lower(),
            "ensemble_member": self.widgets["init_params"].value,
            "product_type": "base_period_1981_2010",
            "variable": self.widgets["variable"].value,
            "experiment": self.widgets["scenario"].value.lower().replace(".", "-"),
            "temporal_aggregation": self.widgets["frequency"].value,
            "period": self.widgets["timespan"].value}
        return data_request

    # Launch the widget
    # ======================================================================== #

    def render(self):
        self.download_widgets["model"].options = self.cds_list["model"]
        self.download_widgets["scenario"].options = self.cds_list["scenario"]
        self.download_widgets["init_params"].options = self.cds_list["init_params"]
        self.download_widgets["frequency"].options = list(self.cds_list["frequency"].keys())
        self.download_widgets["variable"].options = self.cds_list["variable"]
        self.download_widgets["frequency"].observe(self._check_frequency_update, names = "value")
        filters = []
        for field, widget in self.download_widgets.items():
            filters.append(VBox(
                [Label(field), widget],
                layout = {"flex": "1 1 100px", "width": "auto"}))
        download_header = Label("Request data:")
        download_widgets = HBox(filters)
        download_button = self.download_button
        app = VBox([download_header, download_widgets, download_button])
        return app

    # Update widget list
    # ------------------------------------------------------------------------ #

    def _check_frequency_update(self, change):
        self.download_widgets["timespan"].options = self.cds_list["frequency"][change.new]

