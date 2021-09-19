#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 14:09:11 2020

@author: ernany
"""

import pandas as pd
first_temp = pd.read_excel('6k+_temp108beforedeploy_data.xlsx')
second_temp = pd.read_excel('6k+_temp109beforedeploy_data.xlsx')

#%%

first_temp_fail = first_temp[first_temp['FAIL'].notna()]['Analyzed text'].to_frame()
second_temp_fail = second_temp[second_temp['FAIL'].notna()]['Analyzed text'].to_frame()

diff = second_temp_fail.merge(first_temp_fail, how = 'outer', indicator=True).loc[lambda x : x['_merge']=='left_only']
diff = diff.drop_duplicates()

joined = ''
for para in diff['Analyzed text'].values:
    joined += para + '\n'
    
joined

#%%

#first_temp_fail = first_temp[first_temp['Misspelling'].notna()]['Analyzed text'].to_frame()
#second_temp_fail = second_temp[second_temp['Misspelling'].notna()]['Analyzed text'].to_frame()
#
#diff = second_temp_fail.merge(first_temp_fail, how = 'outer', indicator=True).loc[lambda x : x['_merge']=='left_only']
#diff = diff.drop_duplicates()
#
#joined = ''
#for para in diff['Analyzed text'].values:
#    joined += para + '\n'
#    
#joined


#%%

#file_df = pd.read_csv('frases_problem.txt', sep='\n', names=['sentence'])
#unique_df = file_df.drop_duplicates()
#
#joined = ''
#for para in unique_df['sentence'].values:
#    joined += para + '\n'
#    
#joined
