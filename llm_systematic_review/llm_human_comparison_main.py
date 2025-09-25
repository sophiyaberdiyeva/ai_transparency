# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 14:04:10 2025

@author: Admin
"""
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    
df = pd.read_csv("data/human_llm_title_abstract_second_version.csv")

cm = confusion_matrix(df['Sofiyas_decision'], df['llm_final_decision_bin'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for the final inclusion decision (second version)")
plt.savefig('conf_matrices/final_decision_second_ver.png')
plt.show()
