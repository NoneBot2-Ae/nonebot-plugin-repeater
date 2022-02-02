from nonebot import get_driver, on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.permission import PRIVATE_FRIEND, GROUP_ADMIN
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent, GroupMessageEvent

from .config import Config

global_config = get_driver().config
config: Config = Config.parse_obj(global_config.dict())

reply_group_dict = {}
reply_dict = {'?': '?', '？': '？'}
reply = on_message(priority=100)


@reply.handle()
async def reply_handle(bot: Bot, event: Event):
    if isinstance(
            event,
            GroupMessageEvent) and event.group_id not in config.enable_groups:
        return

    user_msg = str(event.get_message()).strip()
    try:
        reply_msg = reply_dict[user_msg]
        await reply.finish(reply_msg)
    except KeyError:
        await reply.finish()


#查看关键词
check_kw = on_command('re-check',
                      priority=50,
                      permission=SUPERUSER | PRIVATE_FRIEND)


@check_kw.handle()
async def check_kw_handle(bot: Bot, event: Event):
    reply_msg_list = ['关键词为：']
    for k, v in reply_dict.items():
        reply_msg_list.append(f'{k} => {v}')
    reply_msg = '\n'.join(reply_msg_list)
    await check_kw.finish(reply_msg)


#增加关键词
add_kw = on_command('re-add',
                    priority=50,
                    permission=SUPERUSER | PRIVATE_FRIEND)


@add_kw.handle()
async def add_kw_handle(bot: Bot, event: Event):
    user_msg = str(event.get_message()).replace('/add', '').strip()
    keyword, replyword = user_msg.split('=>')
    reply_dict[keyword] = replyword
    await add_kw.finish(f'已经更改 {keyword} => {replyword}')


#删除关键词
del_kw = on_command('re-del',
                    priority=50,
                    permission=SUPERUSER | PRIVATE_FRIEND)


@del_kw.handle()
async def del_kw_handle(bot: Bot, event: Event):
    keyword = str(event.get_message()).replace('/del', '').strip()
    try:
        replyword = reply_dict[keyword]
        del reply_dict[keyword]
        await del_kw.finish(f'已删除 {keyword} => {replyword}')
    except KeyError:
        await del_kw.finish(f'不存在关键字 {keyword}')
