from nonebot import on_command, CommandSession

# on_command 装饰器将函数声明为一个命令处理器
@on_command('music', aliases=('点歌'))
async def weather(session: CommandSession):
    # 从会话状态（session.state）中获取歌曲名称（name），如果当前不存在，则建议用户输入其他的
    name = session.get('name', prompt='目前还查不到此歌，请换一首')
    # 获取
    music_report = await get_music_of_name(name)
    # 向用户发送
    await session.send(music_report)