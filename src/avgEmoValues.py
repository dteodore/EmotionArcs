import os, re, csv, json, sys, string
import numpy as np
import pandas as pd
from collections import defaultdict, Counter

import gzip

from tqdm import tqdm

import pickle as pkl
from argparse import ArgumentParser
import logging
from twTokenizer import twokenize
tqdm.pandas()

parser = ArgumentParser()
parser.add_argument('--dataPath', help='path to CSV data file with texts')
parser.add_argument('--lexPath', help='path to lexicon. CSV with columns "word" plus emotion columns')
parser.add_argument('--lexNames', nargs="*", type=str, help='Names of the lexicons/column names in the lexicon CSV')
parser.add_argument('--savePath', help='path to save folder')
parser.add_argument('--NA', help='Whether words not in lexicon get neutral scores: none or present')

def read_lexicon(path, LEXNAMES):
    df = pd.read_csv(path, quotechar="'")
    df = df[~df['word'].isna()]
    df = df[['word']+LEXNAMES]
    df['word'] = [x.lower() for x in df['word']]
    return df

def prep_dim_lexicon(df, dim):
    ldf = df[['word']+[dim]]
    ldf = ldf[~ldf[dim].isna()]
    ldf.drop_duplicates(subset=['word'], keep='first', inplace=True)
    ldf[dim] = [float(x) for x in ldf[dim]]
    ldf.rename({dim: 'val'}, axis='columns', inplace=True)
    ldf.set_index('word', inplace=True)
    return ldf

def get_alpha(token):
    return token.isalpha()


def get_vals(twt, lexdf, NA):
    twt = " ".join(twokenize.tokenizeRawTweetText(twt))
    tt = twt.lower().split(" ")

    at = []
    pw = []
    word_labels = []
    for w in tt:
        if w.isalpha(): # Words that are alphabetic
            at.append(w)
        if w in lexdf.index: # Words that are in lexicon
            pw.append(w)
            
            # Word is in lexicon - use score
            score = lexdf.loc[w]['val']
            word_labels.append((w, float(score)))
        else: # Word is not in lexicon     
            if NA == 'none': # use neutral score
                word_labels.append((w, 0))
            elif NA == 'present': # use NA
                word_labels.append((w, 'NA'))
    numTokens = len(at)
    numLexTokens = len(pw)

    sum_score = 0
    count = 0
    for (word, score) in word_labels:
        if score != 'NA':
            sum_score += score
            count += 1
    if count != 0:
        avgLexVal = sum_score/count
    else:
        avgLexVal = 'NA'
    
    return [numTokens, numLexTokens, avgLexVal]


def process_df(df, lexdf, NA):
    logging.info("Number of rows: " + str(len(df)))

    resrows = [get_vals(x, lexdf, NA) for x in df['text']]
    resrows = [x + y for x,y in zip(df.values.tolist(), resrows)]

    resdf = pd.DataFrame(resrows, columns=df.columns.tolist() + ['numTokens', 'numLexTokens', 'avgLexVal'])
    #resdf = resdf[resdf['numLexTokens']>=1]
    
    resdf['lexRatio'] = resdf['numLexTokens']/resdf['numTokens']
   
    return resdf

def main(dataPath, LEXICON, LEXNAMES, savePath, NA):

    os.makedirs(savePath, exist_ok=True)

    logfile = os.path.join(savePath, 'log.txt')

    logging.basicConfig(filename=logfile, format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
    print(dataPath)
    df = pd.read_csv(dataPath)

    for LEXNAME in LEXNAMES:

        lexdf = prep_dim_lexicon(LEXICON, LEXNAME)
        logging.info(LEXNAME + " lexicon length: " + str(len(lexdf)))
        resdf = process_df(df, lexdf, NA)
    
        resdf.to_csv(os.path.join(savePath, LEXNAME+'.csv'), index=False)

if __name__=='__main__':
    args = parser.parse_args()

    dataPath = args.dataPath
    lexPath = args.lexPath

    LEXNAMES = args.lexNames
    LEXICON = read_lexicon(lexPath, LEXNAMES)

    savePath = args.savePath

    NA = args.NA
    main(dataPath, LEXICON, LEXNAMES, savePath, NA)
