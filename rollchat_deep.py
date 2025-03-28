# 这个文件的函数是DeepSeek的深度思考，对应DeepSeek-R1
from openai import OpenAI
from message import key
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

def roll_deep(client, messages, say):
    messages.append({"role": "user", "content": say})
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=True
    )

    reasoning_content = ""
    content = ""

    # 处理流式响应
    for chunk in response:
        if chunk.choices[0].delta.reasoning_content:
            reasoning_content += chunk.choices[0].delta.reasoning_content
            # print(chunk.choices[0].delta.reasoning_content, end='', flush=True)
        elif chunk.choices[0].delta.content:
            content += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end='', flush=True)
    
    print()  # 换行
    
    # 将助手的回复添加到消息历史
    messages.append({"role": "assistant", "content": content})
    return " "+content
