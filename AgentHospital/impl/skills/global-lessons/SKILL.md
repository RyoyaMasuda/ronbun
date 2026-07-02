---
name: global-lessons
description: 過去の診察教訓（global_lessons.json）を読み書きする。Interview で参照、Reflection 後の追記に使う。
allowed-tools: file_read shell
---

# 共通教訓ノート

データ: `storage/doctor/global_lessons.json`

## 読み込み

```bash
python scripts/read_global_lessons.py
```

`is_active: true` のエントリだけ JSON で返す。

## 追記

```bash
python scripts/update_global_lessons.py --rule "ルール文" [--deactivate lesson_xxx]
```

古いルールは `is_active: false` で論理削除し、新規エントリを Append-only で追加する。
