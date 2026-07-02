---
name: patient-record
description: 診察セッション（sessions/patient_xxx/）の dialogue に問診ログを追記する。
allowed-tools: file_read shell
---

# 患者カルテ（セッション）

データ: `storage/sessions/patient_xxx/{session_id}.json`

## 追記

```bash
python scripts/write_patient_record.py --patient patient_001 --session SESSION_ID --role doctor --text "問診内容"
```

`dialogue` に Append-only で追記する。
