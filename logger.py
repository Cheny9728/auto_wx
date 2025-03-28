import logging
import os
from datetime import datetime

class TkinterHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        try:
            self.text_widget.configure(state='normal')
            self.text_widget.insert('end', msg + '\n')
            self.text_widget.configure(state='disabled')
            # 自动滚动到最新的日志信息
            self.text_widget.see('end')
            # 强制刷新界面
            self.text_widget.update_idletasks()
        except Exception:
            self.handleError(record)

def setup_logger(text_widget=None):
    # 创建 log 文件夹
    log_dir = os.path.join(os.path.dirname(__file__), 'log')
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
            print(f"成功创建日志文件夹: {log_dir}")
        except Exception as e:
            print(f"创建日志文件夹时出错: {e}")

    # 以当前日期和时间命名日志文件
    now = datetime.now()
    log_file_name = now.strftime("%Y%m%d_%H%M%S") + ".log"
    log_file = os.path.join(log_dir, log_file_name)
    try:
        print(f"成功创建日志文件: {log_file}")
    except Exception as e:
        print(f"记录日志文件创建信息时出错: {e}")

    # 配置日志记录，将日志保存到 log 文件夹中的文件，指定编码为 UTF-8
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_file, encoding='UTF-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if text_widget:
        tkinter_handler = TkinterHandler(text_widget)
        tkinter_handler.setFormatter(formatter)
        logger.addHandler(tkinter_handler)

    return logger