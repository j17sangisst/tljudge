#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#juman++のダウンロードからインストールまで実行
get_ipython().system(' wget https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc3/jumanpp-2.0.0-rc3.tar.xz && sudo apt install cmake && tar xJvf jumanpp-2.0.0-rc3.tar.xz && cd jumanpp-2.0.0-rc3/ && mkdir bld && cd bld && cmake .. && sudo make install')


# In[ ]:


#pyknpのインストール
get_ipython().system('pip install pyknp')


# In[ ]:


#juman++のバージョン確認
get_ipython().system('jumanpp -v')


# In[ ]:


pip install neologdn


# In[1]:


# -*- coding: utf-8 -*-
  
from pyknp import Juman                   # 形態素解析器JUMAN++
  
import math
import csv
import pandas as pd
import tweepy
import re
import neologdn

#TwitterAPI
consumer_key="Ms2FQQ62QsUjYlXv5HOaTfp6V"
consumer_secret = "YOPBtrj49150OvH2w0maUNpPJ6f9hBelmawBPIiPHq5EYYAR6H"
access_key= "1288272352036286464-wqPh2Txh2816WpKyzj3kQYzQFU7ji0"
access_secret = "f9BZlUvu3cxWlLd32MMW4rZ399Z8yrfl8D5PDJqExuqZY"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
#TwitterIDまたはキーワードを入力
q = "モルカー"
count=100
text=[]
tweets = api.search(q=q, locale="ja", count=count,tweet_mode='extended')
for tweet in tweets:
    text.append(tweet.full_text)


#取得したテキスト数
txt_num = len(text)
print ('total texts:', txt_num)
print
  
fv_tf = []                      # ある文書中の単語の出現回数を格納するための配列
fv_df = {}                      # 単語の出現文書数を格納するためのディクショナリ
word_count = []                 # 単語の総出現回数を格納するための配列
  
fv_tf_idf = []                  # ある文書中の単語の特徴量を格納するための配列
  
count_flag = {}                 # fv_dfを計算する上で必要なフラグを格納するためのディクショナリ

csv_list = []                   #CSVで保存するデータを格納

hinsi_list = ['品詞','動詞','名詞','形容詞'] #抽出する単語を品詞、動詞、名詞、形容詞のみ

# 各文書の形態素解析と、単語の出現回数の計算
for txt_id, txt in enumerate(text):
    
    #分割した単語の品詞を格納
    list_hinsi = []

    #記号を全角に変換
    txt = str(txt)
    normalized_text = neologdn.normalize(txt)
    comment = re.sub(r'[!-/:-@[-`{-~]', r' ', normalized_text)

    #取得したコメントを表示
    print(comment)
    
    #jumanで文章を分割
    juman = Juman()
    node = juman.analysis(comment)
    
    fv = {}                     # 単語の出現回数を格納するためのディクショナリ
    words = 0                   # ある文書の単語の総出現回数
    
    for word in fv_df.keys():
        count_flag[word] = False
    for node in node.mrph_list():
        hinsi = node.hinsi
        #代表表記の漢字部分のみを抽出　例「漢字/かんじ」→「漢字」
        if node:
          text = node.repname
          pos = text.find('/')
          node = text[:pos]
        surface = node
        print(node)
        print(hinsi)
        words += 1

        if hinsi in hinsi_list:
          fv[surface] = fv.get(surface, 0) + 1 # fvにキー値がsurfaceの要素があれば、それに1を加え、なければ新しくキー値がsurfaceの要素をディクショナリに加え、値を1にする
  
          if surface in fv_df.keys(): # fv_dfにキー値がsurfaceの要素があれば
              if count_flag[surface] == False: # フラグを確認し，Falseであれば
                  fv_df[surface] += 1 # 出現文書数を1増やす
                  count_flag[surface] = True # フラグをTrueにする
          else:                 # fv_dfにキー値がsurfaceの要素がなければ
              fv_df[surface] = 1 # 新たにキー値がsurfaceの要素を作り，値として1を代入する
              count_flag[surface] = True # フラグをTrueにする

    fv_tf.append(fv)
    word_count.append(words)
  
# tf, idf, tf-idfなどの計算
for txt_id, fv in enumerate(fv_tf):
    tf = {}
    idf = {}
    tf_idf = {}
    for key in fv.keys():
        tf[key] = float(fv[key]) / word_count[txt_id] # tfの計算
        #print(txt_num)#値確認用
        #print(fv_df[key])#値確認用
        idf[key] = math.log(float(txt_num) / fv_df[key]) # idfの計算
        tf_idf[key] = (tf[key] * idf[key], tf[key], idf[key], fv[key], fv_df[key]) # tf-idfその他の計算
    tf_idf = sorted(tf_idf.items(), key=lambda x:x[1][0], reverse=True) # 得られたディクショナリtf-idfを、tf[key]*idf[key](tf-idf値)で降順ソート(処理後にはtf-idfはリストオブジェクトになっている)
    fv_tf_idf.append(tf_idf)
    
# 出力
print(fv_tf_idf)
for txt_id, fv in enumerate(fv_tf_idf):
    print ('This is the tf-idf of text', txt_id)
    print ('total words:', word_count[txt_id])
  
    for word, tf_idf in fv:
        print ('%s\ttf-idf:%lf\ttf:%lf\tidf:%lf' % (word, tf_idf[0], tf_idf[1], tf_idf[2]) )
        csv_list.append([word,tf_idf[0]])


#CSV形式にタイムラインとtf-idfを保存する。
print(csv_list)
with open("sample_モルカー_代表表記.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f,lineterminator="\n")
    for key, value in csv_list:
       writer.writerow([key, value])

