# 这个文件的函数是DeepSeek的普通对话，对应DeepSeek-V3
from openai import OpenAI
from message import key,url

client = OpenAI(api_key=key, base_url=url)

messages = []

def roll(client, messages, say):
    messages.append({"role": "user", "content": say})  # 加入
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    messages.append(response.choices[0].message)
    return " "+response.choices[0].message.content

