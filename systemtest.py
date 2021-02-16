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


# In[78]:


# -*- coding: utf-8 -*-
  
from pyknp import Juman                   # 形態素解析器JUMAN++
  
import math
import csv
import pandas as pd
import tweepy
import re
import neologdn

#コメントの点数を格納（合計）
list_sum = []
#誹謗中傷ではないと判断された個数
pos_cnt = 0
#誹謗中傷であると判断された個数
neg_cnt = 0
#CSVで保存する
csv_list = []

#TwitterAPI
consumer_key="Ms2FQQ62QsUjYlXv5HOaTfp6V"
consumer_secret = "YOPBtrj49150OvH2w0maUNpPJ6f9hBelmawBPIiPHq5EYYAR6H"
access_key= "1288272352036286464-wqPh2Txh2816WpKyzj3kQYzQFU7ji0"
access_secret = "f9BZlUvu3cxWlLd32MMW4rZ399Z8yrfl8D5PDJqExuqZY"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
#TwitterIDまたはキーワードを入力
q = "コロナ"
count=100
text =[]

#誹謗中傷文
#text=['不愉快です', '存在がいらいらした', '可哀想', 'しつこい', '死ね', 'ブス', '化粧濃すぎ', 'デブ', '裏切り者', 'お前もか', '何が当選や', '糞その100万円を俺にくれんやったら殺すからなガチで', 'お前の住所特定して殺しに行くからな覚えとけよ', 'なにしてんねん失望したわ', '他のメンバーに失礼じゃないの', 'お前が頑張らんかい', 'お前のせいで負けたんやで', '戦犯やんけお前', '大戦犯で草', '調査打ち切り', '誰一人助ける気無いのか', 'しまいにどつくぞ', 'なめるな', '終わりにしよう', '別れてください', '投稿消してください', '求めすぎ', '大嫌いです', '嘘', '名誉毀損', '柄が悪い', 'やめるなら今', '嘘つき', 'アンチ', 'キモイ', '消えろ', '間違い', '糞', 'センス無い', '邪魔', 'いらない', 'うざい', 'レッテル貼り', '誰かを傷つけて幸せなのか', 'お前の息子は便所掃除', '見苦しい', '人を傷つけて楽しい', '怠けてる', '仮病', '死んでもらっていい', '被害者面', 'お前病気だろ', '病院行ってこい', '精神科行ってこい', 'お前の心が歪んでるからだ', '転売', 'ダブスタ野郎', '誰に頼っても無駄', '責任逃れするな', 'マジで黙れ', '原因にしがみついといてつらいつらい言ってて間抜けなの', 'あいつは犯罪を犯してる', '二次元ゲームのヲタクズ', 'クズ', 'ゴミ', '無知蒙昧', '現代社会の最底辺', '肥溜めの底に沈殿した糞', '社会の隅で死なない程度にかろうじて生きることしかできない塵芥', '不正乗車確定', '回収していただきました', '出来の悪いギャグみたい', '品性の欠片も見当たらない', '犯罪者予備軍ども', 'このクソ豚', 'しね雑魚', '言われてんぞかまってちゃん', '身勝手じゃなくて見苦しいよ', 'こいつみたいなやつが社会を腐らせる', 'さっさといなくなれ', 'ぼったくり仕事', '他人にやらせて礼も言わないモラルの低さ', '温暖化対策を利権とする大人たちに操られている', '無知のなせる技', 'こんなもん', '現場を知らない自称専門家', '出番なし', 'まだ張り付きつ続けるの', '使えない', '身の程知らず', 'スートカー野郎', '顔真っ赤で泣いてんのかあ', 'ふざけてんのか', '俺のこと忘れてない', 'やり方が幼稚', '信用に値しない', 'お前がいなくても世界は変わらない', '死んでおめでとう', '勝った気でいるのか', '初対面で説教垂れんな']

