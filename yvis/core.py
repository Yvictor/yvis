from IPython.display import display, DisplayHandle
from pydantic import BaseModel
import typing
from enum import Enum


class Base(BaseModel):
    @classmethod
    def _get_value(
        cls,
        v: typing.Any,
        to_dict: bool,
        by_alias: bool,
        include: typing.Optional[
            typing.Union["AbstractSetIntStr", "DictIntStrAny"]],
        exclude: typing.Optional[
            typing.Union["AbstractSetIntStr", "DictIntStrAny"]],
        exclude_unset: bool,
        exclude_defaults: bool,
        # exclude_none: bool,
    ) -> typing.Any:
        if to_dict and isinstance(v, Enum):
            return v.value
        return super()._get_value(
            v,
            to_dict,
            by_alias,
            include,
            exclude,
            exclude_unset,
            exclude_defaults,
            # exclude_none,
        )


class Scope(str, Enum):
    init = 'init'
    update = 'update'
    append = 'append'


class MetaContent(Base):
    scope: Scope = Scope.init
    height: typing.Union[str, int] = '600px'
    width: typing.Union[str, int] = '800px'


class BaseContent(Base):
    meta: MetaContent = MetaContent()
    option: typing.Dict[str, typing.Any]


class Dataset(Base):
    source: typing.Dict[str, list]


class BaseOption(Base):
    dataset: typing.List[Dataset]


class UpdateContent(BaseContent):
    meta: MetaContent = MetaContent(scope=Scope.append)
    option: BaseOption


class DisplayCore:
    def __init__(self, content: BaseContent):
        self._app: str = "application/vnd.yvis.v1+json"
        self.content: BaseContent = content
        self.display_handle: DisplayHandle = None
        if not self.display_handle:
            self.display(self.content)

    def display(self, content: BaseContent):
        self.display_handle = display(
            {self._app: content.dict()}, raw=True, display_id=True
        )

    @staticmethod
    def update_data(data: dict, update_data: dict):
        for key, value in data.items():
            if isinstance(value, list):
                update_data[key].append(*value)
            elif isinstance(value, dict):
                update_data[key] = update_data(value, update_data[key])
            else:
                update_data[key] = value

    def update(self, content: UpdateContent):
        # self.update_data(content.option.dict(), self.content.option)
        for idx, dataset in enumerate(content.option.dataset):
            for col, value in dataset.source.items():
                self.content.option['dataset'][idx]['source'][col].extend(value)
        self.display_handle.update({self._app: content.dict()}, raw=True)
