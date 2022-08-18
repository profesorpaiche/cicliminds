import os
import json

from ipywidgets import Label, VBox, HBox, Button, Select

import cdsapi
import tarfile

# from cicliminds.widgets.common import ObserverWidget

class DownloadWidget:
    FILTER_FIELDS = ["model", "init_params", "frequency", "timespan", "scenario", "variable"]
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

    # FIXME: For the moment the daily frequency was removed to simplify the process
    def create_data_request(self):
        condition_list_1 = [
            "cold_days", "cold_nights", "cold_spell_duration_index",
            "extremely_wet_day_precipitation", "warm_days", "warm_nights",
            "very_wet_day_precipitation", "warm_spell_duration_index"]
        if self.download_widgets["variable"].value in condition_list_1:
            base_period = "base_period_1981_2010"
        else:
            base_period = "base_independent"
        data_request = {
            "version": "2_0",
            "format": "tgz",
            "model": self.download_widgets["model"].value.lower(),
            "ensemble_member": self.download_widgets["init_params"].value,
            "product_type": base_period,
            "variable": self.download_widgets["variable"].value,
            "experiment": self.download_widgets["scenario"].value.lower().replace(".", "_"),
            "temporal_aggregation": self.download_widgets["frequency"].value,
            "period": self.download_widgets["timespan"].value}
        return data_request

    # Launch the widget
    # ======================================================================== #

    def render(self):
        self.download_widgets["model"].options = self.cds_list["model"]
        self.download_widgets["frequency"].options = list(self.cds_list["frequency"].keys())
        self.download_widgets["model"].observe(self._update_init_params, names = "value")
        self.download_widgets["frequency"].observe(self._update_timespan, names = "value")
        self.download_widgets["frequency"].observe(self._update_variable, names = "value")
        self.download_widgets["timespan"].observe(self._update_scenario, names = "value")
        filters = []
        for field, widget in self.download_widgets.items():
            filters.append(VBox(
                [Label(field), widget],
                layout = {"width": "33%"}))
        download_header = Label("Request data:")
        download_widgets_up = HBox(filters[0:2])
        download_widgets_mid = HBox(filters[2:5])
        download_widgets_down = HBox(filters[5:6])
        download_button = self.download_button
        app = VBox([
            download_header,
            download_widgets_up,
            download_widgets_mid,
            download_widgets_down,
            download_button])
        return app

    # Update widget options
    # ------------------------------------------------------------------------ #

    def _update_init_params(self, change):
        condition_list_1 = [
            "ACCESS_CM2", "ACCESS_ESM1_5", "BCC_CSM2_MR",
            "EC_Earth3_Veg", "FGOALS_g3", "GFDL_CM4",
            "GFDL_ESM4", "INM_CM4_8", "INM_CM5_0",
            "KACE_1_0_G", "KIOST_ESM", "MPI_ESM1_2_HR",
            "MRI_ESM2_0", "NESM3", "NorESM2_LM", "NorESM2_MM"]
        condition_list_2 = [
            "CNRM_CM6_1", "CNRM_CM6_1_HR", "CNRM_ESM2_1",
            "MIROC_ES2L", "UKESM1_0_LL"]
        condition_list_3 = ["HadGEM3_GC31_LL", "HadGEM3_GC31_MM"]
        condition_list_4 = ["EC_Earth3"]
        condition_list_5 = ["MPI_ESM1_2_LR"]
        condition_list_6 = ["MIROC6"]
        condition_list_7 = ["CanESM5"]
        if change.new in condition_list_1:
            self.download_widgets["init_params"].options = ["r1i1p1f1"]
        elif change.new in condition_list_2:
            self.download_widgets["init_params"].options = ["r1i1p1f2"]
        elif change.new in condition_list_3:
            self.download_widgets["init_params"].options = ["r1i1p1f3"]
        elif change.new in condition_list_4:
            num = [1, 4, 6, 9, 11, 13, 15]
            self.download_widgets["init_params"].options = ["r" + str(i) + "i1p1f1" for i in num]
        elif change.new in condition_list_5:
            self.download_widgets["init_params"].options = ["r" + str(i) + "i1p1f1" for i in range(1,11)]
        elif change.new in condition_list_6:
            self.download_widgets["init_params"].options = ["r" + str(i) + "i1p1f1" for i in range(1,51)]
        elif change.new in condition_list_7:
            option_list_1 = ["r" + str(i) + "i1p1f1" for i in range(1,26)]
            option_list_2 = ["r" + str(i) + "i1p2f1" for i in range(1,26)]
            self.download_widgets["init_params"].options = option_list_1 + option_list_2

    def _update_scenario(self, change):
        date_int = int(change.new[0])
        if date_int < 2:
            self.download_widgets["scenario"].options = ["Historical"]
        else:
            self.download_widgets["scenario"].options = ["SSP1_2.6", "SSP2_4.5", "SSP5_8.5"]

    def _update_timespan(self, change):
        self.download_widgets["timespan"].options = self.cds_list["frequency"][change.new]["timespan"]

    def _update_variable(self, change):
        self.download_widgets["variable"].options = self.cds_list["frequency"][change.new]["variable"]
