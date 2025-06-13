# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 14:04:10 2025

@author: Admin
"""
import pandas as pd

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    
human = pd.read_csv("data/human_title_abstract_50.csv")
llm = pd.read_csv("data/llm_title_abstract_50.csv")

human.columns = ['human_covidence_no', 'title', 'human_human_participants', 'human_involves_persuasion', 'human_persuasion_is_ai', 'human_is_theoretical', 'human_is_marketing', 'human_final_decision']

cm = confusion_matrix(human['human_final_decision'], llm['llm_final_decision'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for the final inclusion decision")
plt.show()

cm_hp = confusion_matrix(human['human_human_participants'], llm['llm_human_participants'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_hp)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for human participants' presence in the study")
plt.show()

cm_ip = confusion_matrix(human['human_involves_persuasion'], llm['llm_involves_persuasion'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_ip)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for persuasion presence in the study")
plt.show()

cm_aip = confusion_matrix(human['human_persuasion_is_ai'], llm['llm_persuasion_is_ai'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_aip)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for AI persuasion detection")
plt.show()

cm_th = confusion_matrix(human['human_is_theoretical'], llm['llm_is_theoretical'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_th)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for the theoretical articles detection")
plt.show()

cm_mar = confusion_matrix(human['human_is_marketing'], llm['llm_is_marketing'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_mar)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for the marketing articles detection")
plt.show()