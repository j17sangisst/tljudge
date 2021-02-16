<!DOCTYPE html>
<html lang="ja" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>分析サンプル</title>
        <link rel="stylesheet" href="css.css">
    </head>
    <body>
        <div class="content">
            <!-- <form method="get" action="after.php"-->
        <P>検索内容(TwitterIDの@は不要です)
        <form method="POST" action="after.php">
        <input type="text" name="twid">
        <input type="submit" value="分析する"></form></p>
	<p>*TwitterIDやユーザー名、単語で検索ができます。</p>
        <p>*入力したユーザー名の直近100件までのタイムラインを分析します</p>
	<p>*最大100件のツイートを取得する為時間がかかる場合があります。</p>
        <P>分析結果が線の下に表示されます</p>
            <hr>
        </div>
    </body>
</html>
