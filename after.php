<?php
$twid = $_POST['twid'];

function escape1($str)
{
    return htmlspecialchars($str,ENT_QUOTES,'UTF-8');
}
?>
<?php
    $command = "sudo python /home/ubuntu/judg1.py ".$twid." 2> error.log";
    exec($command);

    $count="http://18.237.37.220/sample_emot.json";
    #取得件数のjsonファイルがある場所のurl
    $cjson=file_get_contents($count);
    #jsonファイルの取得
    $cnts=json_decode($cjson,true);
    #jsonから元の形式に変換

    $word="http://18.237.37.220/sample_words.json";
    #単語のjsonファイルがある場所のurl
    $wjson=file_get_contents($word);
    #jsonファイルの取得
    $warr=json_decode($wjson);
    #jsonから元の形式に変換

    $list="http://18.237.37.220/sample_score.json";
    #ツイートのjsonファイルがある場所のurl
    $ljson=file_get_contents($list);
    #jsonファイルの取得
    $larr=json_decode($ljson,true);
    #jsonから元の形式に変換
?>
<!DOCTYPE html>
<html lang="ja" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>分析サンプル</title>
        <link rel="stylesheet" href="css.css">
    </head>
    <body>
        <div class="content">
        <p>入力内容:<?=escape1($twid) ?><input type="button" value="戻る" onclick="history.back();"></p>
	<p>*入力した内容の直近100件までのツイートを分析します</p>
        <p>分析結果</p>
            <hr>
            <?php
            echo "<p>取得ツイート：".$cnts[length]."件</p>";
            echo "<p>誹謗中傷に当たる可能性の高いツイート数：".$cnts[negative]."件</p>";
            echo "<p>誹謗中傷に当たる可能性の低いツイート数：".$cnts[positive]."件</p>";
            ?>
            <p>悪意の高い単語</p>
        <?php
        $rank=1;
        foreach ($warr as $data) {
            if($data[1] >= 3){
                $wrnk= $rank++."位".":\"".$data[0]."\"　使用回数：<span>".$data[1]."</span>回";
            }else{
                $wrnk= $rank++."位".":\"".$data[0]."\"　使用回数：".$data[1]."回";#['word']
            }
            if($rank % 3 == 2){
                $wrnk= "<p>".$wrnk;
            }
            if($rank % 3 == 1){
                $wrnk= $wrnk."\n"."</P>".PHP_EOL;
            }
            else{
                $wrnk= $wrnk."　　".PHP_EOL;
            }
            echo $wrnk;
        }
        echo "</p>";
        ?>
            <!--ネガティブ度の高いツイートと点数
            閾値よりネガティブな単語は色を付ける  無理
            表形式で表示する　　|内容|点数|-->
            <div class="table">
            <table border="1">
                <tr>
                    <th>ツイート内容</th>
                    <th>点数</th>
                </tr>
                <?php
                    foreach ($larr as $key) {
                        if($key[1] < -10){
                            echo "<tr><td>" . $key[0] . "</td><td><span>" . $key[1] . "</span></td></tr>";
                        }else{
                            echo "<tr><td>" . $key[0] . "</td><td>" . $key[1] . "</td></tr>";
                        }
                    }
                 ?>
            </table>
            <input type="button" value="戻る" onclick="history.back();">
            </div>
        </div>
    </body>
</html>
