import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import Counter
from tqdm import tqdm
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import collections

def visual(input, output, out_dir,input_path,file,autophrase,multi_word,single_word,token_mapping):
    print("Creating Distribution graphs of the outputs")
    data_kk_single = pd.read_csv(input_path+single_word, sep="\t",header = None,names=['value', 'phrase'])
    data_kk_multi = pd.read_csv(input_path+multi_word, sep="\t",header = None,names=['value', 'phrase'])


    #single-word distribution
    plt.figure()
    plt.title('Quality Score Distribution of Single-Word Phrases')
    plt.hist(data_kk_single['value'], alpha=0.5, label='single', color='gray')
    plt.xlabel('Probability of Quality Word/Phrase')
    plt.ylabel('Frequency')
    plt.legend(loc = 'upper right')
    plt.savefig(input_path + 'single_quality_score'+'.png')
    plt.close()

    #multi-word distribution
    plt.figure()
    plt.title('Quality Score Distribution of Multi-Word Phrases')
    plt.hist(data_kk_multi['value'], alpha=0.5, label='multi', color='red')
    plt.xlabel('Probability of Quality Word/Phrase')
    plt.ylabel('Frequency')
    plt.legend(loc = 'upper right')
    plt.savefig(input_path + 'multi_quality_score' + '.png')
    plt.close()

    plt.figure()
    plt.title('Quality Score Distribution of Single-Word vs. Multi-Word Phrases')
    plt.hist(data_kk_single['value'], alpha = 0.5, label = 'single', color = 'gray')
    plt.hist(data_kk_multi['value'], alpha = 0.5, label = 'multi', color = 'red')
    plt.xlabel('Probability of Quality Word/Phrase')
    plt.ylabel('Frequency')
    plt.legend(loc = 'upper right')
    plt.savefig(input_path + 'comparison_quality_score' + '.png')
    plt.close()


    try:
        with open(input, 'r') as file:
            data = file.read().split('\n')
        ds = pd.read_csv('data/outputs/AutoPhrase_single-word.txt',sep='\t')


        #tf-idf top 20
        tfIdfVectorizer=TfidfVectorizer(stop_words='english')
        tfIdf = tfIdfVectorizer.fit_transform(data)
        cum = []
        for i in tqdm(range(tfIdf.shape[0])):
            df = pd.DataFrame(tfIdf[i].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
            df = df[df['TF-IDF']!=0].sort_values('TF-IDF', ascending=False)
            cum.append(df['TF-IDF'].to_dict())
        counter = collections.Counter()
        for d in cum:
            counter.update(d)
        res = pd.DataFrame({'Word':dict(counter).keys(),'Score':dict(counter).values()})
        res['Score'] = res['Score'].apply(lambda x: (x-min(res['Score']))/(max(res['Score'])-min(res['Score'])))
        res.sort_values('Score',ascending=False,inplace=True)
        res.to_csv(output+'tfidf.txt',index=False, header = None, sep='\t')

        # autophrase top 20
        row = ds.columns.values
        ds.columns = ['Score','Word']
        ds.loc[len(df)] = row
        ds['Score'] = ds['Score'].apply(lambda x:float(x))
        ds.sort_values('Score',inplace=True,ascending=False)
        res.index = res.Word
        ds.index = ds.Word
        ds.to_csv(output+'quality.txt',index=False, header = None, sep='\t')

        # multiplication top 20
        haha = {}
        for key in ds.Score.to_dict():
            try:
                value = (ds.Score.to_dict()[key] * res.Score.to_dict()[key])
                haha[key] = value
            except:
                pass
        lala = pd.DataFrame({'Word':haha.keys(),'Score':haha.values()})
        lala.sort_values('Score',ascending=False,inplace=True)
        lala.to_csv(output+'multiplication.txt',header = None, index=False, sep='\t')


        # 20 most frequent words
        with open(input, 'r') as input_file:
            input_text = input_file.read()

        word_lst = re.findall(r'[A-Za-z]+[0-9]?[+-]*', input_text)
        word_count = Counter(word_lst)

        single_top_20 = data_kk_single[:20]
        single_top_20['frequency'] = single_top_20.apply(lambda row: word_count[row['phrase']], axis = 1)

        plt.figure()
        plt.title('Quality vs. Frequency of Top 20 Single-Word Phrases')
        plt.xlabel('Quality Score')
        plt.ylabel('Frequency')

        for index, row in single_top_20.iterrows():
            plt.text(x = row['value'],
                    y = row['frequency'],
                    s = row['phrase'],
                    size = 8,
                    horizontalalignment = 'center')

        plt.scatter(x = single_top_20['value'],
                    y = single_top_20['frequency'],
                    c = single_top_20['frequency'],
                    s = single_top_20['value'],
                    linewidths = 2,
                    edgecolor = 'w',
                    alpha = 0.5)

        plt.savefig(input_path + 'top_20_value_frequency' + '.png')
        plt.close()

    except:
        print('Does not work!')

    print("Done!")
    print("Results are in the /data/outputs folder!")
    return
