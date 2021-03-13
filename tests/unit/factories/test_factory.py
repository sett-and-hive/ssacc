"""Test factory code."""

from ssacc.factories.factory import Factory


def test_register_concrete_implementation():
    """Test register_concrete_implementation."""

    def a_concrete_implementation():
        """Empty function. We just want to insure it is injected."""

    injection_key = "deadbeef"
    Factory.register(injection_key, a_concrete_implementation)
    the_implementation = Factory.get(injection_key)
    assert the_implementation is a_concrete_implementation
