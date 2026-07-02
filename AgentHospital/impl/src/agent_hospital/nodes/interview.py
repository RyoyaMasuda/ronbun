"""Interview（問診）ノード用 Strands Agent ファクトリ。

LLM ベースの医師エージェントを生成する。AgentSkills と file_read/shell ツールで
カルテ・教訓 Skill を参照できる。診断確定時は [DIAGNOSIS: 病名] を出力する。
"""

from strands import Agent, AgentSkills
from strands_tools import file_read, shell

from agent_hospital.config import SKILLS_ROOT


def create_interview_agent() -> Agent:
    """問診用 Strands Agent を生成する。

    Returns:
        AgentSkills プラグインと file_read/shell ツールを持つ医師 Agent。
        診断確定時は応答末尾に [DIAGNOSIS: 病名] を付けるよう system_prompt で指示。
    """
    skills_plugin = AgentSkills(skills=str(SKILLS_ROOT))
    return Agent(
        name="interview",
        system_prompt=(
            "あなたは医師エージェントです。患者への問診を行い、最終的に診断を下してください。"
            "必要なら patient-record / global-lessons の Skill を有効化してカルテ・教訓を参照してください。"
            "診断が確定したら、応答の末尾に [DIAGNOSIS: 病名] と書いてください。"
        ),
        plugins=[skills_plugin],
        tools=[file_read, shell],
    )
