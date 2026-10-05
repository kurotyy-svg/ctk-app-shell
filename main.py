# -*- coding: utf-8 -*-
"""
CTk App Shell - CustomTkinter 用のサイドバー付きアプリテンプレート

起動:
    pip install -r requirements.txt
    python main.py

自分のアプリにするには:
    1. views/ に新しい画面(BaseViewを継承したクラス)を足す
    2. このファイルの NAV_ITEMS と、下の self.views に1行ずつ足す
    3. 色を変えたいときは theme.py を編集する
"""
import customtkinter as ctk

import theme
from components.sidebar import Sidebar
from views.dashboard import DashboardView
from views.settings import SettingsView
from views.work import WorkView

# (キー, サイドバーの表示名, アイコン名)  アイコンは assets/icons/ にあるもの
NAV_ITEMS = [
    ("dashboard", "ダッシュボード", "layout-dashboard"),
    ("work", "作業", "terminal"),
    ("settings", "設定", "settings"),
]


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=theme.BG_BASE)
        ctk.set_appearance_mode("dark")

        self.title("CTk App Shell")
        theme.apply_window_icon(self)  # タイトルバーの青い標準アイコンを置き換える
        self.geometry("1120x720")
        self.minsize(960, 640)

        # 左: サイドバー(幅固定) / 右: 画面(伸縮)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self, NAV_ITEMS, on_select=self.show_view, on_toggle_theme=self.toggle_theme
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=1, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.settings_view = SettingsView(container, on_mode_change=self.set_mode)
        self.views = {
            "dashboard": DashboardView(container),
            "work": WorkView(container),
            "settings": self.settings_view,
        }
        # 全画面を同じマスに重ねて置いておき、表示したい画面を一番上に持ってくる(tkraise)。
        # grid_remove() で隠す方式だと、ライト/ダーク切替のあとに別の画面へ移ったとき、
        # 隠れていた画面の描き直しが表示の瞬間に起きて、一瞬まっ暗になる(Windows実機の録画で判明)。
        # 重ねておけば、裏の画面もテーマ切替の時点で描き直されるので、切替が一瞬で済む。
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")
        self.show_view("dashboard")

    def show_view(self, key: str):
        """指定した画面を一番上に出し、サイドバーの選択表示も合わせる。"""
        self.views[key].tkraise()
        self.sidebar.set_active(key)

    def set_mode(self, mode: str):
        ctk.set_appearance_mode(mode)  # "dark" / "light" / "system"

    def toggle_theme(self):
        new_mode = "light" if ctk.get_appearance_mode() == "Dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        self.settings_view.sync_mode(new_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
