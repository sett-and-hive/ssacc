"""Test the timing wrapper."""

from ssacc.timing_wrapper import timing


def test_construction():
    """Trivial."""

    @timing
    def hello_world():
        """Hello world."""
        return print("Hello, world.")

    result = hello_world()
    print(result)
