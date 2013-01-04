from functools import WRAPPER_ASSIGNMENTS

def class_wraps(cls):
    """Update a wrapper class `cls` to look like the wrapped function."""

    class Wrapper(cls):
        """New wrapper that will extend the wrapper `cls` to make it look like `wrapped`

        Adapted from: http://stackoverflow.com/questions/6394511

        Args:
            wrapped - Original function or class that is being decorated.
            *args - Args to pass on.
            **kwargs - Kwargs to pass on.
        """

        def __init__(self, wrapped, *args, **kwargs):
            self.__wrapped = wrapped
            for attr in WRAPPER_ASSIGNMENTS:
                setattr(self, attr, getattr(wrapped, attr, None))

            # XXX: I'm not sure if this is right, but it works...
            cls.__init__(self, wrapped, *args, **kwargs)

        def __repr__(self):
            return repr(self.__wrapped)

    return Wrapper
