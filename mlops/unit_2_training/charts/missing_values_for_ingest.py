number_of_rows = len(df_1.index)
columns_with_mising_values = []
percentage_of_missing_values = []
for col in df_1.columns:
    missing = df_1[col].isna().sum()
    if missing > 0:
        columns_with_mising_values.append(col)
        percentage_of_missing_values.append(100 * missing / number_of_rows)
