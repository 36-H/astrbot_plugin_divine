import os
import random

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.message.components import At, Plain, Image

folder_path = 'data/plugins/astrbot_plugin_divine/tarot'


@register("divine", "Helios", "占卜插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 验证目标路径是否为目录
        if not os.path.isdir(folder_path):
            logger.error(f"{folder_path} 不是一个有效的文件夹")
        # 获取目录下所有文件
        all_files = os.listdir(folder_path)

        # 过滤出GIF文件（不区分大小写）
        gif_files = [f for f in all_files if f.lower().endswith('.gif')]

        if not gif_files:
            logger.error(f"在 {folder_path} 中未找到GIF文件")

        self.gif_files = gif_files



    # 注册指令的装饰器。指令名为 占卜。
    @filter.command("占卜")
    async def divine(self, event: AstrMessageEvent):
        ''' 占卜 '''  # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        # 随机选择一个GIF文件
        selected_gif = random.choice(self.gif_files)
        logger.info(f"占卜结果：{selected_gif}")
        # 构建完整路径
        full_path = os.path.join(folder_path, selected_gif)
        logger.info(f"占卜结果路径：{full_path}")
        # 二次验证文件存在性

        if not os.path.isfile(full_path):
            yield event.plain_result("出错哩！占卜图片缺失......")
        else:
            chain = [
                At(qq=event.get_sender_id()),  # At 消息发送者
                Plain("占卜结果如下："),
                Image.fromFileSystem(folder_path),  # 从本地文件目录发送图片
            ]
            yield event.chain_result(chain)
