
from xml.dom.minidom import parse
import testlink
import re
import os
import datetime
manual = 1  # 手动
automation = 2  # 自动
# 连接test link
url = "http://127.0.0.1:8009/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
key = "a116005d403efe3ca0a2f587a8d88657"  # 我这个key是错误的key
tlc = testlink.TestlinkAPIClient(url, key)
def readXML(path):
    #domTree = parse(r"D:\work\autolink\AutoLink\.beats\jobs\AutoLink\test\4\output.xml")
    domTree = parse(path)
    # 文档根元素
    rootNode = domTree.documentElement
    print(rootNode.nodeName)

    # 所有用例
    suites = rootNode.getElementsByTagName("suite")
    print("****开始发送结果****")
    data = {}
    case_Suite_name = suites[0].getAttribute("name")
    data['Suite_name'] = case_Suite_name
    for suite in suites:
        test_case_Suite=suite.getElementsByTagName("suite")
        #case_Suite_name=suite.getAttribute("name")
        for suite_case in test_case_Suite:
            test_case = suite_case.getElementsByTagName("suite")
            case_name=suite_case.getAttribute("name")
            data_case_list = {}
            data[case_name]=data_case_list
            for test in test_case:
                test1=test.getElementsByTagName("test")
                name_1=test.getAttribute("name")
                data_list={}
                data_case_list[name_1]=data_list
                for status in test1:
                    name = status.getAttribute("name")
                    status_list=status.getElementsByTagName("status")
                    for status in status_list:
                        status_name=status.getAttribute("status")
                        data_list[name]=status_name
                    if data_list[name]=={}:
                        del data_list[name]
                if data_case_list[name_1]=={}:
                    del data_case_list[name_1]
            if data [case_name]=={}:
                del data [case_name]

    return data


def report_test_result(path):

    data =readXML(path)
    Suite_name=data['Suite_name']
    del data['Suite_name']
    for k,v in data.items():
        PROJECTNAME=k
        a = tlc.getProjectIDByName(PROJECTNAME)
        if a==-1:
            a = tlc.getProjectIDByName(Suite_name)
        testplans = tlc.getProjectTestPlans(a)
        testplan_id = ""
        build_name=""
        for tp in testplans:
            testplan_id = tp['id']
            response = tlc.getBuildsForTestPlan(testplan_id)
            build_name = response[0]['name']
        for _,val in v.items():
            for id,st in val.items():
                num=re.findall("\d+",id)
                test_case_id=id.replace(num[0],"-"+num[0])
                status=""
                if st=="FAIL":
                    status="f"
                elif st=="PASS":
                    status="p"
                tlc.reportTCResult(testcaseexternalid=test_case_id, testplanid=testplan_id, status=status, buildname=build_name, platformname='tp')
    print("*************结果发送完成*************")
def path_iput(path):

    for parent, dirnames, filenames in os.walk(path, followlinks=True):

        path1=os.path.join(path ,dirnames[-1],"output.xml")
        if os.path.exists(path1):
            print(path1)
            return path1
        else:
            print("输入的路径不正确")


if __name__ == '__main__':
    path=path_iput(r"D:\work\autolink\AutoLink\.beats\jobs\AutoLink\智慧军营")

    report_test_result(path)