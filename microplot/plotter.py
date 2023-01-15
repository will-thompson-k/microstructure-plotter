"""
This module contains the microstructure plotter.
"""

from enable.api import ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import Handler, Item, View

from chaco.scales.api import CalendarScaleSystem
from chaco.scales_tick_generator import ScalesTickGenerator
from chaco.tools.api import PanTool, ZoomTool
from chaco.api import ArrayPlotData, Plot, PlotAxis, PlotGrid, VPlotContainer

from microplot.data import PlotterDataClass


class DummyPlotterHandler(Handler):
    """
    This is a "dummy" plotter handler class.
    This forces a silent close of the plotter.
    """

    def closed(self, info, is_ok):
        return


class MicroPlotter(HasTraits):
    """
    This is the microstructure plotting class.
    """

    container = Instance(VPlotContainer)

    traits_view = View(
        Item("container", editor=ComponentEditor(), show_label=False),
        width=900,
        height=500,
        resizable=True,
        title="Microstructure Plotter",
        handler=DummyPlotterHandler,
    )

    def __init__(self, data: PlotterDataClass, show_legend: bool = False):
        """
        Args:
            data (PlotterDataClass): dataclass for plotting object.
            show_legend (bool): flag to show legend on plots. Crowded image. Default = False.
        """

        # plotterdataclass ingested from datasource
        self._data = data
        # flag to show legend in plots (warning: crowds screen)
        self._show_legend = show_legend
        # find union of symbols across time series
        self._symbols = data.get_symbols()

        # to cache Plot objects
        self._subplots = []
        # to be used later for connecting plots
        self._top_plot_indexer = None
        self._top_plot_index_range = None
        self._top_plot_bottom_axis = None

        super().__init__()

    def plot(self, *args, **kws):
        """
        One stop "public" method for rendering all plots.

        Call this after instantiating object to render plots.

        Raises:
            Exception: HasTraits:: unable to configure.
        """

        try:
            super().configure_traits(*args, **kws)
        except:
            raise Exception("Unable to configure traits.")

    def _container_default(self) -> VPlotContainer:
        """
        Required method for HasTraits class to return a
        "Vertical Plot Container" object containing
        the plots of interest.

        Returns:
            VPlotContainer: Container object with
            the subplots of interest.
        """

        return self._generate_subplots()

    def _generate_subplots(self) -> VPlotContainer:
        """
        Method for instantiating the VPlotContainer.
        Creates subplot Plot objects for each symbol.

        Returns:
            VPlotContainer: Container object with
            the subplots of interest.
        """

        # run through each symbol, instantiate subplots
        for symbol in self._symbols:
            plot = self._generate_subplot(symbol)
            self._link_subplot(plot)

        # instantiate a container to hold all the plots
        container = VPlotContainer(bgcolor="transparent")

        # add all the linked sub-plots to the VPlotContainer
        for plot in self._subplots:
            container.add(plot)
        # clear cache
        self._subplots = []

        return container

    def _generate_subplot(self, symbol: str) -> Plot:
        """
        For a given symbol, instantiate a subplot
        timeseries with all the relevant plot datapoints.

        Args:
            symbol (str): The symbol of interest.

        Returns:
            Plot: The subplot object for a given symbol.
        """
        # set plot data
        data_array = self._set_plot_data_array(symbol)
        plot_attributes = set(data_array.list_data())

        # instantiate plot object
        plot = Plot(data_array, auto_grid=False, auto_axis=False)

        # render plots
        self._render_plots(plot, plot_attributes)

        # setup plot stuff
        self._setup_plot(plot, symbol)

        return plot

    def _setup_plot(self, plot: Plot, symbol: str):
        """
        Setup Plot attributes (zooming, etc).

        Args:
            plot (Plot): The Plot class (for a given symbol).
            symbol (str): The symbol of interest.
        """

        # setup plot details
        plot.title = "Symbol: %s " % (symbol)
        plot.legend.visible = self._show_legend

        # create pan tool
        plot.tools.append(PanTool(plot))
        # create zooming ability
        zoom_controller = ZoomTool(
            component=plot, tool_mode="box", drag_button="right", always_on=True
        )
        plot.overlays.append(zoom_controller)
        # setup plot axis
        left_axis = PlotAxis(plot, orientation="left")
        plot.overlays.append(left_axis)
        # setup plot grid
        h_mapper = plot.value_mapper
        h_grid = PlotGrid(
            mapper=h_mapper,
            orientation="horizontal",
            component=plot,
            line_color="lightgray",
            line_style="dot",
        )
        plot.underlays.append(h_grid)

    def _render_plots(self, plot: Plot, plot_attributes: set):
        """
        Render Plot elements within instantiated class. Set title and other properties.

        Args:
            plot (Plot): The Plot class (for a given symbol).
            plot_attributes (set): plot attributes set in data_array object.
        """
        # quote_data
        if "quote_timestamp" in plot_attributes:
            plot.plot(
                ("quote_timestamp", "quote_bid_price"),
                line_width=4,
                name="bid_price",
                color="black",
                line_style="solid",
                render_style="connectedhold",
            )
            plot.plot(
                ("quote_timestamp", "quote_ask_price"),
                line_width=4,
                name="ask_price",
                color="black",
                line_style="solid",
                render_style="connectedhold",
            )
            plot.plot(
                ("quote_timestamp", "quote_micro_price"),
                line_width=1,
                name="micro_price",
                color="blue",
                line_style="solid",
                render_style="connectedhold",
            )

        # trade_data
        if "trade_timestamp" in plot_attributes:
            plot.plot(
                ("trade_timestamp", "trade_price"),
                type="scatter",
                marker="circle",
                name="trade_price",
                color="red",
                marker_size=8,
                render_style="hold",
            )

        # aggr_buy_sim
        if "sim_aggr_buy_timestamp" in plot_attributes:
            plot.plot(
                ("sim_aggr_buy_timestamp", "sim_aggr_buy_price"),
                type="scatter",
                marker="triangle",
                name="sim_aggr_buy_price",
                color="blue",
                marker_size=12,
                render_style="hold",
            )

        # pass_buy_sim
        if "sim_pass_buy_timestamp" in plot_attributes:
            plot.plot(
                ("sim_pass_buy_timestamp", "sim_pass_buy_price"),
                type="scatter",
                marker="circle",
                name="sim_pass_buy_price",
                color="blue",
                marker_size=12,
                render_style="hold",
            )

        # aggr_sell_sim
        if "sim_aggr_sell_timestamp" in plot_attributes:
            plot.plot(
                ("sim_aggr_sell_timestamp", "sim_aggr_sell_price"),
                type="scatter",
                marker="triangle",
                name="sim_aggr_sell_price",
                color="gold",
                marker_size=12,
                render_style="hold",
            )

        # pass_sell_sim
        if "sim_pass_sell_timestamp" in plot_attributes:
            plot.plot(
                ("sim_pass_sell_timestamp", "sim_pass_sell_price"),
                type="scatter",
                marker="circle",
                name="sim_pass_sell_price",
                color="gold",
                marker_size=12,
                render_style="hold",
            )

        # aggr_buy_prod
        if "prod_aggr_buy_timestamp" in plot_attributes:
            plot.plot(
                ("prod_aggr_buy_timestamp", "prod_aggr_buy_price"),
                type="scatter",
                marker="triangle",
                name="prod_aggr_buy_price",
                color="purple",
                marker_size=12,
                render_style="hold",
            )

        # pass_buy_prod
        if "prod_pass_buy_timestamp" in plot_attributes:
            plot.plot(
                ("prod_pass_buy_timestamp", "prod_pass_buy_price"),
                type="scatter",
                marker="circle",
                name="prod_pass_buy_price",
                color="purple",
                marker_size=12,
                render_style="hold",
            )

        # aggr_sell_prod
        if "prod_aggr_sell_timestamp" in plot_attributes:
            plot.plot(
                ("prod_aggr_sell_timestamp", "prod_aggr_sell_price"),
                type="scatter",
                marker="triangle",
                name="prod_aggr_sell_price",
                color="green",
                marker_size=12,
                render_style="hold",
            )

        # pass_sell_prod
        if "prod_pass_sell_timestamp" in plot_attributes:
            plot.plot(
                ("prod_pass_sell_timestamp", "prod_pass_sell_price"),
                type="scatter",
                marker="circle",
                name="prod_pass_sell_price",
                color="green",
                marker_size=12,
                render_style="hold",
            )

        # new_orders
        if "new_order_timestamp" in plot_attributes:
            plot.plot(
                ("new_order_timestamp", "new_order_price"),
                type="scatter",
                marker="diamond",
                name="new_order_price",
                color="green",
                marker_size=6,
                render_style="hold",
            )

        # new_order_acks
        if "new_order_ack_timestamp" in plot_attributes:
            plot.plot(
                ("new_order_ack_timestamp", "new_order_ack_price"),
                type="scatter",
                marker="diamond",
                name="new_order_ack_price",
                color="lightgreen",
                marker_size=6,
                render_style="hold",
            )

        # cancel_orders
        if "cancel_order_timestamp" in plot_attributes:
            plot.plot(
                ("cancel_order_timestamp", "cancel_order_price"),
                type="scatter",
                marker="diamond",
                name="cancel_order_price",
                color="red",
                marker_size=6,
                render_style="hold",
            )

        # cancel_order_acks
        if "cancel_order_ack_timestamp" in plot_attributes:
            plot.plot(
                ("cancel_order_ack_timestamp", "cancel_order_ack_price"),
                type="scatter",
                marker="diamond",
                name="cancel_order_ack_price",
                color="pink",
                marker_size=6,
                render_style="hold",
            )

        # rejects
        if "reject_orders_timestamp" in plot_attributes:
            plot.plot(
                ("reject_orders_timestamp", "reject_orders_price"),
                type="scatter",
                marker="diamond",
                name="reject_orders_price",
                color="black",
                marker_size=6,
                render_style="hold",
            )

        # val_data
        if "val_data_timestamp" in plot_attributes:
            plot.plot(
                ("val_data_timestamp", "val_data_price"),
                color="green",
                line_style="solid",
                name="val_data_price",
                line_width=1,
                render_style="connectedhold",
            )

    def _set_plot_data_array(self, symbol: str) -> ArrayPlotData:
        """
        Instantiate ArrayPlotData class for Plot object.

        Args:
            symbol (str): The symbol of interest.

        Returns:
            ArrayPlotData: The array plot data class with required data fields set.
        """

        array_plot_data = ArrayPlotData()

        # quote data
        quote_data = self._data.quote_data
        if quote_data is not None:
            quote_data = self._data.quote_data[
                self._data.quote_data["symbol"] == symbol
            ]
            array_plot_data.set_data("quote_timestamp", quote_data.timestamp.ravel())
            array_plot_data.set_data("quote_bid_price", quote_data.bid_price.ravel())
            array_plot_data.set_data("quote_ask_price", quote_data.ask_price.ravel())
            array_plot_data.set_data(
                "quote_micro_price", quote_data.micro_price.ravel()
            )

        # trade data
        trade_data = self._data.trade_data
        if trade_data is not None:
            trade_data = self._data.trade_data[
                self._data.trade_data["symbol"] == symbol
            ]
            array_plot_data.set_data("trade_timestamp", trade_data.timestamp.ravel())
            array_plot_data.set_data("trade_price", trade_data.price.ravel())

        # fill data - sim
        (
            buy_aggressive_fills,
            buy_passive_fills,
            sell_aggressive_fills,
            sell_passive_fills,
        ) = self._data.fill_data_sim
        # aggr_buy
        if not (buy_aggressive_fills is None or buy_aggressive_fills.empty):
            buy_aggressive_fills = buy_aggressive_fills[
                buy_aggressive_fills["symbol"] == symbol
            ]
            array_plot_data.set_data(
                "sim_aggr_buy_timestamp", buy_aggressive_fills.timestamp.ravel()
            )
            array_plot_data.set_data(
                "sim_aggr_buy_price", buy_aggressive_fills.price.ravel()
            )
        # pass_buy
        if not (buy_passive_fills is None or buy_passive_fills.empty):
            buy_passive_fills = buy_passive_fills[buy_passive_fills["symbol"] == symbol]
            array_plot_data.set_data(
                "sim_pass_buy_timestamp", buy_passive_fills.timestamp.ravel()
            )
            array_plot_data.set_data(
                "sim_pass_buy_price", buy_passive_fills.price.ravel()
            )
        # aggr_sell
        if not (sell_aggressive_fills is None or sell_aggressive_fills.empty):
            sell_aggressive_fills = sell_aggressive_fills[
                sell_aggressive_fills["symbol"] == symbol
            ]
            array_plot_data.set_data(
                "sim_aggr_sell_timestamp", sell_aggressive_fills.timestamp.ravel()
            )
            array_plot_data.set_data(
                "sim_aggr_sell_price", sell_aggressive_fills.price.ravel()
            )
        # pass_sell
        if not (sell_passive_fills is None or sell_passive_fills.empty):
            sell_passive_fills = sell_passive_fills[
                sell_passive_fills["symbol"] == symbol
            ]
            array_plot_data.set_data(
                "sim_pass_sell_timestamp", sell_passive_fills.timestamp.ravel()
            )
            array_plot_data.set_data(
                "sim_pass_sell_price", sell_passive_fills.price.ravel()
            )

        # fill data - prod
        (
            buy_aggressive_fills,
            buy_passive_fills,
            sell_aggressive_fills,
            sell_passive_fills,
        ) = self._data.fill_data_prod
        # aggr_buy
        if not (buy_aggressive_fills is None or buy_aggressive_fills.empty):
            buy_aggressive_fills = buy_aggressive_fills[
                buy_aggressive_fills["symbol"] == symbol
            ]
            array_plot_data.set_data(
                "prod_aggr_buy_timestamp", buy_aggressive_fills.timestamp.ravel()
            )
            array_plot_data.set_data(
                "prod_aggr_buy_price", buy_aggressive_fills.price.ravel()
            )
        # pass_buy
        if not (buy_passive_fills is None or buy_passive_fills.empty):
            buy_passive_fills = buy_passive_fills[buy_passive_fills["symbol"] == symbol]
            array_plot_data.set_data(
                "prod_pass_buy_timestamp", buy_passive_fills.timestamp.ravel()
            )
            array_plot_data.set_data(
                "prod_pass_buy_price", buy_passive_fills.price.ravel()
            )
        # aggr_sell
        if not (sell_aggressive_fills is None or sell_aggressive_fills.empty):
            sell_aggressive_fills = sell_aggressive_fills[
                sell_aggressive_fills["symbol"] == symbol
            ]
            array_plot_data.set_data(
                "prod_aggr_sell_timestamp", sell_aggressive_fills.timestamp.ravel()
            )
            array_plot_data.set_data(
                "prod_aggr_sell_price", sell_aggressive_fills.price.ravel()
            )
        # pass_sell
        if not (sell_passive_fills is None or sell_passive_fills.empty):
            sell_passive_fills = sell_passive_fills[
                sell_passive_fills["symbol"] == symbol
            ]
            array_plot_data.set_data(
                "prod_pass_sell_timestamp", sell_passive_fills.timestamp.ravel()
            )
            array_plot_data.set_data(
                "prod_pass_sell_price", sell_passive_fills.price.ravel()
            )

        # orders
        self._data.orders
        (
            new_orders,
            new_order_acks,
            cancel_orders,
            cancel_order_acks,
            rejects,
        ) = self._data.orders
        # new orders
        if not (new_orders is None or new_orders.empty):
            new_orders = new_orders[new_orders["symbol"] == symbol]
            array_plot_data.set_data(
                "new_order_timestamp", new_orders.timestamp.ravel()
            )
            array_plot_data.set_data("new_order_price", new_orders.price.ravel())
        # new orders - ack
        if not (new_order_acks is None or new_order_acks.empty):
            new_order_acks = new_order_acks[new_order_acks["symbol"] == symbol]
            array_plot_data.set_data(
                "new_order_ack_timestamp", new_order_acks.timestamp.ravel()
            )
            array_plot_data.set_data(
                "new_order_ack_price", new_order_acks.price.ravel()
            )
        # cancels
        if not (cancel_orders is None or cancel_orders.empty):
            cancel_orders = cancel_orders[cancel_orders["symbol"] == symbol]
            array_plot_data.set_data(
                "cancel_order_timestamp", cancel_orders.timestamp.ravel()
            )
            array_plot_data.set_data("cancel_order_price", cancel_orders.price.ravel())
        # cancels - ack
        if not (cancel_order_acks is None or cancel_order_acks.empty):
            cancel_order_acks = cancel_order_acks[cancel_order_acks["symbol"] == symbol]
            array_plot_data.set_data(
                "cancel_order_ack_timestamp", cancel_order_acks.timestamp.ravel()
            )
            array_plot_data.set_data(
                "cancel_order_ack_price", cancel_order_acks.price.ravel()
            )
        # rejects
        if not (rejects is None or rejects.empty):
            rejects = rejects[rejects["symbol"] == symbol]
            array_plot_data.set_data(
                "reject_orders_timestamp", rejects.timestamp.ravel()
            )
            array_plot_data.set_data("reject_orders_price", rejects.price.ravel())

        # val data
        val_data = self._data.val_data
        if val_data is not None:
            val_data = self._data.val_data[self._data.val_data["symbol"] == symbol]
            array_plot_data.set_data("val_data_timestamp", val_data.timestamp.ravel())
            array_plot_data.set_data("val_data_price", val_data.theo_price.ravel())

        return array_plot_data

    def _link_subplot(self, plot: Plot):
        """
        Link a subplot object to others via PlotAxis object.

        Args:
            plot (Plot): The subplot Plot object.
        """

        if self._top_plot_indexer is None:
            # add a calendar-based timescale on the x-axis
            bottom_axis = PlotAxis(
                plot,
                orientation="bottom",
                tick_generator=ScalesTickGenerator(scale=CalendarScaleSystem()),
            )
            plot.underlays.append(bottom_axis)
            # persist plot::indexer and plotaxis - need indices and tick_generator to link axes later
            self._top_plot_indexer = plot.index_mapper
            self._top_plot_index_range = plot.index_range
            self._top_plot_bottom_axis = bottom_axis
        else:
            bottom_axis = PlotAxis(
                plot,
                orientation="bottom",
                # link the first plot's index mapper
                mapper=self._top_plot_indexer,
                tick_generator=ScalesTickGenerator(scale=CalendarScaleSystem()),
            )
            # link other attributes
            bottom_axis.tick_generator = self._top_plot_bottom_axis.tick_generator
            plot.index_range = self._top_plot_index_range
            plot.underlays.append(bottom_axis)

        # store to be added to VPlot later
        self._subplots.append(plot)
