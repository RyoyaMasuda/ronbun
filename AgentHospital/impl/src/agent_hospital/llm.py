"""LLM プロバイダ設定（Azure OpenAI）。

環境変数（.env 可）:
    AZURE_OPENAI_ENDPOINT  … https://YOUR_RESOURCE.openai.azure.com
    AZURE_OPENAI_API_KEY
    AZURE_OPENAI_DEPLOYMENT … デプロイ名（モデル ID として使用）
    AZURE_OPENAI_API_VERSION … 省略時 2024-08-01-preview（legacy URL 形式時）
"""

import os

from strands.models.openai import OpenAIModel


def create_llm_model() -> OpenAIModel:
    """Azure OpenAI 用 OpenAIModel を生成する。

    Returns:
        Interview / Patient ノードで共有する OpenAIModel。

    Raises:
        KeyError: 必須環境変数が未設定の場合。
    """
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

    # Azure OpenAI v1 エンドポイント（openai>=1.0）
    # https://learn.microsoft.com/azure/ai-services/openai/how-to/switching-endpoints
    use_legacy = os.environ.get("AZURE_OPENAI_LEGACY_URL", "").lower() in ("1", "true", "yes")
    if use_legacy:
        client_args = {
            "api_key": api_key,
            "base_url": f"{endpoint}/openai/deployments/{deployment}",
            "default_query": {"api-version": api_version},
        }
    else:
        client_args = {
            "api_key": api_key,
            "base_url": f"{endpoint}/openai/v1/",
        }

    return OpenAIModel(client_args=client_args, model_id=deployment)
