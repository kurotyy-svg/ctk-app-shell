# CTk App Shell

CustomTkinter 用の、サイドバー付きアプリテンプレートです。
ダーク基調(ライトにも切替可)で、コピーして中身を差し替えるだけで「それっぽいツール画面」になります。

- サイドバーのナビ(選択中はオレンジでハイライト)
- 画面は3つ: ダッシュボード / 作業 / 設定
- ライト/ダークの切替(アイコンも自動で切り替わる)
- テーマ対応のメッセージボックス(情報・警告・エラー・はい/いいえ)
- 色・フォント・アイコンは `theme.py` に集約

解説記事: (公開後にURLを入れる)

## 使い方

```
pip install -r requirements.txt
python main.py
```

## 各画面の使い方

| 画面 | できること |
|---|---|
| ダッシュボード | KPIカード・アクティビティ・使用状況の表示見本。数字は `views/dashboard.py` 冒頭の見本データ(`STATS` など)を書き換えると変わります |
| 作業 | 「参照」でフォルダを選び、「実行」を押すと確認ダイアログ → 「はい」で `run_job()` が動きます |
| 設定 | ダーク/ライト/システム切替、UIの大きさ、スイッチ(見本。保存はしていません) |
| サイドバー下部 | 「ライト/ダーク切替」でいつでもテーマを切り替えられます |

**作業画面の流れ(デモ)**
1. 「参照」: フォルダ選択ダイアログが開き、選んだフォルダのパスが「入力フォルダ」の欄に入ります(これだけで、フォルダの中身は読みません)
2. 「実行」: 確認ダイアログ(はい/いいえ)が出ます。フォルダ未選択なら警告が出ます
3. 「はい」: `views/work.py` の `run_job()` が別スレッドで動き、ログと進捗バーが進みます
4. 終わると完了ダイアログが出ます

**いまの `run_job()` はデモです。** 疑似的にログと進捗を出すだけで、ファイルの読み込みも出力もしません。
自分のツールにするときは、この関数の中身を差し替えます。

例: フォルダ内の .xlsx を1つずつ処理する場合

```python
from pathlib import Path


def run_job(folder, output_name, mode, log, progress):
    files = list(Path(folder).glob("*.xlsx"))
    if not files:
        raise ValueError("フォルダに .xlsx ファイルがありません。")
    log(f"{len(files)} 件のファイルを処理します")
    for i, f in enumerate(files, start=1):
        log(f"処理中: {f.name}")
        # ここに1ファイルぶんの処理を書く
        progress(i / len(files))
    log("完了")
```

## フォルダ構成

```
main.py              アプリ本体(画面の切替とサイドバー)
theme.py             色・フォント・アイコンの設定(見た目はここを編集)
components/          sidebar.py / card.py / dialog.py
views/               dashboard.py / work.py / settings.py (base.py が共通の土台)
assets/icons/        アイコンPNG(ライト用・ダーク用)
assets/app.ico       ウィンドウ左上・タスクバー用のアイコン(Windows)
assets/icons_src/    アイコンの元SVGとライセンス
tools/build_icons.py SVG から PNG を作り直すスクリプト(任意)
tools/record_demo.py GIF・動画の撮影用に、アプリを自動で操作するスクリプト(任意)
```

## 自分のアプリにする

**画面を増やす**
1. `views/` に `BaseView` を継承したクラスを作る(`views/work.py` を参考に)
2. `main.py` の `NAV_ITEMS` に `("キー", "表示名", "アイコン名")` を1行足す
3. `main.py` の `self.views` に同じキーで1行足す

**色を変える**
`theme.py` の `ACCENT` などを書き換えます。色は `(ライト用, ダーク用)` のタプルなので、
両方のモードで見た目を合わせてください。

**アイコンを足す**
1. [Lucide](https://lucide.dev/) などの SVG を `assets/icons_src/` に入れる
2. `pip install -r tools/requirements-dev.txt` のあと `python tools/build_icons.py`
   (cairosvg は Cairo ライブラリを使います。Windows では Cairo を別に用意しないと動かないことがあります。
   PNG は同梱済みなので、アイコンを足さないならこの手順は不要です)
3. `theme.icon("名前")` で使う(`size=` で表示サイズ、`variant="accent"` でオレンジ線)

アイコンPNGは表示サイズの4倍(96px)で書き出しています。
`CTkImage(size=(22, 22))` のように小さく表示しても、画面の拡大表示でボケにくくするためです。

**処理をつなぐ**
`views/work.py` の `run_job()` を自分の処理に差し替えます(上の「作業画面の流れ」を参照)。
別スレッドで動くので、時間のかかる処理でも画面は固まりません。
`run_job()` の中から画面の部品(CTkLabelなど)を直接さわらず、`log()` / `progress()` を使ってください。
エラーは `raise` すれば、エラーダイアログが出ます。

## 紹介用のGIF・動画を撮る(任意)

録画ソフトで範囲を決めて録画を始めてから、次を実行すると、アプリが自動で画面を切り替えます。

```
python tools/record_demo.py                 # 全体ツアー(約25秒)
python tools/record_demo.py --scene theme   # ダーク→ライト→ダーク
python tools/record_demo.py --scene run     # 作業画面の「実行」の流れ
python tools/record_demo.py --scene nav     # サイドバーで画面を切り替える
python tools/record_demo.py --scene dialogs # メッセージボックス4種
python tools/record_demo.py --scene scale   # UIの大きさ 100%→125%→100%
```

`--delay 3`(開始までの秒数)、`--speed 2`(倍速)、`--keep`(最後に閉じない)も使えます。
入力フォルダには、個人名の入らないダミーのパスが入ります。

## 動作確認の状況

| 項目 | 状況 |
|---|---|
| Linux (Xvfb 仮想画面) / Python 3.12 / customtkinter 6.0.0 / Pillow 12.3 | 3画面の表示・ライト/ダーク切替・ダイアログ・疑似実行を操作して、エラーなしを確認 |
| Windows 11 / Python 3.13 / customtkinter 6.0.0 / Pillow 12.3.0 | 実機で確認済み: 3画面の表示(ダーク)、ダッシュボードのライトモード、UIの大きさ125%、作業画面の「参照」「実行」、確認・警告・完了ダイアログ |
| ウィンドウのアイコン(`app.ico`) | Windows実機で、メイン画面とダイアログのタイトルバーが人参アイコンになることを確認。タスクバーは未確認 |
| 確認ダイアログの高さ | 実機で、ボタンが見切れず収まることを確認(高さは中身に合わせて自動で決まります) |
| 画面切替の方式 | 実機の録画で、テーマ切替の直後に画面を移ると約0.6秒まっ暗になったため、全画面を重ねて `tkraise()` で切り替える方式に変更。変更後の録画では、まっ暗はなくなった(描き替え途中のコマが約0.2秒写る) |
| ライト/ダーク切替 | 切替の瞬間に、全体の描き直しで0.2〜0.3秒ほど画面がちらつく(Windows実機の録画で確認) |
| 未確認 | UIの大きさを変えた後の作業画面、タスクバーのアイコン、Mac |

`requirements.txt` は、確認できたバージョン(customtkinter 6.0.0)に固定しています。
バージョンを上げると見た目が変わることがあるので、上げるときは画面を一通り確認してください。

## ライセンス

- このテンプレート: MIT License (`LICENSE`)
- アイコン: [Lucide](https://lucide.dev/) (ISC License) 。一部は Feather 由来で MIT License です。
  全文は `assets/icons_src/LICENSE-lucide.txt` にあります。
