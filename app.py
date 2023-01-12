# -*- coding: utf-8 -*-
from pywebio.input import *
from pywebio.output import *
from pywebio import platform
from pywebio.pin import *
from pywebio.session import *
from pywebio import config
# 随机数模块
import requests
from random import sample

from flask import Flask, request

app = Flask(__name__)



 
 

config(title='随机数生成',
description='陈老师专用的随机数生成器',
theme='minty'
)
@app.route('/')
def main():
    # 更改网页的favico
    image_url="https://cdn.xhhdd.cc/uPic2/dxMSIl.jpeg"
    run_js("""
    $('#favicon32,#favicon16').remove(); 
    $('head').append('<link rel="icon" type="image/png" href="%s">')
    """ % image_url)
    # 一言接口
    def yiyan():
        url='https://v1.hitokoto.cn?c=j&c=l&c=d'
        response = requests.post(url)
        content=response.json()['hitokoto']
        with use_scope('yiyan',clear=True):
            put_markdown(r""" *%s*
            """%content)
        return
    yiyan()
    # 网页的标题以及介绍
    def title():
        with use_scope('title'):
            put_markdown(r""" # 陈老师上课专用
            1. 填入最小值、最大值
            2. 选择抽取数量
            3. 生成！
            """)
        return
    title()

    # 随机数输入界面
    def random_input():
        # 校验函数
        def check_number(data):
            if data['max']<data['min']:
                return ('min','最小值超过最大值了！')
            if data['num']>100:
                return ('num','拜托，我算不出来了啦！')
            if data['num']>(data['max']-data['min']+1):
                return ('num','拜托，数字填大啦！')
        with use_scope('input',clear=True):
            data=input_group("生成准备",[
                input('最小值', name='min', type=NUMBER,value=1,required=True),
                input('最大值', name='max', type=NUMBER,required=True),
                input('抽取数量', name='num', type=NUMBER,value=1,required=True,help_text='又会抽到几个幸运鹅呢？'),
            ],validate=check_number)
        return data

    # 调用输入界面
    data=random_input()
    data_b=data.copy() # 保存数据

    # 随机数实现
    def random(data:dict):
        yiyan()
        min_max=[x for x in range(data['min'],data['max']+1)]
        result_l=sample(min_max,data['num'])
        return result_l

    # 调用随机数生成
    result_l=random(data_b)

    # 进行输出
    def put_demo(result_l):
        with use_scope('demo',clear=True):
            put_markdown(r""" ## 生成结果如下
            """)
            result_l.insert(0,'学号')
            put_table(
                [result_l],
                header=[span('左右滑动查看更多',col=len(result_l))]
            )
    put_demo(result_l)

    config_l=[data_b]
    # 重新生成的功能
    def re_create(mode):
        yiyan()
        if mode=='random':
            re_data=config_l[0]
        if mode=='re_content':
            config_l[0]=random_input()
            re_data=config_l[0]
        # 展示
        put_demo(random(re_data))
        return
    # 重新生成
    with use_scope('re_creat'):
        put_markdown(r'''## 生成结果不满意？
        ''')
        put_row(
        [put_button('重新抽取',onclick=lambda : re_create('random'),color='primary'),
        put_button('重新填写参数',onclick=lambda : re_create('re_content'),color='secondary')]
        )
if __name__ == '__main__':
    platform.start_server(main,port=5051,debug=True)

