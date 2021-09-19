#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

columns_names = [
    "correct_sentence",
    "changed_sentence",
    "iterations",
    "positive",
]
# defining the dataframes that will be compared
first_temp = pd.read_csv("output_diff_comma08_all08.csv", sep="\t", names=columns_names)[['correct_sentence']]
second_temp = pd.read_csv("output_diff_comma09_all08.csv", sep="\t", names=columns_names)[['correct_sentence']]

# difference between both dataframes
diff = first_temp.merge(second_temp, how="outer", indicator=True).loc[
    lambda x: x["_merge"] == "left_only"
]
diff = diff.drop_duplicates()
diff
# %%
diff['correct_sentence'].iloc[201]
# %%
example = pd.read_csv("output_diff_comma08_addcrase06_all08.csv", sep="\t", names=columns_names)[['changed_sentence']]
# %%
example['changed_sentence'].iloc[100]
# %%
