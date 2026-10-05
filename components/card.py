# -*- coding: utf-8 -*-
"""カード部品。Card は中身を自由に置ける枠、StatCard は数字を見せるKPIカード。"""
import customtkinter as ctk

import theme


class Card(ctk.CTkFrame):
    """角丸+薄い枠線の入れ物。中身は自分で pack / grid して使う。"""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=theme.BG_CARD,
            corner_radius=theme.RADIUS_CARD,
            border_width=1,
            border_color=theme.BORDER,
            **kwargs,
        )


class StatCard(Card):
    """タイトル・大きな数字・補足・アイコンを並べたKPIカード。"""

    def __init__(self, master, title, value, note, icon_name, note_color=theme.SUCCESS):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text=title, anchor="w", font=theme.font(12),
            text_color=theme.TEXT_MUTED,
        ).grid(row=0, column=0, sticky="w", padx=(20, 0), pady=(16, 0))

        # アイコンは「角丸の背景つきラベル」にすると、バッジ風にできる。
        # 1行目だけに置く(2段ぶん占有しない)ことで、下の数字をカード幅いっぱいに使える。
        # → 「UIの大きさ」を125%にしても数字が見切れにくい
        ctk.CTkLabel(
            self, text="", image=theme.icon(icon_name, 18), width=34, height=34,
            corner_radius=10, fg_color=theme.NAV_ACTIVE,
        ).grid(row=0, column=1, padx=(6, 16), pady=(14, 0), sticky="ne")

        self._value = ctk.CTkLabel(
            self, text=value, anchor="w", font=theme.font(30, "bold"),
            text_color=theme.TEXT,
        )
        self._value.grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 0))

        ctk.CTkLabel(
            self, text=note, anchor="w", font=theme.font(12),
            text_color=note_color,
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(2, 18))

    def set_value(self, value: str) -> None:
        self._value.configure(text=value)