#非誹謗中傷文
text=['ありがとう', '尊敬します', 'お気持ちは嬉しいです', '今更気にしない', '大丈夫です', '見るたび心が痛みます', '限度があると思います', 'いきがい', '明日も生きていける', '感謝します', 'ええんやで', 'うまい', 'よし', 'テスト', '憂鬱', 'あけましておめでとう', 'かわいい', 'あはは', 'アップルパイ', '真銀斬は全てを解決する', 'すばらしい', 'さよなら', 'うまくいった', '間違ってない', 'ポジティブシンキング', '綺麗', 'すごい', '誹謗中傷への最高の返答は、黙って仕事に精を出すことである', '何気ない言葉でも急所に刺さってしまうことがある', '心ない言葉は悪でしかない', 'いいね', 'いろんな性格の人がいるから合う合わないは仕方ない', '毎日関わる人かもしれないけどその人は自分の人生の全てではない', '誰かにとっては大切な人', 'この世から誹謗中傷が消えますように', 'やってることやばいの自覚してないのかないつか後悔するよ', 'そんな雑魚1人の言葉で簡単にうごくんじゃねーよ', '誹謗中傷する人間は馬鹿か暇人であることの証明', '公式が認めたネタ', '普通にジョークグッズとして完成度高いの草', 'トレンド入りおめでとうございます', '待ってました', '有能', '絶対買います', 'さすがですね', 'めっちゃシビレました', '全部かっこよすぎる', 'あのブドウは酸っぱかったに違いない', 'さすがです', '紛らわしいな', 'こういう説明とかすっごい好き', '良いと思います', '見たの初めてだけどここまでするか', '同志よ', '最初から最後までかっこよすぎる', '不摂生してるといざって時に体に力が入らないぞ', 'やればできる', 'ハハッ、ド派手にやってやろうぜ！', '今を楽しめ', '退屈させてくれるなよ', 'へいへい、お前らもよく頑張りました、っと', '機嫌よさそうだな', '助太刀するぞ', '強っ', 'そろそろ休憩の時間だよ', '休める時は、しっかり休養をとってね', '撃っていいのは、撃たれる覚悟のあるやつだけだ', 'どんなに厳しい局面でも、基本を忘れなければ助かることもある', '同じ穴の狢', '誹謗中傷で得をする人は誰もいない', '誰にも吐かずにいこうって思ってたし気にしてないけど気にしちゃう', '早く来てください。全てをとても分かりやすく１つ１つ丁寧に教えますから', '表現の自由があっても、やっていいこと悪いことの区別はあります', '現在の日本は医療従事者を土台として成り立っているものだと思っています', 'ほんまに恐ろしいわ', '誹謗中傷するような人がSNSに向いてない', '人を傷つける為に言葉を使うべきではない', '単なる悪口と他人を貶めたいだけの誹謗中傷と批判は違う', 'それではたから見れば嫉妬した負け犬の遠吠えでしかないのに', 'こういうバカにかぎってアホみたいにフォロワー数が多かったりする', 'どうにかならんもんかなぁ', '失礼なリプやめてくれ、オブラートに包まない毒舌やめてくれ、そこから始まってる話です', '自分の非を認めるのも大事ですよ', '名誉毀損や侮辱罪よりもっと重い罪でいいと思うのですが', 'こういうのまじありえない。自分の大切な人がなくなったらこんなこと言えるのか', 'こういうコメント貰ってる側にもなれよ。きっと耐えられなくなる', '誹謗中傷で亡くなったんじゃないとか関係なくて、誹謗中傷も今回の一件も人が一人亡くなっている事に目を向けて欲しい', 'ここまで袋叩きされてるとさすがに気の毒で同情するわ', '誹謗中傷のせいで亡くなってしまってもその方に誹謗中傷をし続ける人って何を考えているんだろ', 'そうじゃなくてもありえない話だけどただの犯罪者だよ何もかっこよくない', 'ネットって怖いね。遠くからでも人を死に追いやる凶器になる', 'この子は他にもこんなのしてるのかな', 'どんな環境で育ったのかなぁ', '人はお互いに弱いから補いあうことも理解しあうこともできる', '他の人も言ってるから良いだろうという気持ちで書いてはいけません', 'どんだけ私を下げても、自分は1ミリも上がらないことに、いつか気づくと思うよ', 'そもそも味方にキレたり喧嘩したりしても勝てる訳じゃない', '喧嘩は同じレベルでしか起こらない', 'みなさん自身が思っているよりも心はダメージを受けています', '普通の会話でも解釈違いで傷付いたり傷付けたりもあってしまう世の中なのに']

