from titlecase import titlecase


class CleanDF:
    @staticmethod
    def titlecase_column(df, column_name):
        df[column_name] = df[column_name].map(lambda x: titlecase(x) if isinstance(x, str) else x)
        return df
