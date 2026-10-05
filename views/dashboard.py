# -*- coding: utf-8 -*-
"""ダッシュボード画面: KPIカード4枚 + アクティビティ表 + 使用状況。gridの見本。"""
import customtkinter as ctk

import theme
from components.card import Card, StatCard
from views.base import BaseView

# 見本データ。実際のアプリでは、ここを自分のデータに差し替える。
STATS = [
    ("処理件数", "1,284", "先週比 +12.4%", "activity", theme.SUCCESS),
    ("ユーザー数", "356", "今週 +8 人", "users", theme.SUCCESS),
    ("データ件数", "48.2k", "先週比 +3.1%", "database", theme.SUCCESS),
    ("エラー", "3", "先週比 -2 件", "info", theme.DANGER),
]

ACTIVITIES = [
    ("請求書の取り込み", "完了", "10:42", theme.SUCCESS),
    ("売上データの集計", "完了", "10:15", theme.SUCCESS),
    ("取引先マスタの更新", "実行中", "09:58", theme.WARNING),
    ("月次レポート出力", "完了", "09:30", theme.SUCCESS),
    ("バックアップ", "失敗", "09:02", theme.DANGER),
]

USAGE = [
    ("ストレージ", 0.62),
    ("今月の処理枠", 0.38),
    ("API呼び出し", 0.81),
]


class DashboardView(BaseView):
    def __init__(self, master):
        super().__init__(master, "ダッシュボード", "全体の状況をひと目で確認できます")

        body = self.body
        # 12列の等幅グリッド。uniform を同じ名前にそろえると、列幅が均等になる。
        # KPIカードは3列ぶん×4枚、下段は 7列(アクティビティ)+5列(使用状況) に分ける
        for col in range(12):
            body.grid_columnconfigure(col, weight=1, uniform="col")
        body.grid_rowconfigure(1, weight=1)

        # --- 1行目: KPIカード ---
        for col, (title, value, note, icon_name, color) in enumerate(STATS):
            card = StatCard(body, title, value, note, icon_name, note_color=color)
            card.grid(row=0, column=col * 3, columnspan=3, sticky="nsew",
                      padx=(0 if col == 0 else 8, 0 if col == 3 else 8), pady=(0, 16))

        # --- 2行目左: アクティビティ(7列ぶん結合) ---
        activity = Card(body)
        activity.grid(row=1, column=0, columnspan=7, sticky="nsew", padx=(0, 8))
        activity.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            activity, text="最近のアクティビティ", anchor="w",
            font=theme.font(16, "bold"), text_color=theme.TEXT,
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=22, pady=(18, 8))

        for i, (name, status, time_text, color) in enumerate(ACTIVITIES, start=1):
            ctk.CTkLabel(
                activity, text=name, anchor="w", font=theme.font(14), text_color=theme.TEXT,
            ).grid(row=i, column=0, sticky="w", padx=(22, 8), pady=7)
            ctk.CTkLabel(
                activity, text=status, width=64, height=24, corner_radius=12,
                font=theme.font(12, "bold"), text_color=color, fg_color=theme.NAV_ACTIVE,
            ).grid(row=i, column=1, padx=8, pady=7)
            ctk.CTkLabel(
                activity, text=time_text, anchor="e", font=theme.font(13),
                text_color=theme.TEXT_MUTED,
            ).grid(row=i, column=2, sticky="e", padx=(8, 22), pady=7)

        # --- 2行目右: 使用状況(5列ぶん結合) ---
        usage = Card(body)
        usage.grid(row=1, column=7, columnspan=5, sticky="nsew", padx=(8, 0))
        usage.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            usage, text="使用状況", anchor="w", font=theme.font(16, "bold"),
            text_color=theme.TEXT,
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(18, 10))

        for i, (name, ratio) in enumerate(USAGE, start=1):
            row = ctk.CTkFrame(usage, fg_color="transparent")
            row.grid(row=i, column=0, sticky="ew", padx=22, pady=(4, 8))
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                row, text=name, anchor="w", font=theme.font(13), text_color=theme.TEXT_MUTED,
            ).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(
                row, text=f"{int(ratio * 100)}%", anchor="e", font=theme.font(13, "bold"),
                text_color=theme.TEXT,
            ).grid(row=0, column=1, sticky="e")
            bar = ctk.CTkProgressBar(
                row, height=8, corner_radius=4, fg_color=theme.NAV_ACTIVE,
                progress_color=theme.ACCENT,
            )
            bar.set(ratio)
            bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