#tweets = api.search(q=q, locale="ja", count=count,tweet_mode='extended')
#for tweet in tweets:
    #text.append(tweet.full_text)

# utf-8 のCSVファイル
with open('notslander.txt', 'r') as csvfile:
  csv_reader = csv.reader(csvfile, delimiter=',')
  #for row in csv_reader:
    #print(row)
    #print(','.join(row))
    #text.append(row)

#取得したコメントの単語を格納
word_count = {}
#出現頻度上位5単語の単語と回数を格納
rank_word_list = []
#誹謗中傷度の高い順にコメントと点数を格納
rank_score_list = []

#単語極性対応表のパス
filepath_emot = 'emotion.txt'
#print('path =' + filepath_emot)


pn_table = pd.read_csv(filepath_emot, engine='python', encoding='utf_8', sep=':', names=('word','reading','POS','PN'))


reading_list = list(pn_table['reading'])
word_list = list(pn_table['word'])
pos_list = list(pn_table['POS'])
pn_list = list(pn_table['PN'])
#単語を評価（感情極性表）を付ける際の辞書
pn_emot = dict(zip(word_list,pn_list))
        
filepath_freq = "tf-idf.txt"
#print('path=' + filepath_freq)

pn_csv = pd.read_csv(filepath_freq, engine='python', encoding='utf_8', sep=':', names=('freq','tfidf'))

#単語出現頻度の単語を格納
freq_list = list(pn_csv['freq'])
#TF-IDFの値を格納
tfidf_list = list(pn_csv['tfidf'])
#単語の出現頻度を付加する辞書
pn_freq = dict(zip(freq_list,tfidf_list))

for comment in text:
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

  #txt = str(comment)
  #normalized_text = neologdn.normalize(txt)
  #comment = re.sub(r'[!-/:-@[-`{-~]', r' ', normalized_text)

  #comment = comment.encode('shift_jis')
  #@を全角にする
  #comment = comment.replace('@','＠')
  #改行を全角スペースにする
  #comment = comment.replace('\n','　')
  #comment = comment.replace('.','・')
  #投稿コメントを格納（現状は一文のみ
  #comment = comment.decode('utf-8')
  print(comment)

  txt = str(comment)
  
  #jumanで文章を分割
  juman = Juman()
  result = juman.analysis(txt)

  #単語をlist_comに格納、品詞をlist_hinsiに格納
  for mrph in result.mrph_list():
    list_com.append(format(mrph.midasi))
    list_repname.append(format(mrph.repname))
    list_hinsi.append(format(mrph.hinsi))
    #list_conv = [list_com, list_hinsi]

  #原文化
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
    print(text) 
    if text in pn_emot.keys():
      emot = pn_emot[text]
      #print(pn_emot[text])
      if text in pn_freq:
        freq = 1 + pn_freq[text]
        #print(pn_freq[text])
        list_score.append(emot * freq)
      else:
        list_score.append(emot)
      
  if sum(list_score) != 0: 
    score_sum = sum(list_score) / len(list_score)
    if score_sum >= 0.0:
      pos_cnt = pos_cnt + 1
    else:
      neg_cnt = neg_cnt + 1
    #comment = comment.encode('utf-8')
    print(score_sum)
    print(comment)	
    csv_list.append([comment,score_sum])

#print(pos_cnt)
#print(neg_cnt)

#son_score = json.dumps(csv_list)
#print('json_score:{}'.format(type(json_score)))

