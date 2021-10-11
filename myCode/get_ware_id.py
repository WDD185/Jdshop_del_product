import jsonpath as jsonpath
import requests
from myCode.request_header import header, body


def trans(data):
    return str(data)


class GetWareId:
    def __init__(self):
        self.search_url = 'https://ware.shop.jd.com/rest/ware/list/search'
        self.del_url = 'https://ware.shop.jd.com/rest/ware/list/doUpdate?op=del&updateWareIds={}'

    def get_json(self):
        res = requests.post(self.search_url, json=body, headers=header)
        data = res.json()
        return data

    def get_id(self, data):
        data1 = data['data']
        data2 = data1['data']
        return list(map(trans, jsonpath.jsonpath(data2, '$..wareId')))

    def del_item(self, ware_id):
        requests.post(self.del_url.format(','.join(ware_id)), headers=header)

    def start(self):
        data = self.get_json()
        if data['data']['totalItem'] > 0:
            print('还剩{}'.format(data['data']['totalItem']))
            self.del_item(self.get_id(data))
            self.start()
        else:
            print('已完成删除')


if __name__ == '__main__':
    print(GetWareId().start())
