from pathlib import Path

from ssacc.ssa_fips import SsaFips


def test_construction():
    assert SsaFips()


def test_read_csv():
    project_root = Path(__file__).parents[1]
    file_path = project_root.joinpath("data", "test1.csv")
    print(file_path)
    required_columns = {"ssacounty", "rating", "year", "runtime"}
    df = SsaFips.read_csv(file_path)
    assert len(df)
    for column_name in required_columns:
        assert column_name in df.columns


def test_read_csv_file_not_found():
    project_root = Path(__file__).parents[1]
    file_path = project_root.joinpath("data", "file_not_found.csv")
    print(file_path)
    df = SsaFips.read_csv(file_path)
    assert df is None


def test_read_csv_exception():
    project_root = Path(__file__).parents[1]
    file_path = project_root.joinpath("data", "test1.csv")
    print(file_path)
    df = SsaFips.read_csv(None)
    assert df is None
