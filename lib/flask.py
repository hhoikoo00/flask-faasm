import ast
import inspect
import json
import logging
from functools import update_wrapper
from itertools import dropwhile
from typing import Any, Callable, Generator

from flask import Flask, request

from lib.constants import FAASM_FUNC_TEMPLATE_FILE
from lib.faasm import invoke_py_func, upload_py_func
from lib.imports import Import, ImportFrom, ImportVisitor
from lib.request import Request

logger = logging.getLogger(__name__)


FAASM_FUNC_TEMPLATE = FAASM_FUNC_TEMPLATE_FILE.read_text(encoding="utf-8")
FLASK_MODULE_NAME = "flask"


def view_funcs_iter(app: Flask) -> Generator[tuple[str, Callable[..., Any]], None, None]:
    """Return a wrapper around `app.view_functions.items()` that filters out irrelevant endpoints e.g. 'static'."""

    for endpoint, view_func in app.view_functions.items():  # type: ignore
        # Skip "static" endpoints as they only host static assets.
        if endpoint == "static":
            continue

        yield endpoint, view_func


def get_view_func_source(view_func: Callable[..., Any]) -> str:
    view_func_lines, _ = inspect.getsourcelines(view_func)
    view_func_lines_no_decorators = dropwhile(lambda line: line.startswith("@"), view_func_lines)
    view_func_source = "".join(view_func_lines_no_decorators)
    return view_func_source


def is_flask_import(import_obj: Import | ImportFrom) -> bool:
    if isinstance(import_obj, Import):
        return import_obj.name.name == FLASK_MODULE_NAME

    assert isinstance(import_obj, ImportFrom)
    return FLASK_MODULE_NAME in (import_obj.module, import_obj.subimport.name.name)


def get_import_stmts_for(*objs: object) -> list[str]:
    import_visitor = ImportVisitor()

    for obj in objs:
        # Get which file the source code of the given object is in.
        obj_path = inspect.getfile(obj)  # type: ignore

        # Read the source file and fetch all imports.
        with open(obj_path, "r", encoding="utf-8") as obj_file:
            import_visitor.visit(ast.parse(obj_file.read()))

    # Exclude Flask imports.
    imports_no_flask = (import_obj for import_obj in import_visitor.imports if not is_flask_import(import_obj))

    # Convert the Import objects into import statement strings.
    import_stmts = list(sorted(str(import_obj) for import_obj in imports_no_flask))

    return import_stmts


def package_view_func_faasm(view_func: Callable[..., Any]) -> str:
    """Format the given `view_func` to be compatible with execution in Faasm."""

    # Get function name and source code for the given `view_func`.
    view_func_name = view_func.__name__
    view_func_source = get_view_func_source(view_func)

    # Get source code of Request class's definition.
    request_cls_source = inspect.getsource(Request)

    # Get all imports used in the view function's source and Request object.
    import_stmts = get_import_stmts_for(view_func, Request)
    imports = "\n".join(import_stmts)

    # Add the source code, function name, and Request class's source to the template file for uploading to Faasm.
    view_func_faasm = FAASM_FUNC_TEMPLATE.format(
        __imports=imports,
        __request_def=request_cls_source,
        __function=view_func_source,
        __function_name=view_func_name,
    )

    return view_func_faasm


def get_entry_view_func(fn_name: str) -> Callable[..., Any]:
    def entry_view_func(*args: Any, **kwargs: Any) -> Any:
        # Package args and kwargs as JSON-compatible objects.
        func_args = {"args": args, "kwargs": kwargs}

        # Package Request() object data as JSON-compatible objects.
        request_data = {
            "args": request.args.to_dict(),
            "form": request.form.to_dict(),
            "data_str": request.get_data(as_text=True),
            "is_json": request.is_json,
            "method": request.method,
        }

        # Invoke function on Faasm.
        input_data = {
            "func_args": func_args,
            "request_data": request_data,
        }
        input_data_json = json.dumps(input_data)
        output_json = invoke_py_func(fn_name, input_data=input_data_json)

        # Parse the output in JSON and return the result.
        output = json.loads(output_json)

        return output

    return entry_view_func


def process_flask_app(app: Flask) -> None:
    """
    Replace `view_func` in `app` with version that invokes Faasm for the function,
    and upload the function to Faasm.
    """

    for endpoint, view_func in view_funcs_iter(app):
        logger.info(f"Processing view function for {endpoint=}...")

        # Package the `view_func` into source executable by Faasm.
        view_func_faasm_source = package_view_func_faasm(view_func)
        logger.debug(f"Packaged view function source: \n{view_func_faasm_source}\n")

        # Upload the function to Faasm.
        view_func_name = upload_py_func(view_func_faasm_source)
        logger.debug(f"Uploading successful for {endpoint=}! Function name is now: {view_func_name!r}")

        # Get new entry view function that invokes the function in Faasm instead.
        # Call `update_wrapper()` to copy over attributes of `view_func` (equivalent to `@wraps()` decorator).
        entry_view_func = update_wrapper(get_entry_view_func(view_func_name), view_func)

        # Replace the function in `app.view_func` with the new entry view function.
        app.view_functions[endpoint] = entry_view_func  # type: ignore

        logger.info(f"Successfully processed view function for {endpoint=}!")
