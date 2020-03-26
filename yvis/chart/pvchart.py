import typing
from .base import (
    BaseChart,
    ChartContent,
    Dataset,
    Eoption,
    Eseries,
    ExAxis,
    EyAxis,
    EaxisType,
    UpdateChartContent,
    UpdateOption,
    Etooltip,
    EtooltipTrigger,
    EdataZoom,
    EdataZoomType,
    EmarkLine,
)


class PVChart(BaseChart):
    def __init__(
        self,
        date: typing.List,
        price: typing.List,
        volume: typing.List,
        price_max: float = None,
        price_min: float = None,
        price_ref: float = None,
    ):
        content = ChartContent(
            option=Eoption(
                dataset=[
                    Dataset(source=dict(date=date, price=price, volume=volume))
                ],
                xAxis=ExAxis(type=EaxisType.time),
                yAxis=[EyAxis(max=price_max, min=price_min), EyAxis()],
                series=[
                    Eseries(
                        type="line",
                        encode=dict(x="date", y="close"),
                        yAxisIndex=0,
                        markLine=EmarkLine(data=[{"yAxis": price_ref}]),
                    ),
                    Eseries(
                        type="bar",
                        encode=dict(x="date", y="volume"),
                        yAxisIndex=1,
                    ),
                ],
                tooltip=Etooltip(trigger=EtooltipTrigger.axis),
                dataZoom=[
                    EdataZoom(type=EdataZoomType.inside, xAxisIndex=[0,]),
                    EdataZoom(type=EdataZoomType.slider, xAxisIndex=[0,]),
                ],
                animation=False,
            )
        )
        super().__init__(content)

    def update(
        self, date: typing.List, price: typing.List, volume: typing.List
    ):
        content = UpdateChartContent(
            option=UpdateOption(
                dataset=[
                    Dataset(source=dict(date=date, price=price, volume=volume)),
                ]
            )
        )
        super().update(content)
