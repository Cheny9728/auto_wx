from wxauto import WeChat
from openai import OpenAI
import time
from rollchat import roll
from rollchat_deep import roll_deep
from message import key, url
import tkinter as tk
from tkinter import simpledialog, messagebox
from logger import setup_logger

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("微信消息自动回复程序")
        self.root.geometry("800x800")  # 调整窗口大小以容纳日志窗口
        self.root.resizable(True, True)

        # 创建日志窗口和滚动条
        self.log_frame = tk.Frame(root)
        self.log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(self.log_frame, state='disabled')
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=self.scrollbar.set)

        # 初始化日志记录器
        self.logger = setup_logger(self.log_text)

        self.logger.info("程序主窗口创建完成")

        # 创建左右两个框架
        self.left_frame = tk.Frame(root, width=400, height=600)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.logger.info("左框架创建完成")

        self.right_frame = tk.Frame(root, width=400, height=600)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.logger.info("右框架创建完成")

        # 系统风格和语气输入（左框架）
        self.system_style_label = tk.Label(self.left_frame, text="请输入系统风格和语气：")
        self.system_style_label.pack(pady=10)
        self.system_style_entry = tk.Entry(self.left_frame, width=50)
        self.system_style_entry.pack(pady=5)
        self.logger.info("系统风格和语气输入框创建完成")

        # 是否使用默认选框（左框架）
        self.use_default_var = tk.IntVar()
        self.use_default_checkbox = tk.Checkbutton(self.left_frame, text="是否使用默认", variable=self.use_default_var,
                                                   command=self.update_system_style)
        self.use_default_checkbox.pack(pady=5)
        self.logger.info("是否使用默认选框创建完成")

        # 系统风格和语气保存按钮（左框架）
        self.system_style_save_button = tk.Button(self.left_frame, text="保存", command=self.save_system_style)
        self.system_style_save_button.pack(pady=10)
        self.logger.info("系统风格和语气保存按钮创建完成")

        # 深度思考回复选项（左框架）
        self.deep_thinking_var = tk.IntVar()
        self.deep_thinking_checkbox = tk.Checkbutton(self.left_frame, text="使用深度思考回复", variable=self.deep_thinking_var)
        self.deep_thinking_checkbox.pack(pady=10)
        self.logger.info("深度思考回复选项复选框创建完成")

        # 监听目标输入（右框架）
        self.listen_targets_label = tk.Label(self.right_frame, text="请输入要监听的好友或群名称：")
        self.listen_targets_label.pack(pady=10)
        self.entry_list = []
        self.entry_frame = tk.Frame(self.right_frame)
        self.entry_frame.pack(pady=5, fill=tk.X, expand=True)
        for _ in range(2):
            entry = tk.Entry(self.entry_frame)
            entry.pack(pady=2, fill=tk.X, expand=True)
            self.entry_list.append(entry)
        self.add_button = tk.Button(self.right_frame, text="添加", command=self.add_entry)
        self.add_button.pack(pady=5)
        self.logger.info("监听目标输入框及添加按钮创建完成")

        # 监听目标保存按钮（右框架）
        self.listen_targets_save_button = tk.Button(self.right_frame, text="保存", command=self.save_listen_targets)
        self.listen_targets_save_button.pack(pady=10)
        self.logger.info("监听目标保存按钮创建完成")

        # 按钮框架
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.BOTTOM, pady=20)

        # 开始按钮
        self.start_button = tk.Button(self.button_frame, text="开始", command=self.start_program, bg="green")
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.logger.info("开始按钮创建完成")

        # 暂停按钮
        self.pause_button = tk.Button(self.button_frame, text="暂停", command=self.pause_program, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.logger.info("暂停按钮创建完成")

        # 重置按钮
        self.reset_button = tk.Button(self.button_frame, text="重置", command=self.reset_program, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        self.logger.info("重置按钮创建完成")

        self.is_running = False
        self.is_paused = False

    def add_entry(self):
        new_entry = tk.Entry(self.entry_frame)
        new_entry.pack(pady=2, fill=tk.X, expand=True)
        self.entry_list.append(new_entry)
        self.logger.info("用户成功添加一个新的输入框")

    def update_system_style(self):
        if self.use_default_var.get() == 1:
            default_content = "你是一个社会经历丰富的人，充满情绪价值的，针对对方的话，能提供完美的情绪价值，不能太调皮，但也不要失去风格，针对对方的话回复的内容在 20 字以内"
            self.system_style_entry.delete(0, tk.END)
            self.system_style_entry.insert(0, default_content)
            self.logger.info("已使用默认系统风格和语气填充输入框")
        else:
            self.system_style_entry.delete(0, tk.END)
            self.logger.info("已清空系统风格和语气输入框")

    def save_system_style(self):
        self.logger.info("用户点击了系统风格和语气保存按钮，开始保存操作")
        if self.use_default_var.get() == 1:
            content = "你是一个社会经历丰富的人，充满情绪价值的，针对对方的话，能提供完美的情绪价值，不能太调皮，但也不要失去风格，针对对方的话回复的内容在 20 字以内"
            self.logger.info("用户选择使用默认系统风格和语气，已保存默认内容")
        else:
            content = self.system_style_entry.get()
            self.logger.info(f"用户输入自定义系统风格和语气，已保存内容: {content}")

    def save_listen_targets(self):
        self.logger.info("用户点击了监听目标保存按钮，开始保存操作")
        targets = []
        for entry in self.entry_list:
            text = entry.get().strip()
            if text:
                targets.append(text)
        self.logger.info(f"成功保存监听目标: {', '.join(targets) if targets else '无有效目标'}")

    def start_program(self):
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.logger.info("用户点击开始按钮，程序正式启动")

        # 获取系统风格和语气
        if self.use_default_var.get() == 1:
            content = "你是一个社会经历丰富的人，充满情绪价值的，针对对方的话，能提供完美的情绪价值，不能太调皮，但也不要失去风格，针对对方的话回复的内容在 20 字以内"
            self.logger.info("使用默认系统风格和语气启动程序")
        else:
            content = self.system_style_entry.get()
            self.logger.info(f"使用自定义系统风格和语气启动程序: {content}")
        messages = [
            {"role": "system",
             "content": content}
        ]

        # 获取监听目标
        targets = []
        for entry in self.entry_list:
            text = entry.get().strip()
            if text:
                targets.append(text)
        self.logger.info("开始验证监听目标的有效性")
        wx = WeChat()
        found_targets = []
        for target in targets:
            try:
                wx.ChatWith(target)
                found_targets.append(target)
                self.logger.info(f"成功验证监听目标: {target}")
            except Exception:
                self.logger.warning(f"未找到监听目标: {target}")
        if len(found_targets) != len(targets):
            not_found = [t for t in targets if t not in found_targets]
            messagebox.showerror("错误", f"未找到以下目标: {', '.join(not_found)}，请重新输入。")
            self.logger.error(f"部分监听目标未找到: {', '.join(not_found)}，程序启动流程暂停")
            self.reset_program()
            return
        self.logger.info(f"所有监听目标验证通过: {', '.join(found_targets)}")

        # 初始化 OpenAI 客户端
        self.logger.info("开始初始化 OpenAI 客户端")
        client = OpenAI(api_key=key, base_url=url)
        self.logger.info("OpenAI 客户端初始化成功")

        # 循环添加监听对象
        self.logger.info("开始循环添加监听对象")
        for i in found_targets:
            wx.AddListenChat(who=i, savepic=True)
            self.logger.info(f"已添加监听对象：{i}")

        # 处理消息回复
        self.logger.info("开始处理消息回复流程")
        self.handle_messages(wx, client, messages, found_targets)

    def pause_program(self):
        if self.is_running:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_button.config(text="继续")
                self.logger.info("程序已暂停")
            else:
                self.pause_button.config(text="暂停")
                self.logger.info("程序已继续")

    def reset_program(self):
        self.is_running = False
        self.is_paused = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.system_style_entry.delete(0, tk.END)
        self.use_default_var.set(0)
        self.deep_thinking_var.set(0)
        for entry in self.entry_list:
            entry.delete(0, tk.END)
        self.logger.info("程序已重置")

    def handle_messages(self, wx, client, messages, listen_list):
        self.logger.info("消息处理循环正式开启")
        wait = 1
        while self.is_running:
            if not self.is_paused:
                try:
                    self.logger.info("开始获取微信消息")
                    msgs = wx.GetListenMessage()
                    self.logger.info(f"成功获取到 {len(msgs)} 条微信消息")
                    for chat in msgs:
                        who = chat.who
                        if who in listen_list:
                            one_msgs = msgs.get(chat)
                            for msg in one_msgs:
                                msgtype = msg.type
                                content = msg.content
                                self.logger.info(f"收到来自【{who}】的消息: {content}")
                                if msgtype == 'friend':
                                    try:
                                        if self.deep_thinking_var.get() == 1:
                                            self.logger.info(f"针对【{who}】的消息，使用深度思考模式进行回复")
                                            response = roll_deep(client, messages, content)
                                            # 假设 roll_deep 可能返回元组，取最后一个元素作为最终结果
                                            if isinstance(response, tuple):
                                                response = response[-1]
                                            chat.SendMsg(response)
                                            self.logger.info(f"已向【{who}】发送深度思考回复消息: {response}")
                                        else:
                                            self.logger.info(f"针对【{who}】的消息，使用普通模式进行回复")
                                            response = roll(client, messages, content)
                                            # 假设 roll 可能返回元组，取最后一个元素作为最终结果
                                            if isinstance(response, tuple):
                                                response = response[-1]
                                            chat.SendMsg(response)
                                            self.logger.info(f"已向【{who}】发送普通回复消息: {response}")
                                    except Exception as e:
                                        self.logger.error(f"回复【{who}】的消息时出错: {e}")
                except Exception as e:
                    self.logger.error(f"获取微信消息时出错: {e}")
            time.sleep(wait)
        self.logger.info("消息处理循环已停止")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()