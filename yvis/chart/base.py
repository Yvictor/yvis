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
    max: float = None
    min: float = None


class EtooltipTrigger(str, Enum):
    item = "item"
    axis = "axis"
    none = "none"


class EaxisPointType(str, Enum):
    line = "line"
    shadow = "shadow"
    none = "none"
    cross = "cross"


class EaxisPoint(Base):
    type: EaxisPointType = EaxisPointType.cross


class Etooltip(Base):
    trigger: EtooltipTrigger = EtooltipTrigger.axis
    axisPointer: EaxisPoint = EaxisPoint()
    position: typing.Union[typing.List[str], typing.List[int]] = ["90%", "10%"]


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


class EdataZoomType(str, Enum):
    slider = "slider"
    inside = "inside"


class EdataZoom(Base):
    type: EdataZoomType = None
    start: int = 0
    end: int = 100
    xAxisIndex: typing.List[int] = None


class ElineSymbol(str, Enum):
    circle = "circle"
    rect = "rect"
    roundRect = "roundRect"
    triangle = "triangle"
    diamond = "diamond"
    pin = "pin"
    arrow = "arrow"
    none = "none"


class Elabel(Base):
    show: bool = True
    position: str = "start"

class EmarkLine(Base):
    symbol: typing.Union[
        ElineSymbol, typing.List[ElineSymbol]
    ] = ElineSymbol.none
    data: typing.List = None
    label: Elabel = Elabel()


class Eseries(Base):
    type: SeriesType
    encode: dict
    yAxisIndex: int = None
    showSymbol: bool = False
    markLine: EmarkLine = None


class Eoption(Base):
    dataset: typing.List[Dataset]
    xAxis: typing.Union[ExAxis, typing.List[ExAxis]] = ExAxis()
    yAxis: typing.Union[EyAxis, typing.List[EyAxis]] = EyAxis()
    series: typing.List[Eseries]
    tooltip: Etooltip = Etooltip()
    dataZoom: typing.List[EdataZoom] = None
    animation: bool = False


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
