from mage_ai.data_preparation.models.constants import DATAFRAME_ANALYSIS_MAX_COLUMNS
from mage_ai.shared.parsers import convert_matrix_to_dataframe


df_1 = convert_matrix_to_dataframe(df_1)
columns = ['mode value', 'frequency', '% of values']
column_index = []
rows = []
for col in df_1.columns[:DATAFRAME_ANALYSIS_MAX_COLUMNS]:
    value_counts = df_1[col].value_counts()
    if len(value_counts.index) == 0:
        continue
    column_value = value_counts.index[0]
    value = value_counts[column_value]
    number_of_rows = df_1[col].count()
    column_index.append(col)
    rows.append([
        column_value,
        f'{round(100 * value / number_of_rows, 2)}%',
        value,
      ])