print(csv_list)
with open("検証.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f,lineterminator="\n")
    for key, value in csv_list:
      print(key)
      print(value)
      writer.writerow([key, value])
#ツイート数、誹謗中傷、非誹謗中傷のカウント数を格納
#return_list = cl.OrderedDict()

#name_list = ["length","positive","negative"]
#return_list[name_list[0]] = len(tweet_list)
#return_list[name_list[1]] = pos_cnt
#return_list[name_list[2]] = neg_cnt


#d =[(v, k) for k, v in word_count.items()]
#d.sort()
#d.reverse()

#誹謗中傷度の高い順に並び変える
#com_list = sorted(com_list, reverse=False, key=lambda x: x[1])

#頻出頻度上位5単語を格納
#for count, word in d[:5]:
    #rank_word_list.append([word,count])

#誹謗中傷度の高い順にコメントと点数を格納
#for text, score in com_list:
    #rank_score_list.append([text, score])

#それぞれのデータをjson形式で保存する
#with open("sample_score.json",'w') as outfile:
    #json.dump(rank_score_list, outfile, indent=2)
#with open("sample_words.json","w") as outfile:
    #json.dump(rank_word_list, outfile, indent=2)
#with open("sample_emot.json","w") as outfile:
    #json.dump(return_list, outfile, indent=2)

  


# In[41]:


# -*- coding: utf-8 -*-
  
from pyknp import Juman                   # 形態素解析器JUMAN++
  
import math
import csv
import pandas as pd
import tweepy
import re
import neologdn


#コメントの点数を格納（合計）
list_sum = []
#誹謗中傷ではないと判断された個数
pos_cnt = 0
#誹謗中傷であると判断された個数
neg_cnt = 0
#CSVで保存する
csv_list = []


# 文書集合のサンプル 
#text = ['ミニアルバム☆ 新谷良子withPBB「BANDScore」 絶賛発売chu♪ いつもと違い、「新谷良子withPBB」名義でのリリース！！ 全５曲で全曲新録！とてもとても濃い１枚になりましたっ。 PBBメンバーと作り上げた、新たなバンビポップ。 今回も、こだわり抜いて', '2012年11月24日 – 2012年11月24日(土)／12:30に行われる、新谷良子が出演するイベント詳細情報です。', '単語記事: 新谷良子. 編集 Tweet. 概要; 人物像; 主な ... その『ミルフィーユ・桜葉』という役は新谷良子の名前を広く認知させ、本人にも大切なものとなっている。 このころは演技も歌も素人丸出し（ ... え、普通のことしか書いてないって？ 「普通って言うなぁ！」', '2009年10月20日 – 普通におっぱいが大きい新谷良子さん』 ... 新谷良子オフィシャルblog 「はぴすま☆だいありー♪」 Powered by Ameba ... 結婚 356 名前： ノイズh(神奈川県)[sage] 投稿日：2009/10/19(月) 22:04:20.17 ID:7/ms/OLl できたっちゃ結婚か','2010年5月30日 – この用法の「壁ドン（壁にドン）」は声優の新谷良子の発言から広まったものであり、一般的には「壁際」＋「追い詰め」「押し付け」などと表現される場合が多い。 ドンッ. 「……黙れよ」. このように、命令口調で強引に迫られるのが女性のロマンの'] 


#csv_file = open("Tweetsdata.csv", "r", encoding="utf-8", errors="", newline="" )
#text = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
#text = csv.reader(csv_file)
#text = ['ミニアルバム☆ 新谷良子withPBB「BANDScore」 絶賛発売chu♪ いつもと違い、「新谷良子withPBB」名義でのリリース！！ 全５曲で全曲新録！とてもとても濃い１枚になりましたっ。 PBBメンバーと作り上げた、新たなバンビポップ。 今回も、こだわり抜いて', '2012年11月24日 – 2012年11月24日(土)／12:30に行われる、新谷良子が出演するイベント詳細情報です。', '単語記事: 新谷良子. 編集 Tweet. 概要; 人物像; 主な ... その『ミルフィーユ・桜葉』という役は新谷良子の名前を広く認知させ、本人にも大切なものとなっている。 このころは演技も歌も素人丸出し（ ... え、普通のことしか書いてないって？ 「普通って言うなぁ！」', '2009年10月20日 – 普通におっぱいが大きい新谷良子さん』 ... 新谷良子オフィシャルblog 「はぴすま☆だいありー♪」 Powered by Ameba ... 結婚 356 名前： ノイズh(神奈川県)[sage] 投稿日：2009/10/19(月) 22:04:20.17 ID:7/ms/OLl できたっちゃ結婚か','2010年5月30日 – この用法の「壁ドン（壁にドン）」は声優の新谷良子の発言から広まったものであり、一般的には「壁際」＋「追い詰め」「押し付け」などと表現される場合が多い。 ドンッ. 「……黙れよ」. このように、命令口調で強引に迫られるのが女性のロマンの'] 
#text =["京都大霊長類研究所（愛知県犬山市）のチンパンジー飼育施設の整備工事をめぐり、元所長の松沢哲郎・京大特別教授（７０）ら４人が公的研究費など約５億円を不正支出したとする問題。","会計検査院は１０日、新たに計約６億２千万円の不適な経理があったと指摘した。","設備工事をめぐる不正支出は総額１１億２８２３万円に上った。","大学側が公表した不正支出額の倍となっており、国立大学法人として学校運営のあり方が問われそうだ。"]



consumer_key="Ms2FQQ62QsUjYlXv5HOaTfp6V"
consumer_secret = "YOPBtrj49150OvH2w0maUNpPJ6f9hBelmawBPIiPHq5EYYAR6H"
access_key= "1288272352036286464-wqPh2Txh2816WpKyzj3kQYzQFU7ji0"
access_secret = "f9BZlUvu3cxWlLd32MMW4rZ399Z8yrfl8D5PDJqExuqZY"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
q = "雪"
count=100
text=[]
#tweets = api.search(q=q, locale="ja", count=count,tweet_mode='extended')
#for tweet in tweets:
   #text.append(tweet.full_text)
# utf-8 のCSVファイル
with open('slander.txt', 'r') as csvfile:
  csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in csv_reader:
    text.append(row)
    print(row)
    #print(','.join(row))
#with open("") as f:
  #text.append(f)


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

    #comment = txt.replace('^','＾')
    #comment = txt.replace('\n','　')
    #comment = txt.replace('@','＠')

    txt = str(txt)
    normalized_text = neologdn.normalize(txt)
    comment = re.sub(r'[!-/:-@[-`{-~]', r' ', normalized_text)

    print(comment)
    # MeCabを使うための初期化
    #tagger = MeCab.Tagger()
    #node = tagger.parseToNode(txt.encode('utf-8'))
    
    
    #jumanで文章を分割
    juman = Juman()
    node = juman.analysis(comment)
    
    fv = {}                     # 単語の出現回数を格納するためのディクショナリ
    words = 0                   # ある文書の単語の総出現回数
    
    for word in fv_df.keys():
        count_flag[word] = False
    for node in node.mrph_list():
        hinsi = node.hinsi
        if node:
          text = node.repname
          pos = text.find('/')
          node = text[:pos]
        #node = node.midasi
        surface = node
        print(node)
        print(hinsi)
        # while node.next:
        # node = node.next
        # surface = node.surface.decode('utf-8') # 形態素解析により得られた単語
  
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
        print(txt_num)#値確認用
        #rint(fv_df[key])#値確認用
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

    #print ('%s\ttf-idf:%lf' % (word, tf_idf[0]) )# 左から順に、単語、tf-idf値、tf値、idf値、その文書中の単語の出現回数、その単語の出現文書数(これは単語ごとに同じ値をとる))
    #\ttf:%lf\tidf:%lf\tterm_count:%d\tdocument_count:%d
    # tf_idf[1], tf_idf[2], tf_idf[3], tf_idf[4]


#CSV形式にタイムラインとtf-idfを保存する。
print(csv_list)
with open("sample_雪_代表表記.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f,lineterminator="\n")
    for key, value in csv_list:
       writer.writerow([key, value])

