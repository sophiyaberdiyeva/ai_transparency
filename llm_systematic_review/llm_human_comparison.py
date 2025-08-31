# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 14:04:10 2025

@author: Admin
"""
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    
human = pd.read_excel("data/subset_50_title_abstract_screened_caro.xlsm")
llm = pd.read_csv("data/llm_title_abstract_50.csv")

#human.columns = ['human_covidence_no', 'title', 'human_human_participants', 'human_involves_persuasion', 'human_persuasion_is_ai', 'human_is_theoretical', 'human_is_marketing', 'human_final_decision']

for col in llm.columns:
    if '.decision' in col:
        llm[col] = llm[col].map({'Yes': 1, 'No': 0})

llm['final_decision'] = llm['final_decision'].map({'Include': 1, 'Exclude': 0})


llm.columns = ['covidence_number',
               'llm_final_decision',
               'llm_ic_1_population.reasoning',
               'llm_ic_1_population.decision',
               'llm_ic_2_intervention.reasoning',
               'llm_ic_2_intervention.decision',
               'llm_ic_3_technology.reasoning',
               'llm_ic_3_technology.decision',
               'llm_ic_4_study_type.reasoning',
               'llm_ic_4_study_type.decision',
               'llm_ec_1_domain.reasoning',
               'llm_ec_1_domain.decision']

joint_df = pd.concat([human, llm], axis=1)
joint_df['human_llm_diff']= np.where(joint_df['Decision logical']!=joint_df['llm_final_decision'], 1, 0)

joint_df.to_csv('data/caro_llm_title_abstract_50_joint.csv', index = False)

cm = confusion_matrix(human['Decision logical'], llm['llm_final_decision'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for the final inclusion decision")
plt.savefig('conf_matrices/final_decision.png')
plt.show()

cm_hp = confusion_matrix(human['human_human_participants'], llm['llm_ic_1_population.decision'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_hp)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for human participants' presence in the study")
plt.savefig('conf_matrices/human_participants.png')
plt.show()

cm_ip = confusion_matrix(human['human_involves_persuasion'], llm['llm_ic_2_intervention.decision'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_ip)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for persuasion presence in the study")
plt.savefig('conf_matrices/persuasion.png')
plt.show()

cm_aip = confusion_matrix(human['human_persuasion_is_ai'], llm['llm_ic_3_technology.decision'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_aip)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for AI persuasion detection")
plt.savefig('conf_matrices/ai_persuasion.png')
plt.show()

cm_emp = confusion_matrix(~(human['human_is_theoretical']), llm['llm_ic_4_study_type.decision'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_emp)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for empiciral studies detection")
plt.savefig('conf_matrices/empirical_studies.png')
plt.show()

cm_mar = confusion_matrix(human['human_is_marketing'], llm['llm_ec_1_domain.decision'])
fig, ax = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm_mar)
disp.plot(ax=ax)
ax.set_title("Confusion matrix for the marketing articles detection")
plt.savefig('conf_matrices/marketing_articles.png')
plt.show()