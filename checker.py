#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import json
import csv
from tqdm import tqdm
import pandas as pd
import urllib.request


def raw_url(args):
    if type(args) == argparse.Namespace:
        raw_url = args.url
    if type(args) == dict:
        raw_url = args['url']
    return raw_url

def check(args, input_lines):

    all_info = []
    for line in tqdm(input_lines[:args.num_lines]):
        # setting up the query to the url address
        text_encoded = urllib.parse.quote(line)
        query = raw_url(args) + '/?text=' + text_encoded
        # making the request
        contents = urllib.request.urlopen(query).read()
        # converting the bytes object to json
        output_json = json.loads(contents)
        
        # this snippet is for replacing the matches into the original line
        matches = output_json['matches']; diff_line = line;
        for match in matches:
        	repls = match['replacements']
        	offset = match['offset']
        	length = match['length']
        	for i, repl in enumerate(repls):
        		separator = '|||'
        		if i == 0:
        			separator = '|||DIFF|||'
        		diff_line = line[:offset+length] + separator + repl['value'] + line[offset+length:]
        		length += len(separator+repl['value'])


        num_matches = len(output_json['matches'])
        status = bool(output_json['matches'])
        single_info = [line, diff_line, num_matches, status]
        all_info.append(single_info)
    
    return pd.DataFrame(all_info, columns=['sentence', 'diff_sentence', 'matches', 'positive'])

def main(args):
    
    assert os.path.exists(args.input_file), 'The input file path does not exist.'
    with open(args.input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    input_lines = [s.strip() for s in lines if s.strip()]
    
    # check the paragraphs
    output_dataframe = check(args, input_lines)
    output_dataframe.to_csv(args.output_file_all, index=False, header=False, sep='\t', quoting=csv.QUOTE_NONE)

    # output only the paragraphs which have been corrected
    mask_diff = output_dataframe['positive'] > 0
    diff = output_dataframe[mask_diff]
    diff.to_csv(args.output_file_diff, index=False, header=False, sep='\t', quoting=csv.QUOTE_NONE)
    
    print('positive rate: ' + str(sum(output_dataframe['positive'])) + '/' + str(len(output_dataframe['positive'])))

    return




#%%

if __name__ == '__main__':
    # read parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file',
                        help='Path to the input file.',
                        required=True)
    parser.add_argument('--output_file_all',
    					default='output_all.csv',
                        help='Path to the output file.')
    parser.add_argument('--output_file_diff',
    					default='output_diff.csv',
                        help='Path to the output file.')
    parser.add_argument('--url',
                        help='url where the check is done',
                        required=True)
    parser.add_argument('--num_lines',
                        help='number of lines to be checked',
                        type=int)
    args = parser.parse_args()
    main(args)
    
    
    
    
    
    