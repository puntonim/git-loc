from contextlib import ContextDecorator

from git_loc.conf import settings


class override_settings(ContextDecorator):
    """
    Context manager and decorator to override a key in `conf.settings`.
    Only existing keys (in settings) can be overridden; non-existing keys are discarded.

    As a context manager:
        with override_settings(IS_TEST="xxx"):
            assert settings.IS_TEST == "xxx"

    As decorator, you can decorate a test function or method like:
        @override_settings(IS_TEST="xxx")
        def test_override_settings_decorator_happy_flow():
            assert settings.IS_TEST == "xxx"

    But you can NOT decorate a (test) class. To use it for the entire test class:
        class TestMyTest:
            def setup(self):
                self.override_settings = override_settings(IS_TEST=False)
                self.override_settings.__enter__()

            def teardown(self):
                self.override_settings.__exit__()
    """

    def __init__(self, do_allow_new_settings=False, **kwargs):
        self.kwargs = kwargs
        self.do_allow_new_settings = do_allow_new_settings

    def __enter__(self):
        for key, value in self.kwargs.items():
            # If not self.do_allow_new_settings then only update existing keys and
            #  discard non-existing keys.
            if not self.do_allow_new_settings and key not in settings:
                continue
            settings.set(key, value)

    def __exit__(self, *exc):
        # To reset settings: https://github.com/rochacbruno/dynaconf/issues/441
        settings.reload()
        settings.validators.validate()
