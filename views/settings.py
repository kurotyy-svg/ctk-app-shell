# -*- coding: utf-8 -*-
"""設定画面: 外観(ダーク/ライト/システム)・スイッチ・UIサイズ。"""
from importlib.metadata import version

import customtkinter as ctk

import theme
from components.card import Card
from views.base import BaseView

MODES = [("ダーク", "dark"), ("ライト", "light"), ("システムに合わせる", "system")]


class SettingsView(BaseView):
    def __init__(self, master, on_mode_change):
        super().__init__(master, "設定", "見た目や動作のオプションを変更できます")
        self._on_mode_change = on_mode_change

        body = self.body
        body.grid_columnconfigure(0, weight=1)

        # ---------------- 外観 ----------------
        look = Card(body)
        look.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self._section_title(look, "外観")

        self.mode_var = ctk.StringVar(value="dark")
        radios = ctk.CTkFrame(look, fg_color="transparent")
        radios.pack(fill="x", padx=22, pady=(0, 8))
        for text, value in MODES:
            ctk.CTkRadioButton(
                radios, text=text, value=value, variable=self.mode_var,
                font=theme.font(13), text_color=theme.TEXT,
                fg_color=theme.ACCENT, hover_color=theme.ACCENT_HOVER, border_color=theme.BORDER,
                command=lambda: self._on_mode_change(self.mode_var.get()),
            ).pack(side="left", padx=(0, 22))

        size_row = ctk.CTkFrame(look, fg_color="transparent")
        size_row.pack(fill="x", padx=22, pady=(8, 20))
        ctk.CTkLabel(
            size_row, text="UIの大きさ", font=theme.font(13), text_color=theme.TEXT,
        ).pack(side="left")
        ctk.CTkOptionMenu(
            size_row, values=["90%", "100%", "110%", "125%"], width=100, height=34,
            corner_radius=theme.RADIUS_BUTTON, font=theme.font(13), dropdown_font=theme.font(13),
            fg_color=theme.BG_INPUT, button_color=theme.SECONDARY,
            button_hover_color=theme.SECONDARY_HOVER, text_color=theme.TEXT,
            dropdown_fg_color=theme.BG_CARD, dropdown_hover_color=theme.NAV_HOVER,
            dropdown_text_color=theme.TEXT,
            command=lambda v: ctk.set_widget_scaling(int(v.rstrip("%")) / 100),
        ).pack(side="left", padx=(12, 0))
        self._size_menu = size_row.winfo_children()[-1]
        self._size_menu.set("100%")

        # ---------------- 動作 ----------------
        behavior = Card(body)
        behavior.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        self._section_title(behavior, "動作")
        for text, on in [("完了時に通知する", True), ("起動時に前回のフォルダを開く", True),
                         ("ログを自動で保存する", False)]:
            sw = ctk.CTkSwitch(
                behavior, text=text, font=theme.font(13), text_color=theme.TEXT,
                progress_color=theme.ACCENT, button_color=("#5b4a3c", "#f1e8de"),
                button_hover_color=("#3f3228", "#ffffff"), fg_color=theme.SECONDARY,
            )
            if on:
                sw.select()
            sw.pack(anchor="w", padx=22, pady=7)
        sw.pack_configure(pady=(7, 26))  # 最後のスイッチだけ下に余白を足す

        # ---------------- このアプリについて ----------------
        about = Card(body)
        about.grid(row=2, column=0, sticky="ew")
        self._section_title(about, "このアプリについて")
        ctk.CTkLabel(
            about, anchor="w", justify="left", font=theme.font(13), text_color=theme.TEXT_MUTED,
            text=f"CTk App Shell v1.0.0\nCustomTkinter {version('customtkinter')}",
        ).pack(fill="x", padx=22, pady=(0, 20))

    @staticmethod
    def _section_title(parent, text):
        ctk.CTkLabel(
            parent, text=text, anchor="w", font=theme.font(16, "bold"), text_color=theme.TEXT,
        ).pack(fill="x", padx=22, pady=(18, 10))

    def sync_mode(self, mode: str):
        """サイドバーのボタンなど、設定画面の外でモードが変わったときに表示を合わせる。"""
        self.mode_var.set(mode)
