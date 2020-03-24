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
)


class PVChart(BaseChart):
    def __init__(
        self, date: typing.List, price: typing.List, volume: typing.List
    ):
        content = ChartContent(
            option=Eoption(
                dataset=[
                    Dataset(source=dict(date=date, price=price, volume=volume))
                ],
                xAxis=ExAxis(type=EaxisType.time),
                yAxis=[EyAxis(), EyAxis()],
                series=[
                    Eseries(
                        type="line",
                        encode=dict(x="date", y="close"),
                        yAxisIndex=0,
                    ),
                    Eseries(
                        type="bar",
                        encode=dict(x="date", y="volume"),
                        yAxisIndex=1,
                    ),
                ],
                tooltip=Etooltip(trigger=EtooltipTrigger.axis),
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
