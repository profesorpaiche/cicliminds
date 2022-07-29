import os
import json

import ipywidgets as widgets

import cdsapi
import tarfile

class AppCDS:
    def __init__(self, datapath, cds_list):
        self.datapath = datapath
        self.json_file = cds_list
        self.dictionary = self._get_list() # -> maybe this is the only one needed
        self.model = self.dictionary["model"]
        self.scenario = self.dictionary["scenario"] # FIXME: Convert . to _
        self.init_params = self.dictionary["init_params"]
        self.frequency_dict = self.dictionary["frequency"]
        self.frequency = list( self.frequency_dict.keys() )
        self.timespan = self.frequency_dict[self.frequency[0]]
        self.variable = self.dictionary["variable"]
        self.widgets = {}
        self.widgets["model"] = self._create_simple_widget(options = self.model)
        self.widgets["scenario"] = self._create_simple_widget(options = self.scenario)
        self.widgets["init_params"] = self._create_simple_widget(options = self.init_params)
        self.widgets["frequency"] = self._create_simple_widget(options = self.frequency)
        self.widgets["timespan"] = self._create_simple_widget(options = None)
        self.widgets["variable"] = self._create_simple_widget(options = self.variable)

    # Getting information from lists
    # ........................................................................ #

    def _get_list(self):
        file = open(self.json_file)
        dictionary = json.load(file)
        return dictionary

    # Creating widgets
    # ........................................................................ #

    def _create_simple_widget(self, options):
        simple_widget = widgets.Select(layout = {"width": "auto", "margin": "0 20px 0 0"})
        if options is not None:
            simple_widget.options = options
        return simple_widget

    # Launch the app.
    # ======================================================================== #

    def render(self):
        self.widgets["frequency"].observe(self._check_frequency_update, names = "value")
        widgets_list = []
        for field, widget in self.widgets.items():
            widgets_list.append( widgets.VBox(
                                    [widgets.Label(field), widget],
                                    layout = {"flex": "1 1 100px", "width": "auto"}) )
        widget_request = widgets.HBox(widgets_list)
        widget_download = widgets.Button(description = "Request data", icon = "download")
        widget_download.on_click(self._click_download)
        app = widgets.VBox([widget_request, widget_download], layout = {"flex": "1 1 100px"})
        return app

    # React to widgets
    # ........................................................................ #

    def _check_frequency_update(self, change):
        self.widgets["timespan"].options = self.frequency_dict[change.new]

    def _click_download(self, b):
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
            "experiment": self.widgets["scenario"].value.lower(),
            "temporal_aggregation": self.widgets["frequency"].value,
            "period": self.widgets["timespan"].value}
        return data_request
