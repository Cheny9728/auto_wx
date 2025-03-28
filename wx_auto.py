# 这个是运行的主要界面，运行速度可能很慢，请细心等待，至于什么原因，可以自己再找资料，这只提供最简单的实现
# 主播也是没怎么学python，如果有需要改进或交流，请加wx：wlxdr1234567

from wxauto import WeChat
from openai import OpenAI
import time
from rollchat import roll
from rollchat_deep import roll_deep
from message import key,url

def main():
    client = OpenAI(api_key=key, base_url=url)
    
    # content中的内容，可以随意修改，也可以不写，就是给它一个AI对话的人物设定，下面提供一个比较有意思的content
    # 你是一个暴躁老表，回答问题非常尖锐
    messages=[
            {"role": "system", "content": "你是一个社会经历丰富的人，充满情绪价值的，针对对方的话，能提供完美的情绪价值，不能太调皮，但也不要失去风格，针对对方的话，内容在20字以内"} #设置系统风格和语气
        ]

    # 获取微信窗口对象
    wx = WeChat()
    # 成功之后输出 > 初始化成功，获取到已登录窗口：xxxx

    # 设置监听列表，下面是你要监听的微信好友，把他们的备注复制粘贴到下面的'listen_list'即可，可以随意增加或者减少
    listen_list = [
        #'Rise Before',
        #'DeeSpeek自动回复测试'
        #'海装-邱虎'
        '龙永义17784727708'

    ]

    # 循环添加监听对象
    for i in listen_list:
        wx.AddListenChat(who=i, savepic=True)
    # 持续监听消息，并且收到消息后回复“收到”
    wait = 1  # 设置1秒查看一次是否有新消息
    i = 1
    while True:
        msgs = wx.GetListenMessage()
        for chat in msgs:
            who = chat.who  # 获取聊天窗口名（人或群名）
            one_msgs = msgs.get(chat)  # 获取消息内容
            # 回复收到
            for msg in one_msgs:
                msgtype = msg.type  # 获取消息类型
                content = msg.content  # 获取消息内容，字符串类型的消息内容
                print(f'【{who}】：{content}')
                if msgtype == 'friend': #下面选择用DeepSeek的深度思考和普通对话
                    #chat.SendMsg(roll_deep(client, messages, content))  # 深度思考
                    chat.SendMsg(roll(client, messages, content))       # 普通对话
        time.sleep(wait)
if __name__ == "__main__":
    main()