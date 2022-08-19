from functools import partial

import numpy as np
import pandas as pd
from ipywidgets import Label, VBox, HBox, Button, SelectMultiple

from cicliminds.widgets.common import ObserverWidget
from cicliminds_lib.query.datasets import get_shallow_filters_mask
from cicliminds_lib.query.files import get_datasets
from cicliminds.interface.query_builder.filter_expander import expand_model_scenarios


class FilterWidget(ObserverWidget):
    FILTER_FIELDS = ["model", "scenario", "init_params", "frequency", "timespan", "variable"]
    DISABLED_FIELDS = ["timespan"]

    def __init__(self, datapath):
        self.datapath = datapath
        self.datasets = get_datasets(self.datapath)
        self.button_reset = self._get_reset_button()
        self.button_refresh = self._get_refresh_button()
        self.button_reload = self._get_reload_button()
        self.filter_widgets = self._get_filter_widgets()
        super().__init__()

    def render(self):
        filter_controls = HBox([self.button_reset, self.button_refresh, self.button_reload])
        filter_widget_panel = self._get_filter_widget_panel()
        filter_widget = VBox([Label("Configuration filter:"),
                              filter_widget_panel,
                              filter_controls])
        return filter_widget

    def get_filtered_dataset(self, agg_params):
        filter_values = self.get_filter_values()
        mask = get_shallow_filters_mask(self.datasets, filter_values)
        if np.count_nonzero(mask) < 200:
            mask = mask & self.get_scenarios_mask(self.datasets, mask,
                                                  agg_params["aggregate_scenarios"], agg_params["aggregate_years"],
                                                  filter_values)
        return self.datasets[mask].copy()

    @staticmethod
    def get_scenarios_mask(datasets_reg, mask, agg_scenarios, agg_years, query):
        blocks_with_mask = [(query, mask)]
        scenarios_mask = pd.Series(np.full(datasets_reg.shape[0], False), index=datasets_reg.index)
        for _, partial_mask in expand_model_scenarios(blocks_with_mask, query, agg_scenarios, agg_years, datasets_reg):
            scenarios_mask = scenarios_mask | partial_mask
        return scenarios_mask

    def get_filter_values(self):
        res = {}
        for field, widget in self.filter_widgets.items():
            values = list(widget.value)
            res[field] = values
        return res

    def update_state_from_dataset(self, partial_dataset):
        for field, widget in self.filter_widgets.items():
            if widget.value:
                continue
            widget.options = partial_dataset[field].unique()
            widget.notify_change({"type": "change", "name": "options", "new": widget.options})

    def reset_filters(self):
        for widget in self.filter_widgets.values():
            widget.values = tuple()
            widget.notify_change({"type": "change", "name": "value", "new": widget.values})

    def _get_filter_widget_panel(self):
        filters = []
        for field, widget in self.filter_widgets.items():
            filters.append(VBox([Label(field), widget], layout={"flex": "1 1 100px", "width": "auto"}))
        filter_widget = HBox(filters)
        return filter_widget

    def _get_reset_button(self):
        button_reset = Button(description="Reset filter", button_style="danger", icon="broom")
        button_reset.on_click(self._reset_filters)
        return button_reset

    def _reset_filters(self, change):  # pylint: disable=unused-argument
        self.reset_filters()

    def _get_refresh_button(self):
        button_refresh = Button(description="Refresh filters", button_style="success", icon="redo")
        button_refresh.on_click(self.trigger)
        return button_refresh

    def _get_reload_button(self):
        button_reload = Button(description="Reaload filter", button_style="info", icon="redo")
        button_reload.on_click(self._reload_filters)
        return button_reload

    def _reload_filters(self, change):
        self.datasets = get_datasets(self.datapath)
        for field in self.FILTER_FIELDS:
            self.filter_widgets[field].options = self.datasets[field].unique()

    def _get_filter_widgets(self):
        filter_widgets = {}
        for field in self.FILTER_FIELDS:
            widget = SelectMultiple(
                options=self.datasets[field].unique(),
                layout={"width": "auto", "margin": "0 20px 0 0"},
                rows=10,
                disabled=field in self.DISABLED_FIELDS)
            widget.observe(partial(self.propagate, [widget]), names="value")
            filter_widgets[field] = widget
        return filter_widgets
