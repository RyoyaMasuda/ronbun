#!/usr/bin/env python3
"""症例マスタ JSON（patient_001〜020）と manifest.json を生成する。"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATIENTS_DIR = ROOT / "storage" / "patients"

CASES: list[dict] = [
    {
        "patient_id": "patient_001",
        "split": "train",
        "chief_complaint": "左胸に帯状の水ぶくれと痛み",
        "history": "2日前から発熱。小児期に水痘の既往あり。痛みは触ると増強する。",
        "exam_results": {"skin_findings": "左前胸部に帯状分布の水疱"},
        "ground_truth": "帯状疱疹",
    },
    {
        "patient_id": "patient_002",
        "split": "train",
        "chief_complaint": "高熱と全身の筋肉痛",
        "history": "3日前から38.5度前後の発熱。頭痛と関節痛あり。冬場に同僚がインフルと診断された。",
        "exam_results": {"throat": "咽頭軽度発赤", "lung": "呼吸音清"},
        "ground_truth": "インフルエンザ",
    },
    {
        "patient_id": "patient_003",
        "split": "train",
        "chief_complaint": "右下腹部の強い痛み",
        "history": "12時間前から臍周囲の痛みが始まり、現在は右下腹部に固定。吐き気あり、食欲低下。",
        "exam_results": {"abdomen": "右下腹部の圧痛と反跳痛", "lab": "WBC 14000"},
        "ground_truth": "急性虫垂炎",
    },
    {
        "patient_id": "patient_004",
        "split": "train",
        "chief_complaint": "右側頭部の拍動性頭痛",
        "history": "4時間前から徐々に増悪。光や音で悪化。前兆なし。月1回程度の類似発作歴。",
        "exam_results": {"neuro": "神経学的異常なし", "vitals": "BP 118/76"},
        "ground_truth": "片頭痛",
    },
    {
        "patient_id": "patient_005",
        "split": "train",
        "chief_complaint": "胸やけと夜間の咳",
        "history": "食後や就寝時に胸焼け。2週間前から寝返りで咳が出る。喫煙なし。",
        "exam_results": {"chest": "胸部聴診異常なし", "abdomen": "上腹部軽圧痛"},
        "ground_truth": "胃食道逆流症",
    },
    {
        "patient_id": "patient_006",
        "split": "train",
        "chief_complaint": "排尿時痛と残尿感",
        "history": "1日前から頻尿と排尿時灼熱感。発熱は37.2度程度。腰痛なし。",
        "exam_results": {"urinalysis": "白血球陽性、亀頭部圧痛なし", "abdomen": "下腹部軽圧痛"},
        "ground_truth": "急性膀胱炎",
    },
    {
        "patient_id": "patient_007",
        "split": "train",
        "chief_complaint": "突然の左胸痛と息苦しさ",
        "history": "瘦せ型。本日急に左側胸痛と呼吸困難。咳嗽なし。外傷なし。",
        "exam_results": {"lung": "左呼吸音減弱", "vitals": "SpO2 94% 室内気"},
        "ground_truth": "自然気胸",
    },
    {
        "patient_id": "patient_008",
        "split": "train",
        "chief_complaint": "喉の渇きと体重減少",
        "history": "1か月で3kg減少。多飲多尿。以前健康診断で血糖高値を指摘されたが未受診。",
        "exam_results": {"lab": "空腹時血糖 286 mg/dL", "urinalysis": "尿糖+++"},
        "ground_truth": "2型糖尿病",
    },
    {
        "patient_id": "patient_009",
        "split": "train",
        "chief_complaint": "動悸と息切れ",
        "history": "2週間前から階段上りで息切れ。月経量多い。偏食気味。",
        "exam_results": {"lab": "Hb 9.2 g/dL, MCV 72", "conjunctiva": "結膜蒼白"},
        "ground_truth": "鉄欠乏性貧血",
    },
    {
        "patient_id": "patient_010",
        "split": "train",
        "chief_complaint": "突然の胸骨後部痛",
        "history": "60代男性。30分前から持続する重い胸痛。冷汗あり。喫煙歴20年。",
        "exam_results": {"ecg": "ST上昇", "vitals": "BP 90/60, 頻脈"},
        "ground_truth": "急性心筋梗塞",
    },
    {
        "patient_id": "patient_011",
        "split": "train",
        "chief_complaint": "咳と痰、発熱",
        "history": "5日前から咳が増加。黄色痰。38度の発熱。高齢だが自立。",
        "exam_results": {"lung": "右下肺野でラ音", "lab": "CRP 8.2"},
        "ground_truth": "市中肺炎",
    },
    {
        "patient_id": "patient_012",
        "split": "train",
        "chief_complaint": "上腹部痛と吐き気",
        "history": "昨日から飲酒後に上腹部痛。今日朝に2回嘔吐。下痢なし。",
        "exam_results": {"abdomen": "上腹部圧痛、反跳痛軽度", "lab": "アミラーゼ正常"},
        "ground_truth": "急性胃炎",
    },
    {
        "patient_id": "patient_013",
        "split": "train",
        "chief_complaint": "手足のしびれと呼吸が深くなる",
        "history": "試験前のストレス後に発症。過呼吸感。胸痛なし。",
        "exam_results": {"vitals": "呼吸数 24/分", "lab": "ABG 軽度呼吸性アルカローシス"},
        "ground_truth": "過換気症候群",
    },
    {
        "patient_id": "patient_014",
        "split": "train",
        "chief_complaint": "右腰背部の激痛",
        "history": "突然の疝痛様腰痛。血尿あり。嘔吐1回。発熱なし。",
        "exam_results": {"abdomen": "右側腹部叩打痛", "urinalysis": "血尿+++"},
        "ground_truth": "尿管結石",
    },
    {
        "patient_id": "patient_015",
        "split": "train",
        "chief_complaint": "動悸、汗、体重減少",
        "history": "1か月で4kg減。手の震え。イライラしやすい。",
        "exam_results": {"thyroid": "甲状腺腫大、頻脈", "lab": "FT3/FT4 高値"},
        "ground_truth": "甲状腺機能亢進症",
    },
    {
        "patient_id": "patient_016",
        "split": "test",
        "chief_complaint": "発疹と発熱",
        "history": "3日前から38度前後。今日から顔から体に赤い発疹。予防接種未接種の情報あり。",
        "exam_results": {"skin": "顔面から体幹へ向かう紅斑性発疹", "oral": "口内コプラジック斑疑い"},
        "ground_truth": "麻疹",
    },
    {
        "patient_id": "patient_017",
        "split": "test",
        "chief_complaint": "右肘外側の痛み",
        "history": "2週間前からテニス再開。肘外側が握力で痛む。しびれなし。",
        "exam_results": {"elbow": "橈骨外側上顆圧痛", "neuro": "橈骨神経領域異常なし"},
        "ground_truth": "外側上顆炎",
    },
    {
        "patient_id": "patient_018",
        "split": "test",
        "chief_complaint": "息切れと足のむくみ",
        "history": "2週間前から平地歩行で息切れ。夜間起座呼吸。高血圧治療中。",
        "exam_results": {"lung": "両肺底ラ音", "leg": "両下腿浮腫", "vitals": "BP 150/92"},
        "ground_truth": "心不全",
    },
    {
        "patient_id": "patient_019",
        "split": "test",
        "chief_complaint": "顔面痛と鼻づまり",
        "history": "10日前から感冒様症状後、右頬部痛と膿性鼻汁。歯痛様の痛みあり。",
        "exam_results": {"sinus": "右頬部圧痛", "nasal": "右側膿性鼻汁"},
        "ground_truth": "急性副鼻腔炎",
    },
    {
        "patient_id": "patient_020",
        "split": "test",
        "chief_complaint": "突然の呼吸困難と胸痛",
        "history": "長時間のデスクワーク。1週間前から左下腿腫脹。本日突然の胸痛。",
        "exam_results": {"vitals": "SpO2 91%", "leg": "左下腿腫脹・圧痛", "d_dimer": "上昇"},
        "ground_truth": "肺塞栓症",
    },
]


def main() -> None:
    PATIENTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_cases = []

    for case in CASES:
        path = PATIENTS_DIR / f"{case['patient_id']}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(case, f, ensure_ascii=False, indent=2)
            f.write("\n")
        manifest_cases.append(
            {
                "patient_id": case["patient_id"],
                "split": case["split"],
                "ground_truth": case["ground_truth"],
            }
        )

    manifest = {
        "version": 1,
        "train_count": sum(1 for c in CASES if c["split"] == "train"),
        "test_count": sum(1 for c in CASES if c["split"] == "test"),
        "cases": manifest_cases,
    }
    with (PATIENTS_DIR / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"wrote {len(CASES)} cases to {PATIENTS_DIR}")


if __name__ == "__main__":
    main()
