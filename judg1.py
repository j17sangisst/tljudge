# coding: utf-8
from pyknp import Juman
import sys
import codecs
import pandas as pd
import Levenshtein
import tweepy
import csv
import json
import collections as cl
import neologdn

tw_id = 'コロナ'
#コマンドライン引数を取得
for line in sys.argv:
    tw_id = line

#コメントの点数を格納（合計）
sum_list = []
#誹謗中傷ではないと判断された個数
pos_cnt = 0
#誹謗中傷であると判断された個数
neg_cnt = 0
#悪意の高い単語の基準値
slander = float(-0.95)

sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


#print(tw_id)
#tweetpyの処理
consumer_key="Ms2FQQ62QsUjYlXv5HOaTfp6V"
consumer_secret = "YOPBtrj49150OvH2w0maUNpPJ6f9hBelmawBPIiPHq5EYYAR6H"
access_key= "1288272352036286464-wqPh2Txh2816WpKyzj3kQYzQFU7ji0"
access_secret = "f9BZlUvu3cxWlLd32MMW4rZ399Z8yrfl8D5PDJqExuqZY"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
q = tw_id
count=100
i=0
tweet_list=[]
tweets = api.search(q=q, locale="ja", count=count,tweet_mode='extended')
for tweet in tweets:
    tweet_list.append(tweet.full_text)

#取得したコメントの単語を格納
word_count = {}
#出現頻度上位5単語の単語と回数を格納
rank_word_list = []
#誹謗中傷度の高い順にコメントと点数を格納
rank_score_list = []

com_list = []
#単語極性対応表のパス
filepath_emot = 'emotion.txt'

#感情極性表を辞書として登録する
pn_table = pd.read_csv(filepath_emot, engine='python', encoding='utf_8', sep=':', names=('word','reading','POS','PN'))


reading_list = list(pn_table['reading'])
word_list = list(pn_table['word'])
pos_list = list(pn_table['POS'])
pn_list = list(pn_table['PN'])
#単語を評価（感情極性表）を付ける際の辞書
pn_emot = dict(zip(word_list,pn_list))

#tf-idf辞書のパス
filepath_freq = "Backbiting.txt"
#print('path=' + filepath_freq)

#tf-idf辞書を辞書として登録する
pn_csv = pd.read_csv(filepath_freq, engine='python', encoding='utf_8', sep=':', names=('freq','tfidf'))

#単語出現頻度の単語を格納
freq_list = list(pn_csv['freq'])
#TF-IDFの値を格納
tfidf_list = list(pn_csv['tfidf'])
#単語の出現頻度を付加する辞書
pn_freq = dict(zip(freq_list,tfidf_list))

for comment in tweet_list:
        #分割した単語を格納
        list_com = []
        #分割した単語の代表表記を格納する
        list_repname = []
        #分割した単語の原文化したものを格納
        list_genbun = []
        #分割した単語の品詞を格納
        list_hinsi = []
        #分割した単語の点数を格納
        list_score = []

        
        comment = comment.encode('utf-8')
        #改行を全角スペースにする
        comment = comment.replace('\n','　')
        #投稿コメントを格納
        comment = comment.replace('@','＠')
        comment = comment.decode('utf-8')
        #print(comment)

        #jumanで文章を分割
        juman = Juman()
        result = juman.analysis(comment)

        #単語をlist_comに格納、品詞をlist_hinsiに格納
        for mrph in result.mrph_list():
            list_com.append(format(mrph.midasi))
            list_repname.append(format(mrph.repname))
            list_hinsi.append(format(mrph.hinsi))



        #辞書で判定しやすい単語を格納する
        for text in list_repname:
            if text:
                pos = text.find('/')
                list_genbun.append(text[:pos])


        #list_comの単語を表示
	    #for i in list_com:
    		#print(u"見出し:{0}".format(i))

        #list_comの単語を表示
        #for i in list_genbun:
    		#print(u"原文化:{0}".format(i))

        #for i in list_hinsi:
    		#print(format(i))

        #単語の判定
        for text in list_genbun:
            #感情極性辞書の単語と一致
            if text in pn_emot.keys():
                emot = pn_emot[text]
                #print(pn_emot[text])
                #抽出した単語が感情極性辞書の点数-0.95以下の場合、単語をカウントする。
                if emot <= slander:
                    word_count[text] = word_count.get(text, 0) + 1
                #tf-idf辞書の単語と一致したら感情極性＊tf-idfの計算を行う
                if text in pn_freq:
                    #tf-idfの値に＋１
                    freq = 1 + pn_freq[text]
                    #print(pn_freq[text])
                    list_score.append(emot * freq)
                #感情極性の点数のみを格納する
                else:
                    list_score.append(emot)

        #単語の各点数を合計する
        score_sum = sum(list_score) / len(list_score)
        #誹謗中傷度の判定
        if score_sum >= 0:
    	    pos_cnt = pos_cnt + 1
        else:
            neg_cnt = neg_cnt + 1

        comment = comment.encode('utf-8')
        #コメントと点数を格納
        com_list.append([comment,score_sum])

print(len(tweet_list))
print(pos_cnt)
print(neg_cnt)

#ツイート数、誹謗中傷、非誹謗中傷のカウント数を格納
return_list = cl.OrderedDict()

name_list = ["length","positive","negative"]
return_list[name_list[0]] = len(tweet_list)
return_list[name_list[1]] = pos_cnt
return_list[name_list[2]] = neg_cnt


d =[(v, k) for k, v in word_count.items()]
d.sort()
d.reverse()

#誹謗中傷度の高い順に並び変える
com_list = sorted(com_list, reverse=False, key=lambda x: x[1])

#頻出頻度上位5単語を格納
for count, word in d[:5]:
    rank_word_list.append([word,count])

#誹謗中傷度の高い順にコメントと点数を格納
for text, score in com_list:
    rank_score_list.append([text, score])

#それぞれのデータをjson形式で保存する
with open("/var/www/html/sample_score.json",'w') as outfile:
    json.dump(rank_score_list, outfile, indent=2)
with open("/var/www/html/sample_words.json","w") as outfile:
    json.dump(rank_word_list, outfile, indent=2)
with open("/var/www/html/sample_emot.json","w") as outfile:
    json.dump(return_list, outfile, indent=2)
