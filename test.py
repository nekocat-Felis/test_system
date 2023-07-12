import datetime,glob,os,gc,sys,time,csv
from importlib import import_module
import setting

# どこから起動してもいいように、ソースファイルの場所に移動している。
os.chdir(f"{__file__[:-7]}")

# 評価対象をまとめて読み込む
method_dic = {}
error_array = []
dir_list = glob.glob("target/*/")
print(f"以下のフォルダを検出しました。\n{dir_list}\n")
for dir_name in dir_list:
    try:
        # 評価対象をモジュールとして読み込む。
        sys.path.append(f"{__file__[:-7]}target\\{dir_name[7:-1]}")
        #method_dic[dir_name[7:-1]] = import_module("main")
        method_dic[dir_name[7:-1]] = import_module(f"target.{dir_name[7:-1]}.main")
        sys.path.remove(f"{__file__[:-7]}target\\{dir_name[7:-1]}")
    except:
        if dir_name[7:-1] not in setting.escape_list:
            error_array.append(dir_name[7:-1])
target_list = list(method_dic.keys())
# 読み込みエラーが一度でも起きた場合に警告を表示
if len(error_array) > 0:
    print("Warning: 以下のフォルダからシステムが読み込めませんでした。")
    print(error_array)
    print('フォルダ名やファイル名に "." が含まれていると、正常に読み込まれないことがあります。\n読み込む必要のないフォルダである場合は無視し、計測したい場合はフォルダ名を変更してください。\n')

def main() -> None:
    diff_dic = {} # 計測結果まとめの辞書
    res_dic = {} # 出力結果まとめの辞書
    writeLinesArray = [] # 出力するファイルの中身

    # モジュールをひとつづつ選んで計測していく
    for target_name in target_list:
        print(f"{target_name} 計測を開始します。")
        response = [] # 計測結果の配列
        ex_res = [] # 出力結果の配列

        # 計測
        for i in range(setting.max_count):
            print(str(i + 1) + "回目",end = " ",flush = True)
            # 処理時間と出力結果を受け取り配列に格納。何もない場合でも return_object には None (他言語における null 相当) が入る。
            diff,return_object = func(target_name)
            response.append(str(diff.seconds + diff.microseconds / 1000000))        
            ex_res.append(return_object)
            # ここまで
            print("終了")
        print("計測が終了しました。\n")

        diff_dic[target_name] = response # 名前をキーに、結果を値に

        # 出力結果を表示に加える
        res_dic[target_name] = ex_res # 名前をキーに、結果を値に

    while True:
        print("データを出力する形式を選んでください。")
        format = input("csv形式の場合はc、tsv形式の場合はtと入力してください。：").lower()
        if format == "c":
            spread = ","
            break
        elif format == "t":
            spread = "\t"
            break
        else:
            print("\nc または t と入力してください。\n")

    # 計測結果配列の変形
    csvList = [] # 出力するcsv
    csvList.append(["num"] + target_list) # 項目名
    for i in range(setting.max_count):
        # ここから行の生成
        csvList.append([])
        csvList[-1].append(i+1) # 行番号
        # ここから値の入力
        for target_name in target_list:
            csvList[-1].append(diff_dic[target_name][i])

    # 出力結果の追加
    for target_name in target_list:
        if object_check(res_dic[target_name]): # 出力がいずれか一か所でも出ていた場合はテキスト化を行い、そうでなければ行わない。
            csvList.append([]) # 一行開ける
            csvList.append(["responce"]) # タイトル表示
            for i in range(setting.max_count):
                # ここから行の生成
                csvList.append([])
                csvList[-1].append(i+1) # 行番号
                # ここから値の入力
                for target_name in target_list:
                    csvList[-1].append(res_dic[target_name][i])
            break

    # 書き出し
    now = datetime.datetime.now().strftime(r"%Y-%m-%d_%H:%M:%S")
    file_name = now.replace(":","-") + f"_diff.{format}sv" # ファイル名に組み込めないコロンを排除
    print(f"\n{format.upper()}SVファイルを出力しています...",end = " ",flush = True)

    with open(f"{__file__[:-7]}\\diff\\{file_name}",mode="w",newline="") as csv_file:
        writer = csv.writer(csv_file,delimiter=spread)
        writer.writerow([now.replace('-','/').replace('_',' ')] + [None] * (len(target_list) - 1) + [f"データの個数：{setting.max_count}"] ) # 最初の行にファイル出力のタイミングとデータの総数を記載
        writer.writerows(csvList)
    
    print("終了しました。\n")

def func(target_name: str) -> datetime.timedelta:
    # target_nameの内容に応じて処理が変わるようにしておく
    while True:
        try:
            if setting.gc:
                gc.disable()
            start = datetime.datetime.now()
            return_object = method_dic[target_name].test() # 出力または None
            end = datetime.datetime.now()
            gc.enable()
            diff = end - start # 処理時間
            break
        except Exception as e:
            gc.enable()
            print(e)
            continue
    return diff,return_object

# リストに None 以外が含まれていれば True 、なければ False を返す。
def object_check(array: list) -> bool:
    for i in array:
        if i is not None:
            return True
    return False

if __name__ == "__main__":
    main()
    input("Enterで終了します。")