import numpy as np
import seaborn as sns
import pandas as pd
import numpy as np
import glob
import matplotlib as mpl
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from pathlib import Path

dataset = "uc50"


ac_list = []
f1_list = []
mcc_list = []
representation_name_list = []
for path in Path("../../result/").glob("drug_target_family_pred_class_based_accuracy_*_"+ dataset +".npy"):
    #print(path)
    representation_name_list.append(str(path).split("class_based_accuracy_")[1].split("_"+dataset+".npy")[0])
    acs = np.load(path)
    #print(acs)
    df = pd.DataFrame(acs[:,3])
    ac_list.append(df)
#print(ac_list)
df_ac = pd.concat(ac_list, axis=1)
df_ac.columns = representation_name_list

representation_name_list = []
for path in Path("../../result/").glob("drug_target_family_pred_class_based_f1_*_"+dataset+".npy"):
    #print(path)
    representation_name_list.append(str(path).split("class_based_f1_")[1].split("_"+dataset+".npy")[0])
    f1s = np.load(path)
    df = pd.DataFrame(f1s[:,3])
    f1_list.append(df)

df_f1 = pd.concat(f1_list, axis=1)
df_f1.columns = representation_name_list

representation_name_list = []
for path in Path("../../result/").glob("drug_target_family_pred_class_based_mcc_*_"+dataset+".npy"):
    #print(path)
    representation_name_list.append(str(path).split("class_based_mcc_")[1].split("_"+dataset+".npy")[0])
    mccs = np.load(path)
    df = pd.DataFrame(mccs[:,3])
    mcc_list.append(df)

df_mcc = pd.concat(mcc_list, axis=1)
df_mcc.columns = representation_name_list
df_mcc = df_mcc.reindex(df_mcc.mean().sort_values().index, axis=1)
df_f1 = df_f1.reindex(columns=df_mcc.columns)
df_ac = df_ac.reindex(columns=df_mcc.columns)

df_ac['metric'] = 'accuracy'
df_f1['metric'] = 'f1-score'
df_mcc['metric'] = 'mcc'

all_data = pd.concat([df_ac, df_f1, df_mcc])
#all_data = all_data.reindex(columns=df_mcc.columns)

cols = all_data.columns
cols = cols[:-1]
#print(cols)
all_data = pd.melt(all_data, id_vars=['metric'], value_vars=cols)

group_color_dict = {'K-SEP':'green','BERT-PFAM^':'red', 'UNIREP':'red', 'T5':'red', 'BERT-BFD':'red',\
                     'SEQVEC':'red', 'ALBERT':'red', 'PFAM^':'green', 'ESMB1':'red', \
                     'XLNET':'red', 'AAC':'green', 'APAAC':'green', 'PROTVEC':'blue', 'MUT2VEC':'blue',\
                    'LEARNED-VEC':'blue', 'CPC-PROT':'blue', 'BLAST':'blue', 'TCGA-EMBEDDING':'blue', 'GENE2VEC^':'blue', 'MUT2VEC^':'blue', 'HMMER':'blue'}


def set_colors_and_marks_for_representation_groups(ax):
    for label in ax.get_yticklabels():
        label.set_color(group_color_dict[label.get_text()])
        if label.get_text() == 'PFAM' or label.get_text() == 'BERT-PFAM' :
            signed_text = label.get_text() + "*"
            label.set_text(signed_text)
    ax.set_yticklabels(ax.get_yticklabels(), fontweight='bold')

sns.set(rc={'figure.figsize':(14,20)})
sns.set_theme(style="whitegrid", color_codes=True)

ax = sns.boxplot(data=all_data, x=all_data['value'], y=all_data['variable'], hue=all_data['metric'], whis=np.inf,  orient="h")
#ax = sns.swarmplot(data=all_data, x=all_data['value'], y=all_data['variable'], orient="h",color=".1")

ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))

ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.grid(b=True, which='major', color='gainsboro', linewidth=1.0)
ax.grid(b=True, which='minor', color='whitesmoke', linewidth=0.5)
ax.set_xlim(0, 1)
yticks = ax.get_yticks()
for ytick in yticks:
    ax.hlines(ytick+0.5,-0.1,1,linestyles='dashed')

set_colors_and_marks_for_representation_groups(ax)
ax.get_figure().savefig('../../result/figures/perclass_Ion_channels_'+dataset+'.png')

