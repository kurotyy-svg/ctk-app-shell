# -*- coding: utf-8 -*-
"""
色・フォント・アイコンの設定をここ1か所にまとめています。
見た目を変えたいときは、基本的にこのファイルだけ編集すればOKです。

色はすべて (ライトモードの色, ダークモードの色) のタプルで書いています。
CustomTkinterは、このタプルを fg_color などに渡すと
set_appearance_mode() の切り替えに合わせて自動で色を切り替えてくれます。
"""
import sys
from pathlib import Path

import customtkinter as ctk
from PIL import Image

# ------------------------------------------------------------
# 色 (ライト, ダーク)
# ------------------------------------------------------------
BG_BASE = ("#f6efe7", "#16130f")       # 画面全体の背景
BG_SIDEBAR = ("#efe3d5", "#100e0b")    # サイドバーの背景
BG_CARD = ("#ffffff", "#211c17")       # カードの背景
BG_INPUT = ("#fbf6f0", "#2a231c")      # 入力欄の背景
BORDER = ("#e6d5c3", "#33291f")        # カードの枠線

TEXT = ("#2b221a", "#f1e8de")          # 本文
TEXT_MUTED = ("#8a7a6a", "#a39484")    # 補足テキスト

ACCENT = ("#c05208", "#ff8a3d")        # アクセント(ブログのオレンジ)
ACCENT_HOVER = ("#a84606", "#ff9f5e")
ON_ACCENT = ("#ffffff", "#1a1209")     # アクセント色の上に載せる文字色

NAV_HOVER = ("#e6d6c4", "#1d1812")     # サイドバーのホバー色
NAV_ACTIVE = ("#f8dcc2", "#2e2015")    # サイドバーで選択中の背景色

SECONDARY = ("#d9cbbd", "#3a3128")     # 「いいえ」など控えめなボタン
SECONDARY_HOVER = ("#cdbdac", "#4a3f34")

SUCCESS = ("#3f7f2f", "#7cc362")
WARNING = ("#b97a12", "#f0b04a")
DANGER = ("#b3322a", "#ff6b5e")
INFO = ("#2f6fae", "#6fb1ee")

# ------------------------------------------------------------
# 形(角丸・余白)
# ------------------------------------------------------------
RADIUS_CARD = 14
RADIUS_BUTTON = 10
PAD = 24  # 画面端の余白

# ------------------------------------------------------------
# フォント
# ------------------------------------------------------------
# Windowsでは「Yu Gothic UI」、それ以外はOS標準にまかせます。
FONT_FAMILY = "Yu Gothic UI" if sys.platform == "win32" else None


def font(size: int = 14, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)


# ------------------------------------------------------------
# アイコン
# ------------------------------------------------------------
# PNGは96pxで書き出し、サイドバーには22pxで表示します(約4倍)。
# 拡大率の高いWindows画面でもボケにくくするためです。
ICON_DIR = Path(__file__).resolve().parent / "assets" / "icons"
_icon_cache = {}


def icon(name: str, size: int = 22, variant: str = "") -> ctk.CTkImage:
    """
    assets/icons/ の PNG から CTkImage を作る。
    light_image(ライトモード用)と dark_image(ダークモード用)を渡しておくと、
    set_appearance_mode() の切り替えに合わせて自動で画像も切り替わる。

    variant: "" = 通常 / "accent" = オレンジ線 / "onaccent" = オレンジのボタン上用
    """
    key = (name, size, variant)
    if key not in _icon_cache:
        stem = f"{name}_{variant}" if variant else name
        _icon_cache[key] = ctk.CTkImage(
            light_image=Image.open(ICON_DIR / f"{stem}_light.png"),
            dark_image=Image.open(ICON_DIR / f"{stem}_dark.png"),
            size=(size, size),
        )
    return _icon_cache[key]


# ------------------------------------------------------------
# ウィンドウのアイコン(タイトルバー左上・タスクバー)
# ------------------------------------------------------------
APP_ICO = Path(__file__).resolve().parent / "assets" / "app.ico"


def apply_window_icon(window) -> None:
    """
    CustomTkinter 標準の青いアイコンを、このアプリのアイコンに置き換える(Windows用)。

    CustomTkinter は、ウィンドウを作った約200ミリ秒後に標準アイコンを設定します。
    ただし iconbitmap() を自分で先に呼んでおくと、そちらが優先されます。
    なので、ウィンドウの __init__ の中でこの関数を呼びます。
    Windows以外では .ico が使えないため、何もしません。
    """
    if sys.platform != "win32" or not APP_ICO.exists():
        return
    try:
        window.iconbitmap(str(APP_ICO))
    except Exception:
        pass
