# tljudge
##judg1.py  
1.TwitterAPIを用い、入力されたIDをもとにタイムラインを最大100件取得。  
2.取得したタイムラインを単語ごとに分割する。  
3.分割された単語ごとに点数を付ける。  
4.1件ごとの平均点で評価を出す。  
5.評価をjsonファイルに保存する。  
  
##emotion.txt tf-idf.txt  
judg1.pyで点数をつけるのに使用。  
  
##before.php  
初期画面  
TwitterIDの入力を行う  

##after.php  
分析結果表示画面  
jsonファイルの内容を表示する  
上から取得件数と分類結果、マイナス評価が大きい単語で使用回数の多い単語、取得したタイムラインとその評価点数  

##css.css  
before.phpとafter.phpで使うcssファイル
