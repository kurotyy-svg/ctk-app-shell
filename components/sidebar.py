# -*- coding: utf-8 -*-
"""左側のサイドバー(ロゴ・ナビボタン・テーマ切替)。"""
import customtkinter as ctk

import theme


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, items, on_select, on_toggle_theme, app_name="CTk App Shell"):
        """
        items: [(キー, 表示名, アイコン名), ...]
        on_select(キー): ナビボタンが押されたときに呼ばれる
        on_toggle_theme(): 下部のテーマ切替ボタンが押されたときに呼ばれる
        """
        super().__init__(master, width=232, corner_radius=0, fg_color=theme.BG_SIDEBAR)
        self.pack_propagate(False)  # 幅を固定する

        self._on_select = on_select
        self._buttons = {}
        self._icons = {}  # キー -> アイコン名

        # --- ロゴ ---
        logo = ctk.CTkFrame(self, fg_color="transparent")
        logo.pack(fill="x", padx=20, pady=(26, 22))
        ctk.CTkLabel(logo, text="", image=theme.icon("carrot", 30)).pack(side="left")
        ctk.CTkLabel(
            logo, text=app_name, font=theme.font(17, "bold"), text_color=theme.TEXT
        ).pack(side="left", padx=(10, 0))

        ctk.CTkLabel(
            self, text="MENU", anchor="w", font=theme.font(11, "bold"),
            text_color=theme.TEXT_MUTED,
        ).pack(fill="x", padx=26, pady=(0, 6))

        # --- ナビボタン ---
        for key, label, icon_name in items:
            btn = ctk.CTkButton(
                self,
                text=f"  {label}",
                image=theme.icon(icon_name),
                anchor="w",
                height=42,
                corner_radius=theme.RADIUS_BUTTON,
                fg_color="transparent",
                hover_color=theme.NAV_HOVER,
                text_color=theme.TEXT,
                font=theme.font(14, "bold"),
                command=lambda k=key: self._on_select(k),
            )
            btn.pack(fill="x", padx=14, pady=3)
            self._buttons[key] = btn
            self._icons[key] = icon_name

        # --- 下部(テーマ切替・バージョン) ---
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=14, pady=(0, 18))

        ctk.CTkButton(
            bottom,
            text="  ライト/ダーク切替",
            image=theme.icon("sun"),
            anchor="w",
            height=40,
            corner_radius=theme.RADIUS_BUTTON,
            fg_color="transparent",
            border_width=1,
            border_color=theme.BORDER,
            hover_color=theme.NAV_HOVER,
            text_color=theme.TEXT_MUTED,
            font=theme.font(13),
            command=on_toggle_theme,
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            bottom, text="v1.0.0", anchor="w", font=theme.font(11),
            text_color=theme.TEXT_MUTED,
        ).pack(fill="x", padx=6)

    def set_active(self, key: str) -> None:
        """選択中のナビボタンをアクセント色でハイライトする。"""
        for k, btn in self._buttons.items():
            icon_name = self._icons[k]
            if k == key:
                btn.configure(
                    fg_color=theme.NAV_ACTIVE, text_color=theme.ACCENT,
                    image=theme.icon(icon_name, variant="accent"),
                )
            else:
                btn.configure(
                    fg_color="transparent", text_color=theme.TEXT,
                    image=theme.icon(icon_name),
                )
