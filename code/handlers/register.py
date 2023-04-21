from typing import Callable

from core.data_structure import MsgInfo


class Register(object):
    def __init__(self, name="universal register"):
        self._name = name
        self._handle_dict = dict()

    def __len__(self):
        return len(self._handle_dict)

    def __contains__(self, key):
        return self.get(key) is not None

    def __repr__(self):
        repr_str = f"{self.name} [\n"
        repr_str += ",\n".join(
            [
                f"{name} : {handle_func.__name__}"
                for name, handle_func in self._handle_dict.items()
            ]
        )
        repr_str += "]\n"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def keys(self):
        return self._handle_dict.keys()

    def get(self, key, force=True) -> Callable[[MsgInfo], None]:
        """
        Get the module by key. If force is True, raise KeyError when key is not found.
        """
        if force and key not in self._handle_dict:
            raise KeyError(f"{key} is not found in {self.name}")
        return self._handle_dict.get(key, None)

    def _register_handle(self, handle_func, keys, force=False):
        assert isinstance(
            keys, (list, tuple)
        ), f"keys must be list or tuple, but got {type(keys)}"
        for key in keys:
            if key in self._handle_dict and not force:
                raise KeyError(f"{key} is already registered in {self.name}")
            self._handle_dict[key] = handle_func

    def register_handle(self, keys, force=False, handle_func=None):
        r"""
        Register a handle function.

        For example::

        ```python
        msg_handle_register = Register(name="message handle register")
        class A:
            pass
        msg_handle_register.register_handle(keys=["A", "B"], handle_func=A)

        @msg_handle_register.register_handle(keys=["C"])
        class C:
            pass
        ```
        """
        # directly call register function
        if handle_func is not None:
            self._register_handle(handle_func, keys=keys, force=force)
            return handle_func

        def _register_module_wrapper(cls):
            self._register_handle(cls, keys=keys, force=force)
            return cls

        return _register_module_wrapper


msg_handle_register = Register(name="message handle register")
