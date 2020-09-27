from titlecase import titlecase


class CleanDF:
    @staticmethod
    def titlecase_columns(df, column_list):
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
    def drop_columns(df, column_list):
        for column_name in column_list:
            if column_name in df.columns:
                df.drop(column_name, axis=1, errors="ignore", inplace=True)
            else:
                print(f"Unexpected column name {column_name} found in drop_columns().")
                # TODO: convert to proper logging
        return df

    @staticmethod
    def reorder_columns(df, column_list):
        df = df[column_list]
        return df

    @staticmethod
    def rename_columns(df, original_list, renamed_list):
        for i in range(len(df.columns)):
            if i < len(original_list):
                if original_list[i] in df.columns:
                    print(f"Renaming {original_list[i]} as {renamed_list[i]}")
                    df.rename(columns={original_list[i]: renamed_list[i]}, inplace=True)
                else:
                    print(f"Unexpected column name {original_list[i]} found in rename_columns().")
                    # TODO: convert to proper logging
        return df

    @staticmethod
    def dropna_rows(df, column_list):
        for column_name in column_list:
            if column_name in df.columns:
                df = df.dropna(subset=[column_name])
            else:
                print(f"Unexpected column name {column_name} found in dropna_rows().")
                # TODO: convert to proper logging
        return df
