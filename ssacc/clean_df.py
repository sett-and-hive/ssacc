"""Data cleaning methods."""

from titlecase import titlecase

from ssacc.wrappers.timing_wrapper import timing


class CleanDF:
    """Utilities for cleaning data frames. Data engineering."""

    @staticmethod
    @timing
    def titlecase_columns(df, column_list):
        """Apply titlecase to some columns in a dataframe.

        TODO: Resolve some weaknesses in the titlecase library.
        """
        for column_name in column_list:
            if column_name in df.columns:
                df[column_name] = df[column_name].map(
                    lambda x: titlecase(x) if isinstance(x, str) else x
                )
            else:
                print(f"Unexpected column name {column_name} found in titlecase_columns().")
                # TODO: convert to proper logging
        return df

    @staticmethod
    @timing
    def drop_columns(df, column_list):
        """Drop a list of columns from a dataframe."""
        for column_name in column_list:
            if column_name in df.columns:
                df.drop(column_name, axis=1, errors="ignore", inplace=True)
            else:
                print(f"Unexpected column name {column_name} found in drop_columns().")
                # TODO: convert to proper logging
        return df

    @staticmethod
    @timing
    def reorder_columns(df, column_list):
        """Reorder the columns in a dataframe."""
        df = df[column_list]
        return df

    @staticmethod
    @timing
    def rename_columns(df, original_list, renamed_list):
        """Rename columns."""
        for i, _unused in enumerate(df.columns):
            if i < len(original_list):
                if original_list[i] in df.columns:
                    df.rename(columns={original_list[i]: renamed_list[i]}, inplace=True)
                else:
                    print(f"Unexpected column name {original_list[i]} found in rename_columns().")
                    # TODO: convert to proper logging
        return df

    @staticmethod
    @timing
    def dropna_rows(df, column_list):
        """Drop rows with now data in certain columns."""
        for column_name in column_list:
            if column_name in df.columns:
                df = df.dropna(subset=[column_name])
            else:
                print(f"Unexpected column name {column_name} found in dropna_rows().")
                # TODO: convert to proper logging
        return df
