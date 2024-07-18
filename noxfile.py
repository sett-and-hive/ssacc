import nox

package = "ssacc"
python_versions = ["3.10", "3.9", "3.11", "3.12"]
nox.needs_version = ">= 2021.6.6"
# nox.options.sessions = (
#     "pre-commit",
#     "safety",
#     "mypy",
#     "tests",
#     "typeguard",
#     "xdoctest",
#     "docs-build",
# )

# @nox.session(python=python_versions[0])
# def .package(session):
#     """isolated packaging environment"""
#     session.env['COVERAGE_FILE'] = '.coverage..package'
#     session.install('.')
#     session.run('pytest', '-W', 'error')


@nox.session(python=python_versions[0])
def bandit(session):
    """Security check with bandit"""
    session.env["COVERAGE_FILE"] = ".coverage.bandit"
    session.install("bandit")
    session.run("bandit", "-r", "ssacc", "-c", ".bandit.yaml", "--verbose")


# @nox.session(python=python_versions[0])
# def safety(session) -> None:
#     """Scan dependencies for insecure packages."""
#     requirements = session.poetry.export_requirements()
#     session.install("safety")
#     session.run("safety", "check", "--full-report", f"--file={requirements}")


@nox.session(python=python_versions[0])
def coverage(session):
    """Calculate unit test code coverage"""
    session.install("-rrequirements.txt", "-rdev-requirements.txt")
    session.install(".")
    session.run("pytest", "--cov=./", "--cov-report=xml")


@nox.session(python=python_versions[0])
def format(session):
    """Format Python."""
    session.install("-rdev-requirements.txt")
    session.run("isort", "ssacc", "tests")
    session.run("black", "ssacc", "tests")


# @nox.session(python=python_versions[0])
# def fmt_check(session):
#     session.install('-r/home/tomas/develop/ssacc/dev-requirements.txt')
#     session.run('isort', '--check-only', 'ssacc', 'tests')
#     session.run('black', '--check', 'ssacc', 'tests')


@nox.session(python=python_versions[0])
def licenses(session):
    """Check licenses."""
    session.install("pip-licenses", "-rrequirements.txt")
    session.install(".")
    session.run("pip-licenses", "--from=mixed")


@nox.session(python=python_versions[0])
def mypy(session):
    """Check types."""
    session.install("-rrequirements.txt", "-rdev-requirements.txt")
    session.run("mypy", "ssacc")


@nox.session(python=python_versions[0])
def pep8(session):
    """Enforce pep8 with flake8."""
    session.install("-rdev-requirements.txt")
    session.run("flake8", "ssacc", "tests")


@nox.session(python=python_versions)
def tests(session):
    """Run tests."""
    session.env["COVERAGE_FILE"] = ".coverage.python3.10"
    session.install("-rrequirements.txt", "-rdev-requirements.txt")
    session.install(".")
    session.run("pytest", "-W", "error")
