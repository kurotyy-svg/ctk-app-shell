# -*- coding: utf-8 -*-
"""
テーマ対応のメッセージボックス(Vol.3の完成版をこのテンプレ用に整えたもの)。

    from components.dialog import show_info, show_warning, show_error, ask_yes_no

    if ask_yes_no(self, "削除しますか？"):
        ...
"""
import customtkinter as ctk

import theme

_STYLES = {
    "info": {"color": theme.INFO, "symbol": "i"},
    "warning": {"color": theme.WARNING, "symbol": "!"},
    "error": {"color": theme.DANGER, "symbol": "×"},
    "question": {"color": theme.ACCENT, "symbol": "?"},
}

_W = 360  # ダイアログの最小の幅(高さは中身に合わせて自動で決まる)


class _MessageDialog(ctk.CTkToplevel):
    def __init__(self, parent, message, kind, buttons):
        super().__init__(parent)
        self.title("")
        theme.apply_window_icon(self)
        self.resizable(False, False)
        self.configure(fg_color=theme.BG_CARD)
        self.transient(parent)

        # 幅だけ最小値を決める細い見えない枠。高さは中身(メッセージの行数)に合わせて自動で伸びる。
        # (高さを固定すると、パスが長いメッセージでボタンが見切れる)
        ctk.CTkFrame(self, width=_W, height=1, fg_color="transparent").pack()

        self.result = None
        style = _STYLES[kind]

        ctk.CTkLabel(
            self, text=style["symbol"], width=42, height=42, corner_radius=21,
            fg_color=style["color"], text_color=theme.ON_ACCENT if kind == "question" else "white",
            font=theme.font(20, "bold"),
        ).pack(pady=(22, 10))

        ctk.CTkLabel(
            self, text=message, font=theme.font(14), text_color=theme.TEXT,
            wraplength=300, justify="center",
        ).pack(padx=24, pady=(0, 14), fill="x")

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=(0, 20))
        for label in buttons:
            secondary = label in ("いいえ", "キャンセル")
            ctk.CTkButton(
                row, text=label, width=104, height=36,
                corner_radius=theme.RADIUS_BUTTON, font=theme.font(13, "bold"),
                fg_color=theme.SECONDARY if secondary else theme.ACCENT,
                hover_color=theme.SECONDARY_HOVER if secondary else theme.ACCENT_HOVER,
                text_color=theme.TEXT if secondary else theme.ON_ACCENT,
                command=lambda v=label: self._finish(v),
            ).pack(side="left", padx=6)

        self.protocol("WM_DELETE_WINDOW", lambda: self._finish(None))

        # 親ウィンドウの中央に配置(中身が決まってから、実際の大きさで計算する)
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_reqwidth()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_reqheight()) // 2
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

        # モーダル化: 表示されてから grab_set() する(表示前だと失敗することがある)
        self.after(50, self._modalize)

    def _modalize(self):
        try:
            self.update_idletasks()  # 描画待ちの部品を先に描き切る(白抜けのまま表示されるのを防ぐ)
            self.lift()
            self.grab_set()
            self.focus_force()
        except Exception:
            self.after(50, self._modalize)

    def _finish(self, value):
        self.result = value
        self.destroy()


def _show(parent, message, kind, buttons):
    dialog = _MessageDialog(parent, message, kind, buttons)
    parent.wait_window(dialog)
    return dialog.result


def show_info(parent, message):
    _show(parent, message, "info", ["OK"])


def show_warning(parent, message):
    _show(parent, message, "warning", ["OK"])


def show_error(parent, message):
    _show(parent, message, "error", ["OK"])


def ask_yes_no(parent, message) -> bool:
    return _show(parent, message, "question", ["はい", "いいえ"]) == "はい"
