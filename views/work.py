# -*- coding: utf-8 -*-
"""作業画面: 入力 → 実行 → ログ表示。自分のツールの処理をつなぐ場所。"""
import queue
import threading
import time
from tkinter import filedialog

import customtkinter as ctk

import theme
from components.card import Card
from components.dialog import ask_yes_no, show_error, show_info, show_warning
from views.base import BaseView


def run_job(folder: str, output_name: str, mode: str, log, progress) -> None:
    """
    ★ここを自分の処理に差し替えます★

    「実行」ボタンを押して確認ダイアログで「はい」を選ぶと、この関数が別スレッドで呼ばれます。
    時間のかかる処理を書いても、画面は固まりません。

      folder       : 「参照」で選んだフォルダ
      output_name  : 「出力ファイル名」の欄の文字
      mode         : 「処理モード」で選んだ項目
      log("文字")   : ログ欄に1行追加する
      progress(0.5): 進捗バーを更新する(0.0 〜 1.0)

    注意: この中から CTkLabel などの画面の部品を直接さわらないでください
    (必ず log() / progress() を通します)。エラーは raise すれば、エラーダイアログが出ます。

    いまはデモです。フォルダの中身は見ませんし、ファイルも作りません。
    """
    steps = ["ファイルを読み込み中", "データを整形中", "集計中", "結果を書き出し中"]
    for i, step in enumerate(steps, start=1):
        log(f"({i}/{len(steps)}) {step}…")
        time.sleep(0.5)  # ← 本物の処理に置き換える
        progress(i / len(steps))
    log("完了(デモ): 実際のファイル処理は行っていません。")


