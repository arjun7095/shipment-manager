import base64
import unittest

import app.exceptions


class StructureTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.MODULE = app.exceptions

    def test_class_exists_baseexception(self):
        classes = _get_class_names(self.MODULE)
        self.assertIn(
            base64.b64decode(b"Q29yZUV4Y2VwdGlvbg==").decode(),
            classes,
            msg=f"The class "
            f"`{base64.b64decode(b'Q29yZUV4Y2VwdGlvbg==').decode()}` "
            f"is not found, but it was marked as required.",
        )

    def test_class_exists_contentnotset(self):
        classes = _get_class_names(self.MODULE)
        self.assertIn(
            base64.b64decode(b"Q29udGVudE5vdFNldA==").decode(),
            classes,
            msg=f"The class "
            f"`{base64.b64decode(b'Q29udGVudE5vdFNldA==').decode()}` "
            f"is not found, but it was marked as required.",
        )

    def test_class_exists_invalidcontentdata(self):
        classes = _get_class_names(self.MODULE)
        self.assertIn(
            base64.b64decode(b"SW52YWxpZENvbnRlbnREYXRh").decode(),
            classes,
            msg=f"The class "
            f"`{base64.b64decode(b'SW52YWxpZENvbnRlbnREYXRh').decode()}` "
            f"is not found, but it was marked as required.",
        )

    def test_class_exists_invalididformat(self):
        classes = _get_class_names(self.MODULE)
        self.assertIn(
            base64.b64decode(b"SW52YWxpZElkRm9ybWF0").decode(),
            classes,
            msg=f"The class "
            f"`{base64.b64decode(b'SW52YWxpZElkRm9ybWF0').decode()}` "
            f"is not found, but it was marked as required.",
        )

    def test_class_exists_nodatafound(self):
        classes = _get_class_names(self.MODULE)
        self.assertIn(
            base64.b64decode(b"Tm9EYXRhRm91bmQ=").decode(),
            classes,
            msg=f"The class "
            f"`{base64.b64decode(b'Tm9EYXRhRm91bmQ=').decode()}` "
            f"is not found, but it was marked as required.",
        )


# === Internal functions, do not modify ===
import inspect

from types import ModuleType
from typing import List


def _get_function_names(module: ModuleType) -> List[str]:
    names = []
    functions = inspect.getmembers(module, lambda member: inspect.isfunction(member))
    for name, fn in functions:
        if fn.__module__ == module.__name__:
            names.append(name)
    return names


def _get_function_arg_names(module: ModuleType, fn_name: str) -> List[str]:
    arg_names = []
    functions = inspect.getmembers(module, lambda member: inspect.isfunction(member))
    for name, fn in functions:
        if fn.__module__ == module.__name__:
            if fn.__qualname__ == fn_name:
                args_spec = inspect.getfullargspec(fn)
                arg_names = args_spec.args
                if args_spec.varargs is not None:
                    arg_names.extend(args_spec.varargs)
                if args_spec.varkw is not None:
                    arg_names.extend(args_spec.varkw)
                arg_names.extend(args_spec.kwonlyargs)
                break
    return arg_names


def _get_class_names(module: ModuleType) -> List[str]:
    names = []
    classes = inspect.getmembers(module, lambda member: inspect.isclass(member))
    for name, cls in classes:
        if cls.__module__ == module.__name__:
            names.append(name)
    return names


def _get_class_function_names(module: ModuleType, cls_name: str) -> List[str]:
    fn_names = []
    classes = inspect.getmembers(module, lambda member: inspect.isclass(member))
    for cls_name_, cls in classes:
        if cls.__module__ == module.__name__:
            if cls_name_ == cls_name:
                functions = inspect.getmembers(
                    cls,
                    lambda member: inspect.ismethod(member)
                    or inspect.isfunction(member),
                )
                for fn_name, fn in functions:
                    fn_names.append(fn.__qualname__)
                break
    return fn_names


def _get_class_function_arg_names(
    module: ModuleType, cls_name: str, fn_name: str
) -> List[str]:
    arg_names = []
    classes = inspect.getmembers(module, lambda member: inspect.isclass(member))
    for cls_name_, cls in classes:
        if cls.__module__ == module.__name__:
            if cls_name_ == cls_name:
                functions = inspect.getmembers(
                    cls,
                    lambda member: inspect.ismethod(member)
                    or inspect.isfunction(member),
                )
                for fn_name_, fn in functions:
                    if fn.__qualname__ == fn_name:
                        args_spec = inspect.getfullargspec(fn)
                        arg_names = args_spec.args
                        if args_spec.varargs is not None:
                            arg_names.extend(args_spec.varargs)
                        if args_spec.varkw is not None:
                            arg_names.extend(args_spec.varkw)
                        arg_names.extend(args_spec.kwonlyargs)
                        break
                break
    return arg_names
