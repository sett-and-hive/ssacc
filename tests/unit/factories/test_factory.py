"""Test factory code."""

from ssacc.factories.factory import Factory


def test_register_concrete_implementation():
    def a_concrete_implementation():
        pass

    injection_key = "deadbeef"
    Factory.register(injection_key, a_concrete_implementation)
    the_implementation = Factory.get(injection_key)
    assert the_implementation == a_concrete_implementation
