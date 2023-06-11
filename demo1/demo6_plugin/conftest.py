from typing import Optional, List

import pytest
import yaml


def pytest_runtest_setup(item: "Item") -> None:
    print("hook:setup")


def pytest_runtest_teardown(item: "Item", nextitem: Optional["Item"]) -> None:
    print("teardwn")


# 收集完测试用例 之后被调用的hook函数
def pytest_collection_modifyitems(session: "Session", config: "Config", items: List["Item"]
                                  ) -> None:
    print(items)
    # name 用例的名字
    # nodeid 就是测试用例路径
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
    # 修改结果的执行顺序
    items.reverse()


# 定义一个命令参数
def pytest_addoption(parser):
    mygroup = parser.getgroup("hogwarts")  # group 将下面所有的option都展示在这个group下
    mygroup.addoption("--env",  # 注册一个命令行选项
                      default='test',  # 参数的默认值
                      dest='env',  # 存储的变量，为属性命令，可以使用Option对象访问到这个值，咱用不到
                      help='set your run env'  # 帮助提示 参数的描述信息
                      )


# # 如何针对传入的不同参数完成不同的逻辑处理
# @pytest.fixture(scope="session")
# def cmdoption(request):
#     result = request.config.getoption("--env")
#     return result
# 如何针对传入的不同参数完成不同的逻辑处理
@pytest.fixture(scope="session")
def cmdoption(request):
    myenv = request.config.getoption("--env", default='test')
    if myenv == 'test':
        datapath = "datas/test/data.yml"
    elif myenv == 'dev':
        datapath = "datas/dev/data.yml"

    with open(datapath) as f:
        datas = yaml.safe_load(f)
        return myenv, datas

# # 如何针对传入的不同参数完成不同的逻辑处理
# @pytest.fixture(scope="session")
# def cmdoption(request):
#     return request.config.getoption("--env")
