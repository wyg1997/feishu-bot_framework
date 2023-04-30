class Register(object):
    def __init__(self, name="universal register"):
        self._name = name
        self._object_dict = dict()

    def __len__(self):
        return len(self._object_dict)

    def __contains__(self, key):
        return self.get(key, force=False) is not None

    def __repr__(self):
        repr_str = f"{self.name} [\n"
        repr_str += ",\n".join(
            [f"{name} : {obj.__name__}" for name, obj in self._object_dict.items()]
        )
        repr_str += "]\n"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def keys(self):
        return self._object_dict.keys()

    def get(self, key, force=True):
        """
        Get the module by key. If force is True, raise KeyError when key is not found.
        """
        if force and key not in self._object_dict:
            raise KeyError(f"{key} is not found in {self.name}")
        return self._object_dict.get(key, None)

    def _register_object(self, obj, key, force=False):
        assert isinstance(
            key, (list, tuple, str)
        ), f"keys must be list or tuple or str, but got {type(key)}"
        if isinstance(key, str):
            key = [key]

        for key in key:
            if key in self._object_dict and not force:
                raise KeyError(f"{key} is already registered in {self.name}")
            self._object_dict[key] = obj

    def register_object(self, key, force=False, obj=None):
        r"""
        Register a handle function.

        For example::

        ```python
        msg_handle_register = Register(name="message handle register")
        class A:
            pass
        msg_handle_register.register_object(keys=["A", "B"], obj=A)

        @msg_handle_register.register_object(keys=["C"])
        class C:
            pass
        ```
        """
        # directly call register function
        if obj is not None:
            self._register_object(obj, key=key, force=force)
            return obj

        def _register_object_wrapper(cls):
            self._register_object(cls, key=key, force=force)
            return cls

        return _register_object_wrapper


msg_handle_register = Register(name="message handle register")
bot_register = Register(name="bot register")
