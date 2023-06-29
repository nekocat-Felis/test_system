# test_system
処理速度の検証に使えるシステム。  
標準ライブラリだけを使っているので、  
Pythonの動作環境ならライブラリのインストールは不要です。  
LinuxやMacで動くかは試していませんが、たぶん動きます。  

# test.py
システムの本体です。  
これをPythonで動かせばcsvの出力までやります。

# diffフォルダ
計測結果の出力されるフォルダです。

# targetフォルダ
計測対象を入れておくフォルダです。  
target/<何かしらの名前>/main.py  
が読み込まれ、その中の test() が実行、計測されます。  
escapeフォルダは避難用に作ったものです。いらなかったら消しても大丈夫です。

# 説明書フォルダ
そのまんま。動作には影響しません。  
中身も古いので見る必要はないと思います。

# .gitignore、.gitkeep、LICENSEについて
.gitignoreはgitによる追跡先を変えるもの、  
.gitkeepはフォルダ構造をgitに認識させるためのダミーファイル、  
LICENSEは利用許諾とかそういうのです。  
.gitなんちゃらはgitにこそ影響しますが、LICENSE ふくめ test_system 自体の動作には影響しません。  
git cloneした後にいじり倒したいとかでなければ消してもいいです。  
MITライセンスにしてますが、実はMITライセンスがどういうものかは把握してません。  
たぶん無料で好き放題できるんだろうなあ、くらいに思ってます。  
好きに使ってください。
