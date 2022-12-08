import io

from .scramble import generateScramble
from .visualizer import render

from nonebot.plugin import on_regex
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from nonebot.matcher import Matcher
from nonebot.params import EventMessage

scramble = on_regex(r'^\.([234567])$')

@scramble.handle()
async def _(matcher: Matcher, event: GroupMessageEvent, raw_message: Message = EventMessage()):
    message = raw_message.extract_plain_text()
    size = int(message[1])
    scramble_str = generateScramble(size)
    scramble_img = io.BytesIO()
    render(scramble_img, size, 100, scramble_str)
    await matcher.finish(scramble_str + MessageSegment.image(scramble_img))
