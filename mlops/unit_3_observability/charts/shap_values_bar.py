import base64
import io
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import shap
from pandas import Series
from scipy.sparse._csr import csr_matrix
from xgboost import Booster


@render(render_type='jpeg')
def create_visualization(inputs: Tuple[Booster, csr_matrix, Series], **kwargs):
    model, X, _ = inputs

    # Random sampling - for example, 10% of the data
    sample_indices = np.random.choice(X.shape[0], size=int(X.shape[0] * 0.1), replace=False)
    X_sampled = X[sample_indices]
    X_sampled = X[:1]

    # Now, use X_sampled instead of X for SHAP analysis
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sampled)
    shap.summary_plot(shap_values, X_sampled, plot_type='bar')

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()

    plt.close()

    return my_base64_jpgData
