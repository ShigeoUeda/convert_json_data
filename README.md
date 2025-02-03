# convert_json_data

沖電気のグラフエディタで保存したJSONファイルをPython環境から編集するJSON形式への変更するプログラム。

## 環境構築
```sh
git clone https://github.com/ShigeoUeda/convert_json_data.git
cd convert_json_data
python -m venv venv
pip install -r equirements.txt
```

## JSONファイルの変換
```sh
# ファイルの変換
python json_converter.py SA.json
```
## デバッグ用グラフ表示（グラフエディタが動作することが前提）

```sh
# グラフエディタに表示する
python display_node.py analysis_result_0001.json グラフエディタのURL
```
