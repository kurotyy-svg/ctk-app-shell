# -*- coding: utf-8 -*-
"""
GIF/動画の撮影用: アプリを自動で操作してくれるデモスクリプト。

使い方(録画ソフトで範囲を決めて録画を始めてから、これを実行):
    python tools/record_demo.py              # 全体ツアー(約25秒)
    python tools/record_demo.py --scene theme   # ダーク→ライト→ダークだけ(約8秒)
    python tools/record_demo.py --scene run     # 作業画面の「実行」の流れだけ(約12秒)
    python tools/record_demo.py --scene nav     # サイドバーで画面を切り替える(約7秒)
    python tools/record_demo.py --scene dialogs # メッセージボックス4種(約12秒)
    python tools/record_demo.py --scene scale   # UIの大きさ 100%→125%→100%(約12秒)

オプション:
    --delay 3     開始までの待ち時間(秒)。録画ボタンを押す余裕のため(既定 3)
    --speed 1.0   2.0 にすると2倍速で進む(動作確認用)
    --keep        最後にウィンドウを閉じない

アプリの本物の画面・本物の処理をそのまま動かしています(マウスのクリックそのものではなく、
画面切替やボタンの処理を呼び出しています)。ダイアログの「はい」「OK」だけは自動で押します。
入力フォルダには、個人名の入らないダミーのパスを入れます。
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk  # noqa: E402

from components.dialog import ask_yes_no, show_error, show_info, show_warning  # noqa: E402
from main import App  # noqa: E402

DEMO_PATH = "C:/Users/demo/Documents/請求書フォルダ"
WINDOW_POS = "+80+60"  # 録画範囲を合わせやすいよう、位置を固定する


def find_buttons(widget):
    found = []
    for child in widget.winfo_children():
        if child.__class__.__name__ == "CTkButton":
            found.append(child)
        found.extend(find_buttons(child))
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", choices=["all", "theme", "run", "nav", "dialogs", "scale"], default="all")
    parser.add_argument("--delay", type=float, default=3.0)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    app = App()
    app.geometry(WINDOW_POS)  # 位置だけ指定(大きさは変えない)
    work = app.views["work"]

    def wait(sec):
        return sec / args.speed

    # ---- ダイアログの自動クリック(最初のボタン = 「はい」/「OK」) ----
    seen = {}

    def dialog_watcher():
        now = time.time()
        for w in list(app.winfo_children()):
            if w.__class__.__name__ == "_MessageDialog":
                buttons = find_buttons(w)
                # ダイアログが実際に画面に出て、ボタンまで描かれてから数え始める
                if not buttons or not w.winfo_viewable() or not buttons[0].winfo_ismapped():
                    continue
                first = seen.setdefault(id(w), now)
                if now - first >= wait(2.0):  # 2秒見せてから押す
                    buttons[0].invoke()
        app.after(100, dialog_watcher)

    # ---- 場面の部品 ----
    def type_path():
        work.folder_entry.delete(0, "end")
        for ch in DEMO_PATH:
            work.folder_entry.insert("end", ch)
            app.update()
            time.sleep(wait(0.05))

    def wait_job_finished():
        # 実行が終わり、完了ダイアログも閉じるまで待つ
        while work._running or any(
            w.__class__.__name__ == "_MessageDialog" for w in app.winfo_children()
        ):
            app.update()
            time.sleep(0.05)

    def scene_theme():
        app.show_view("dashboard")
        yield 1.5
        app.toggle_theme()  # ライトへ
        yield 3.0
        app.toggle_theme()  # ダークへ戻す
        yield 2.0

    def scene_run():
        app.show_view("work")
        yield 1.2
        type_path()
        yield 0.8
        work._on_run()  # 確認ダイアログ → 自動で「はい」 → 実行
        wait_job_finished()  # 完了ダイアログも自動で「OK」
        yield 2.0

    def scene_all():
        app.show_view("dashboard")
        yield 3.0
        yield from scene_run()
        app.show_view("settings")
        yield 2.0
        app.toggle_theme()  # ライトへ
        yield 2.5
        app.show_view("dashboard")
        yield 2.5
        app.show_view("work")
        yield 2.0
        app.show_view("dashboard")
        yield 1.0
        app.toggle_theme()  # ダークへ戻して締める
        yield 3.0

    def scene_nav():
        # サイドバーの選択中ボタン(オレンジの背景・オレンジのアイコン)が移っていく様子
        for key in ["dashboard", "work", "settings", "dashboard"]:
            app.show_view(key)
            yield 1.6

    def scene_dialogs():
        # 4種類のメッセージボックス(それぞれ2秒見せてから自動で閉じる)
        app.show_view("work")
        yield 1.0
        show_info(app, "保存が完了しました。")
        yield 0.4
        show_warning(app, "未保存の変更があります。")
        yield 0.4
        show_error(app, "ファイルを読み込めませんでした。")
        yield 0.4
        ask_yes_no(app, "このファイルを削除しますか？")
        yield 1.0

    def scene_scale():
        # 設定の「UIの大きさ」を125%にして、ダッシュボードが崩れないことを見せる
        settings = app.settings_view
        app.show_view("settings")
        yield 1.2
        settings._size_menu.set("125%")
        ctk.set_widget_scaling(1.25)
        yield 1.6
        app.show_view("dashboard")
        yield 3.0
        app.show_view("settings")
        yield 1.0
        settings._size_menu.set("100%")
        ctk.set_widget_scaling(1.0)
        yield 1.2
        app.show_view("dashboard")
        yield 2.0

    scenes = {
        "all": scene_all, "theme": scene_theme, "run": scene_run,
        "nav": scene_nav, "dialogs": scene_dialogs, "scale": scene_scale,
    }

    def step(gen):
        try:
            delay = next(gen)
        except StopIteration:
            if not args.keep:
                app.after(300, app.quit)
            return
        app.after(int(wait(delay) * 1000), lambda: step(gen))

    def start():
        print("開始します(Ctrl+C またはウィンドウを閉じると中止)")
        app.after(100, dialog_watcher)
        step(scenes[args.scene]())

    app.update()
    print(f"{args.delay:g}秒後に開始します。録画を始めてください。")
    app.after(int(args.delay * 1000), start)
    app.mainloop()
    print("終了しました。")


if __name__ == "__main__":
    main()
