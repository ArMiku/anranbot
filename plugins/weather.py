from nonebot import on_command, CommandSession
import requests
import json
import re
import time
import datetime

# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    # 获取城市的天气预报
    weather_report = await get_weather_of_city(city)
    # 向用户发送天气预报
    await session.send(weather_report)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg

# 获取星期几
def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]

async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    # 文件下载地址
    Download_addres = 'http://wthrcdn.etouch.cn/weather_mini?city=' + city
    # 把下载地址发送给requests模块
    f = requests.get(Download_addres)
    # 下载文件(原文保存)
    with open("weather", "wb") as code:
        code.write(f.content)
    dataJson = json.load(open('weather', encoding='UTF-8'))  # 读取天气文件

    # 提取天气相关信息
    date = dataJson['data']['forecast'][0]['date']  # 读取日期
    tianqi = dataJson['data']['forecast'][0]['type']  # 读取天气
    low = dataJson['data']['forecast'][0]['low']  # 读取最低气温
    high = dataJson['data']['forecast'][0]['high']  # 读取最高气温
    fengxiang = dataJson['data']['forecast'][0]['fengxiang']  # 读取风向
    fengli = dataJson['data']['forecast'][0]['fengli']  # 读取风力
    c = city + ': '+tianqi  # 城市天气给变量C
    d = '气温: '+low[3:-1]+'-'+high[3:-1]+'℃'  # 气温给变量d
    e = '风力: '+re.findall('.*CDATA\[(.*)]]', fengli)[0]  # 风力给变量e
    f = '风向: ' + fengxiang  # 风向给变量f
    # print(time.strftime('%Y年%m月%d日', time.localtime(time.time())) +
    #   get_week_day(datetime.datetime.now()))
    # print(c)  # 显示城市天气
    # print(d)  # 显示气温
    # print(e)  # 显示风力
    # print(f)  # 显示风向
    message = date + '\n' + c + '\n' + d + '\n' + e + '\n' + f
    return message
