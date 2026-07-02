---
name: patient-record
description: 個別患者カルテ（patients/patient_xxx.json）に問診ログを追記する。
allowed-tools: file_read shell
---

# 患者カルテ

データ: `storage/patients/patient_xxx.json`

## 追記

```bash
python scripts/write_patient_record.py --patient patient_001 --role doctor --text "問診内容"
```

`consultation_log` に Append-only で追記する。
