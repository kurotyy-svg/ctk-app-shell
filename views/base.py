# -*- coding: utf-8 -*-
"""全画面共通の土台。タイトルと説明文を表示し、その下に body を用意する。"""
import customtkinter as ctk

import theme


class BaseView(ctk.CTkFrame):
    def __init__(self, master, title: str, subtitle: str = ""):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=theme.PAD, pady=(theme.PAD, 14))
        ctk.CTkLabel(
            header, text=title, anchor="w", font=theme.font(26, "bold"),
            text_color=theme.TEXT,
        ).pack(fill="x")
        if subtitle:
            ctk.CTkLabel(
                header, text=subtitle, anchor="w", font=theme.font(13),
                text_color=theme.TEXT_MUTED,
            ).pack(fill="x", pady=(2, 0))

        # 各画面は、この body の中に部品を置く
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.grid(row=1, column=0, sticky="nsew", padx=theme.PAD, pady=(0, theme.PAD))
