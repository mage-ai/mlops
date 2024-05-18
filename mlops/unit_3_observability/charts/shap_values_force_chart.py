import base64
import io
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from pandas import Series
from scipy.sparse._csr import csr_matrix
from xgboost import Booster

from mage_ai.shared.parsers import convert_matrix_to_dataframe


@render(render_type='jpeg')
def create_visualization(inputs: Tuple[Booster, csr_matrix, Series], *args, **kwargs):
    model, X, _ = inputs

    # Random sampling - for example, 10% of the data
    sample_indices = np.random.choice(X.shape[0], size=int(X.shape[0] * 0.1), replace=False)
    X_sampled = X[sample_indices]
    X_sampled = X[:1]

    X_sampled = convert_matrix_to_dataframe(X_sampled)

    # Now, use X_sampled instead of X for SHAP analysis
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sampled)

    # Calculate the mean absolute SHAP values for each feature
    shap_sum = np.abs(shap_values).mean(axis=0)

    X = convert_matrix_to_dataframe(X)

    importance_df = pd.DataFrame([X.columns.tolist(), shap_sum.tolist()]).T
    importance_df.columns = ['column_name', 'shap_importance']
    importance_df = importance_df.sort_values('shap_importance', ascending=False)

    # Get the names of the top 10 most important features
    top_n_features = importance_df['column_name'].head(10).tolist()

    # Reduce the original X to these top 10 features
    X_top_n = X[top_n_features]

    # If idx is not defined, assuming we're taking the first sample for demonstration
    idx = 0  # Or any specific index of interest

    # Generate the force plot for this specific instance and only for the top N features
    shap.force_plot(
        explainer.expected_value,
        shap_values[idx, :][np.newaxis, X.columns.get_indexer(top_n_features)],
        X_top_n.iloc[idx, :],
        matplotlib=True
    )

    string_bytes = io.BytesIO()
    plt.savefig(string_bytes, format='png')
    string_bytes.seek(0)
    image_str = base64.b64encode(string_bytes.read()).decode()

    plt.close()

    return image_str
