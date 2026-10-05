# -*- coding: utf-8 -*-
"""
SVGアイコンを、ライト用/ダーク用のPNGに書き出すスクリプト。

使い方:
    pip install -r tools/requirements-dev.txt
    python tools/build_icons.py

assets/icons_src/*.svg (Lucide, ISC License) を読み込み、
stroke="currentColor" をテーマごとの色に置き換えて
assets/icons/<名前>_light.png / <名前>_dark.png を作ります。

SVGの描画には resvg-py を使います。Windows用の完成品が pip で配られているので、
Cairo などのライブラリを別に入れなくても動きます。

ポイント: 画面に表示するサイズの約4倍(ICON_PX=96)で書き出します。
CTkImage(size=(22, 22)) のように小さく表示しても、
Windowsの拡大表示(125%/150%/200%)でボケにくくなります。
"""
from io import BytesIO
from pathlib import Path

import resvg_py
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "assets" / "icons_src"
OUT_DIR = ROOT / "assets" / "icons"

ICON_PX = 96  # 書き出しサイズ(サイドバーは22pxで表示 = 約4倍)

# テーマごとの線の色
COLORS = {
    "light": "#5b4a3c",  # ライトモード用(落ち着いた茶)
    "dark": "#d6c8ba",   # ダークモード用(やわらかい明るめのベージュ)
}
# ロゴ(carrot)だけは両テーマ共通のアクセント色
ACCENT = "#ff8a3d"

# 用途別のバリエーション(ファイル名: <名前>_<バリエーション>_light.png など)
#   accent   : サイドバーで「選択中」のとき使う、オレンジの線
#   onaccent : オレンジのボタンの上に載せる線(文字色と同じ色にそろえる)
VARIANTS = {
    "accent": {"light": "#c05208", "dark": "#ff8a3d"},
    "onaccent": {"light": "#ffffff", "dark": "#1a1209"},
}


def svg_to_png(svg_path: Path, color: str, size: int) -> bytes:
    svg = svg_path.read_text(encoding="utf-8").replace("currentColor", color)
    return resvg_py.svg_to_bytes(svg_string=svg, width=size, height=size)


def render(svg_path: Path, color: str, out_path: Path) -> None:
    out_path.write_bytes(svg_to_png(svg_path, color, ICON_PX))


def build_app_ico() -> None:
    """ウィンドウ左上(タイトルバー)用の app.ico を作る。

    .ico は1つのファイルに複数サイズ(16〜256px)を入れておくと、
    Windowsが表示場所に合わせて最適なサイズを選んでくれる。
    """
    png = svg_to_png(SRC_DIR / "carrot.svg", ACCENT, 256)
    img = Image.open(BytesIO(png)).convert("RGBA")
    img.save(
        ROOT / "assets" / "app.ico",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print("ok: app.ico")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for svg_path in sorted(SRC_DIR.glob("*.svg")):
        name = svg_path.stem
        if name == "carrot":
            render(svg_path, ACCENT, OUT_DIR / f"{name}_light.png")
            render(svg_path, ACCENT, OUT_DIR / f"{name}_dark.png")
        else:
            for mode, color in COLORS.items():
                render(svg_path, color, OUT_DIR / f"{name}_{mode}.png")
            for variant, colors in VARIANTS.items():
                for mode, color in colors.items():
                    render(svg_path, color, OUT_DIR / f"{name}_{variant}_{mode}.png")
        print("ok:", name)
    build_app_ico()


if __name__ == "__main__":
    main()
