import json
import typing as t


class Request:
    def __init__(
        self,
        args: t.Dict[str, str],
        form: t.Dict[str, str],
        data_str: str,
        is_json: bool,
        method: str,
    ) -> None:
        """
        Arguments:
            * `args`: URL parameter arguments (after question mark on URL).
            * `form`: Form parameters.
            * `data_str`: String representation of the data stream.
            * `is_json`: Whether the give data is JSON or not.
            * `method`: HTTP Method
        """

        # TODO: Change types of `args` and `form` to MultiDict.
        self._args = args
        self._form = form
        self._data_str = data_str
        self._is_json = is_json
        self._method = method

    @property
    def args(self) -> t.Dict[str, str]:
        return self._args

    @property
    def form(self) -> t.Dict[str, str]:
        return self._form

    @property
    def json(self) -> t.Optional[t.Any]:
        return self.get_json()

    @property
    def is_json(self) -> bool:
        return self._is_json

    @property
    def method(self) -> str:
        return self._method

    def get_data(self, as_text: bool = False) -> t.Union[bytes, str]:
        if as_text:
            return self._data_str
        return self._data_str.encode(encoding="utf-8")

    def get_json(self) -> t.Optional[t.Any]:
        if not self.is_json:
            return None
        return json.loads(self._data_str)
