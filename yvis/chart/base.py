import typing
from enum import Enum
from yvis.core import Base, DisplayCore, MetaContent, Dataset, UpdateContent


class EaxisType(str, Enum):
    value = "value"
    category = "category"
    time = "time"
    log = "log"


class ExAxis(Base):
    type: EaxisType = EaxisType.value
    scale: bool = True


class EyAxis(Base):
    type: EaxisType = EaxisType.value
    scale: bool = True


class SeriesType(str, Enum):
    line = "line"
    bar = "bar"
    pie = "pie"
    scatter = "scatter"
    effectScatter = "effectScatter"
    radar = "radar"
    tree = "tree"
    treemap = "treemap"
    sunburst = "sunburst"
    boxplot = "boxplot"
    candlestick = "candlestick"
    heatmap = "heatmap"
    map = "map"
    parallel = "parallel"
    lines = "lines"
    graph = "graph"
    sankey = "sankey"
    funnel = "funnel"
    gauge = "gauge"
    pictorialBar = "pictorialBar"
    themeRiver = "themeRiver"
    custom = "customs"


class Eseries(Base):
    type: SeriesType
    encode: dict
    yAxisIndex: int = None


class Eoption(Base):
    dataset: typing.List[Dataset]
    xAxis: typing.Union[ExAxis, typing.List[ExAxis]] = ExAxis()
    yAxis: typing.Union[EyAxis, typing.List[EyAxis]] = EyAxis()
    series: typing.List[Eseries]


class UpdateOption(Base):
    dataset: typing.List[Dataset]


class ChartContent(Base):
    meta: MetaContent = MetaContent()
    option: Eoption


class UpdateChartContent(UpdateContent):
    option: UpdateOption


class BaseChart(DisplayCore):
    def __init__(self, content: ChartContent):
        super().__init__(content)

    def update(self, content: UpdateChartContent):
        for idx, dataset in enumerate(content.option.dataset):
            for col, value in dataset.source.items():
                self.content.option.dataset[idx].source[col].extend(value)
        self.display_update(content)