class WorkView(BaseView):
    def __init__(self, master):
        super().__init__(master, "作業", "フォルダを選んで実行すると、ログに進み具合が表示されます")
        self._running = False

        body = self.body
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        # ---------------- 入力カード ----------------
        form = Card(body)
        form.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        form.grid_columnconfigure(1, weight=1)

        def label(text, row):
            ctk.CTkLabel(
                form, text=text, anchor="w", font=theme.font(13, "bold"), text_color=theme.TEXT,
            ).grid(row=row, column=0, sticky="w", padx=(22, 12), pady=10)

        def entry_style():
            return dict(
                height=38, corner_radius=theme.RADIUS_BUTTON, border_width=1,
                fg_color=theme.BG_INPUT, border_color=theme.BORDER, text_color=theme.TEXT,
                font=theme.font(13),
            )

        label("入力フォルダ", 0)
        self.folder_entry = ctk.CTkEntry(
            form, placeholder_text="処理するフォルダを選択してください", **entry_style()
        )
        self.folder_entry.grid(row=0, column=1, sticky="ew", pady=10)
        ctk.CTkButton(
            form, text="参照", image=theme.icon("folder-open", 18), compound="left",
            width=90, height=38, corner_radius=theme.RADIUS_BUTTON, font=theme.font(13, "bold"),
            fg_color=theme.SECONDARY, hover_color=theme.SECONDARY_HOVER, text_color=theme.TEXT,
            command=self._browse,
        ).grid(row=0, column=2, padx=(10, 22), pady=10)

        label("出力ファイル名", 1)
        self.output_entry = ctk.CTkEntry(form, **entry_style())
        self.output_entry.insert(0, "result.xlsx")
        self.output_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(0, 22), pady=10)

        label("処理モード", 2)
        self.mode_menu = ctk.CTkOptionMenu(
            form, values=["標準", "高速(簡易チェック)", "詳細(ログ多め)"], height=38,
            corner_radius=theme.RADIUS_BUTTON, font=theme.font(13), dropdown_font=theme.font(13),
            fg_color=theme.BG_INPUT, button_color=theme.SECONDARY,
            button_hover_color=theme.SECONDARY_HOVER, text_color=theme.TEXT,
            dropdown_fg_color=theme.BG_CARD, dropdown_hover_color=theme.NAV_HOVER,
            dropdown_text_color=theme.TEXT,
        )
        self.mode_menu.grid(row=2, column=1, columnspan=2, sticky="w", pady=10)

        buttons = ctk.CTkFrame(form, fg_color="transparent")
        buttons.grid(row=3, column=0, columnspan=3, sticky="w", padx=22, pady=(6, 20))
        self.run_button = ctk.CTkButton(
            buttons, text="実行", image=theme.icon("play", 18, "onaccent"), compound="left", width=120,
            height=40, corner_radius=theme.RADIUS_BUTTON, font=theme.font(14, "bold"),
            fg_color=theme.ACCENT, hover_color=theme.ACCENT_HOVER, text_color=theme.ON_ACCENT,
            command=self._on_run,
        )
        self.run_button.pack(side="left")
        ctk.CTkButton(
            buttons, text="ログをクリア", width=120, height=40,
            corner_radius=theme.RADIUS_BUTTON, font=theme.font(13, "bold"),
            fg_color=theme.SECONDARY, hover_color=theme.SECONDARY_HOVER, text_color=theme.TEXT,
            command=self._clear_log,
        ).pack(side="left", padx=(10, 0))

        # ---------------- ログカード ----------------
        log_card = Card(body)
        log_card.grid(row=1, column=0, sticky="nsew")
        log_card.grid_columnconfigure(0, weight=1)
        log_card.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            log_card, text="ログ", anchor="w", font=theme.font(16, "bold"), text_color=theme.TEXT,
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(18, 8))

        self.progress = ctk.CTkProgressBar(
            log_card, height=8, corner_radius=4, fg_color=theme.NAV_ACTIVE,
            progress_color=theme.ACCENT,
        )
        self.progress.set(0)
        self.progress.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 12))

        self.log_box = ctk.CTkTextbox(
            log_card, corner_radius=theme.RADIUS_BUTTON, border_width=1,
            fg_color=theme.BG_INPUT, border_color=theme.BORDER, text_color=theme.TEXT,
            font=ctk.CTkFont(family="Consolas" if theme.FONT_FAMILY else None, size=13),
        )
        self.log_box.grid(row=2, column=0, sticky="nsew", padx=22, pady=(0, 20))
        self.log_box.configure(state="disabled")
        self._log("準備完了。(デモ表示: 実際のファイル処理は行いません)")
        self._log("使うときは run_job() を自分の処理に差し替えてください。")

    # ---------------- 動作 ----------------
    def _browse(self):
        folder = filedialog.askdirectory(title="処理するフォルダを選択")
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)

    def _log(self, text: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        self.progress.set(0)

    def _on_run(self):
        if self._running:
            return
        folder = self.folder_entry.get().strip()
        if not folder:
            show_warning(self.winfo_toplevel(), "入力フォルダを選択してください。")
            return
        # はい/いいえの戻り値(bool)で、処理を進めるか止めるかを分岐する
        if not ask_yes_no(self.winfo_toplevel(), f"次のフォルダを処理します。\n{folder}\n\n実行しますか？"):
            self._log("キャンセルされました。")
            return
        self._start_job(folder)

    def _start_job(self, folder: str):
        # 画面の部品の値は、必ずメインスレッド(ここ)で読み取ってから渡す
        output_name = self.output_entry.get().strip()
        mode = self.mode_menu.get()

        self._running = True
        self.run_button.configure(state="disabled", text="実行中…")
        self.progress.set(0)
        self._log(f"開始: {folder}")
        self._log(f"モード: {mode}")

        # 別スレッドからは、queue 経由でメインスレッドに結果を渡す
        q = queue.Queue()
        self._queue = q

        def worker():
            try:
                run_job(
                    folder, output_name, mode,
                    log=lambda text: q.put(("log", text)),
                    progress=lambda value: q.put(("progress", value)),
                )
                q.put(("done", None))
            except Exception as e:  # noqa: BLE001
                q.put(("error", str(e)))

        threading.Thread(target=worker, daemon=True).start()
        self.after(100, self._poll_queue)

    def _poll_queue(self):
        """100ミリ秒ごとに queue を確認し、届いた内容を画面に反映する。"""
        finished = None
        try:
            while True:
                kind, value = self._queue.get_nowait()
                if kind == "log":
                    self._log(value)
                elif kind == "progress":
                    self.progress.set(value)
                else:  # "done" or "error"
                    finished = (kind, value)
        except queue.Empty:
            pass

        if finished is None:
            self.after(100, self._poll_queue)
            return

        self._running = False
        self.run_button.configure(state="normal", text="実行")
        kind, value = finished
        if kind == "done":
            show_info(self.winfo_toplevel(), "処理が完了しました。")
        else:
            self._log(f"エラー: {value}")
            show_error(self.winfo_toplevel(), f"処理中にエラーが発生しました。\n{value}")
