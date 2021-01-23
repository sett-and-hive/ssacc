"""
SSA County Code crosswalk application context

The application will:
get zip and fips from one file.
get fips and ssa from another file.
get zips and cities from another file.
map them together.

assumes you ran fetch script to populate the data folders.

TODO: refactor this into a pipeline runner for a
filter and pipes architecture that is more testable.
https://github.com/MicrosoftDocs/architecture-center/blob/master/docs/patterns/pipes-and-filters.md

"""

import sys

from ssacc.adapters import shell_controller


def setup_factory():
    # Factory.register(InjectionKeys.PERSIST_TOTAL_COUNT, persistence_gateway.get_total_count)
    pass


# Allow the script to be run standalone.
if __name__ == "__main__":
    setup_factory()
    shell_controller.shell(sys.argv)
