# 論文PDF → 日本語訳HTML（画像埋め込み）作成フロー

## 概要

PDFで受け取った論文を、全文日本語訳・全図埋め込みの単一HTMLファイルに変換してGitHubにプッシュするまでの手順。

---

## Step 1: PDFのページ画像を生成する

```bash
mkdir -p AgentHospital/images
pdftoppm -r 150 -png /path/to/paper.pdf AgentHospital/images/page
# → page-01.png 〜 page-XX.png が生成される（1275×1650px @ 150DPI）
```

## Step 2: PDF埋め込み画像を抽出する（写真・スクリーンショット用）

```bash
mkdir -p AgentHospital/figures
pdfimages -png /path/to/paper.pdf AgentHospital/figures/fig
# → fig-000.png 〜 fig-XXX.png が生成される
# pdfimages -list で各画像のページ番号・サイズを確認できる
```

## Step 3: 各Figureをページ画像から切り出す

```python
from PIL import Image

# ページ画像は 1275×1650px（150DPI、A4/Letter相当）
# 各Figureのページ番号と大まかな座標（left, upper, right, lower）を指定して切り出す

crops = {
    "figure3": ("page-05.png", 50, 50, 1225, 1010),
    "figure4": ("page-06.png", 50, 50, 1225, 1540),
    # ... 全Figureを列挙
}
for name, (page, l, u, r, lo) in crops.items():
    img = Image.open(f"images/{page}")
    img.crop((l, u, r, lo)).save(f"figures/{name}.png")
```

**使い分け：**
- PDF埋め込みの写真・スクリーンショット → `pdfimages` で抽出したものをそのまま使用（高解像度）
- グラフ・テキストボックス・図表 → `pdftoppm` のページ画像から切り出し

## Step 4: HTMLを作成する（翻訳 + 図の配置）

単一のHTMLファイルとして作成する。構成：

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <style>
    /* 論文レイアウト用CSS（body幅・見出し・figure・table・参考文献スタイルなど） */
  </style>
</head>
<body>
  <!-- タイトル・著者・所属・要旨 -->
  <!-- 本文（日本語訳） -->
  <figure>
    <img src="figures/figureX.png" alt="...">
    <figcaption><strong>図X.</strong> キャプション日本語訳</figcaption>
  </figure>
  <!-- 表は <table> タグで再現 -->
  <!-- 参考文献 <ol class="references"> -->
  <!-- 付録 -->
</body>
</html>
```

**翻訳方針：**
- 本文・キャプション・表の中身・参考文献リストはすべて日本語に翻訳
- モデル名・手法名（GPT-4、MedAgent-Zero、SEAL等）は英語のまま残す

## Step 5: 画像をBase64でHTMLに埋め込む（単一ファイル化）

```python
import base64, re, os

with open("日本語訳_画像込み.html", "r", encoding="utf-8") as f:
    html = f.read()

def replace_img(match):
    src = match.group(1)
    with open(src, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f'src="data:image/png;base64,{data}"'

html = re.sub(r'src="(figures/[^"]+)"', replace_img, html)

with open("日本語訳_画像込み.html", "w", encoding="utf-8") as f:
    f.write(html)
```

**ファイルサイズの目安：**
- PNG画像合計 × 約1.33（Base64オーバーヘッド）+ HTML本文
- 例：画像9.6MB → HTML単体で約12.5MB
- GitHubの無料アカウントでも100MB未満なら問題なくプッシュ可能

## Step 6: GitHubにプッシュする

```bash
git add AgentHospital/日本語訳_画像込み.html
git commit -m "Add Japanese translation of [論文名] with embedded figures"
git push origin main
```

---

## 使用ツール

| ツール | 用途 |
|--------|------|
| `pdftoppm` | PDFページをPNG画像に変換（poppler-utils） |
| `pdfimages` | PDF埋め込み画像を抽出（poppler-utils） |
| Python `Pillow` | ページ画像からFigureを切り出し |
| Python `base64` + `re` | 画像をHTMLにBase64埋め込み |

インストール：
```bash
sudo apt install poppler-utils
pip install pillow
```
