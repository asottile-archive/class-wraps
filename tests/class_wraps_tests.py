import unittest
from functools import WRAPPER_ASSIGNMENTS
from class_wraps import class_wraps

def test_method_to_wrap(*args, **kwargs):
    """Doc string of test_method_to_wrap"""
    return args, kwargs

class wrapper_class:
    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.__func(*args, original_args=self.__args, original_kwargs=self.__kwargs, **kwargs)

class other_wrapper_class(wrapper_class): pass

class TestClassWraps(unittest.TestCase):

    def assert_wrapped_matches(self, wrapped, unwrapped):
        """Asserts that the wrapped object got its stuff copied correctly."""

        # repr should match
        self.assertEqual(repr(wrapped), repr(unwrapped))

        # Check each of the attributes on the wrapped object
        # Note: that the attributes will always be there by design
        # whereas the unwrapped object may not have them.
        for attr in WRAPPER_ASSIGNMENTS:
            self.assertIs(
                getattr(wrapped, attr),
                getattr(unwrapped, attr, None)
            )

    def test_class_wraps_wrapping_class_wrapping_method(self):
        """Tests that a class wrapper with class_wraps wrapping a method works as expected."""

        wrapped_class = class_wraps(wrapper_class)
        test_method_wrapped_by_class = wrapped_class(test_method_to_wrap)
        self.assert_wrapped_matches(test_method_wrapped_by_class, test_method_to_wrap)

    def test_class_wraps_wrapping_class_wrapping_class(self):
        """Tests one level deeper."""

        wrapped_class = class_wraps(wrapper_class)
        wrapped_other_class = class_wraps(other_wrapper_class)
        wrapped_method = wrapped_class(test_method_to_wrap)
        double_wrapped_method = wrapped_other_class(wrapped_method)
        self.assert_wrapped_matches(double_wrapped_method, test_method_to_wrap)

    def test_arguments_passed_through_constructor(self):
        """Tests that arguments pasesed to constructor are correctly passed through decorator."""

        args_in = ('args_0', 'args_1')
        kwargs_in = {'kwargs_0': 'kwarg_value_0', 'kwarg_1': 'kwarg_value_1'}

        wrapped_class = class_wraps(wrapper_class)
        wrapped_method = wrapped_class(test_method_to_wrap, *args_in, **kwargs_in)

        args_out, kwargs_out = wrapped_method()
        original_args = kwargs_out['original_args']
        original_kwargs = kwargs_out['original_kwargs']

        self.assertEqual(original_args, args_in)
        self.assertEqual(original_kwargs, kwargs_in)

    def test_arguments_passed_through_call(self):
        """Tests that arguments passed to the call are correctly passed through decorator."""

        args_in = ('args_0', 'args_1')
        kwargs_in = {'kwargs_0': 'kwarg_value_0', 'kwarg_1': 'kwarg_value_1'}

        wrapped_class = class_wraps(wrapper_class)
        wrapped_method = wrapped_class(test_method_to_wrap)

        args_out, kwargs_out = wrapped_method(*args_in, **kwargs_in)
        kwargs_out.pop('original_args')
        kwargs_out.pop('original_kwargs')

        self.assertEqual(args_out, args_in)
        self.assertEqual(kwargs_out, kwargs_in)

if __name__ == '__main__':
    unittest.main()
