"""数据分析可视化 · 个人项目

W10 实验三要点：密钥采用「本地 .env + 云端 Secrets」双通道兼容写法，
同一份代码本地和云端都能跑，不需要维护两个版本。
"""

import os

import streamlit as st
from dotenv import load_dotenv

# 本地读 .env；云端没有这个文件，load_dotenv 会自动跳过，不报错
load_dotenv(override=True)

st.set_page_config(page_title="数据分析可视化 · 个人项目", page_icon="📊")


def get_key(name: str):
    """兼容写法：本地从 .env 读，云端从 Streamlit Secrets 读。"""
    value = os.getenv(name)      # ① 先试本地：.env 已被 load_dotenv 装进环境变量
    if value:
        return value
    try:
        return st.secrets[name]  # ② 再试云端：从平台 Secrets 读
    except Exception:
        return None              # ③ 两处都没有 → 返回 None，交给下面友好提示


# ---- 大模型配置：换模型/换厂商只改 Secrets 或 .env，不动代码 ----
# LLM_API_KEY 没配时，退回用 DEEPSEEK_API_KEY（兼容你之前只配了一个 key 的情况）
LLM_API_KEY = get_key("LLM_API_KEY") or get_key("DEEPSEEK_API_KEY")
LLM_BASE_URL = get_key("LLM_BASE_URL") or "https://api.deepseek.com"
LLM_MODEL = get_key("LLM_MODEL") or "deepseek-chat"

st.title("我的第一个云端应用")
st.write("这是我在数据分析课上部署的第一个 Streamlit 应用。")

years = st.slider("投资年限（年）", 1, 30, 10)
rate = st.slider("年化收益率（%）", 1, 20, 5)
result = 10000 * (1 + rate / 100) ** years
st.metric("1 万元到期本息", f"{result:,.0f} 元")

st.divider()

st.subheader("🤖 AI 点评")
st.caption("用来演示密钥双通道：本地读 .env，云端读 Secrets，代码一行都不用改。")

if LLM_API_KEY:
    if st.button("让 AI 点评一下"):
        with st.spinner("AI 正在思考…"):
            try:
                from openai import OpenAI

                client = OpenAI(
                    base_url=LLM_BASE_URL,
                    api_key=LLM_API_KEY,
                )
                completion = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[
                        {"role": "system", "content": "你是一名耐心的理财科普助手。"},
                        {
                            "role": "user",
                            "content": (
                                f"1 万元按年化 {rate}% 复利投资 {years} 年，"
                                f"到期约 {result:,.0f} 元。请用中文点评 2-3 句，"
                                "说明复利的效果，不要给出投资建议。"
                            ),
                        },
                    ],
                )
                st.write(completion.choices[0].message.content)
            except Exception as exc:
                st.error(f"调用失败：{exc}")
else:
    st.info(
        "还没有配置 API key。\n\n"
        "- 本地：把 key 填进项目里的 `.env` 文件\n"
        "- 云端：Manage app → Settings → 秘密 里填\n\n"
        "两份都不用改代码。"
    )

with st.sidebar.expander("🔧 密钥体检（部署排障用）"):
    st.write("API Key：", "已配置" if LLM_API_KEY else "❌ 缺失")
    st.write("当前模型：", f"`{LLM_MODEL}`")
    st.write("接口地址：", f"`{LLM_BASE_URL}`")
    st.caption("只显示「有没有配好」，不显示密钥本身。")
