import requests
import base64
import os, json
from picEval.models import ImageTaskInfo, ResultInfo


# ocr接口：http://10.143.52.35:10098/v4/ocr/json
# 参数：lang，image=base64串
# 英文：en
# 中文：zh-CHS
# 日文：ja
# 韩文：ko
# 俄文：ru
# 法文：fr
# 西班牙文：es
# 德文：de
# 葡萄牙：pt
# 意大利：it

# 翻译回帖接口：http://api.image.sogou/v1/open/ocr_translate.json
# 参数：from、to、image、result_type=image

def imageTobase64(path):
    with open(path, 'rb') as f:
        image = base64.b64encode(f.read())
        image = image.decode('utf-8')
        return image


def post_ocr(test_ocrip, base_ocrip, test_imgip, base_imgip, from_langs, to_langs):
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    pic_path = r'/Users/apple/AnacondaProjects/demo_pro/image/'
    sum_num = len(os.listdir(pic_path))
    for filename in os.listdir(pic_path):
        base64image = imageTobase64(pic_path + filename)
        params_ocr = {
            'lang': from_langs,
            'image': base64image,
        }
        resp_test = requests.post(test_ocrip, data=params_ocr, headers=headers)
        resp_base = requests.post(base_ocrip, data=params_ocr, headers=headers)

        post_image(from_langs, to_langs, base64image, test_imgip, filename, 'test')
        post_image(from_langs, to_langs, base64image, base_imgip, filename, 'base')

        result_test = resp_test.json()
        result_base = resp_base.json()

        distance(result_test, result_base)

        # y = x['result']
        # for i in y:
        #     for k, v in i.items():
        #         print('k',k)
        #         print('v',v)

        # y = xx['result']['content']
        # print(y)
        # z=json.loads(y.join())
        # print(z['content'])
        # # print(json.dumps(x['result']))

    return sum_num


def post_image(from_langs, to_langs, base64image, url, filename, type):
    # module_path = os.path.dirname(__file__)
    # print(module_path)
    # pic_path = r'/Users/apple/AnacondaProjects/demo_pro/image/'
    # sum_num = len(os.listdir(pic_path))
    # for filename in os.listdir(pic_path):
    #     image_base64 = imageTobase64(pic_path + filename)
    #     print(image_base64)
    # headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary0COmad6TmBUZmkWm"}

    params_img = {
        'from': from_langs,
        'to': to_langs,
        'image': base64image,
        'result_type': 'image'
    }
    # resp = requests.post('http://api.image.sogou/v1/open/ocr_translate.json', data=params_img)
    resp = requests.post(url, data=params_img)
    result = resp.json()
    print("image", result)
    pic = result['pic']
    pic = base64.b64decode(pic)
    result_path = '/Users/apple/AnacondaProjects/demo_pro/result/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
        filename = filename[:-4]
        if type == 'test':
            file = open(result_path + filename + '_test.jpg', 'wb')
            file.write(pic)
            file.close()
        elif type == 'base':
            file = open(result_path + filename + '_base.jpg', 'wb')
            file.write(pic)
            file.close()
        else:
            print('回帖图请求类型未知！')
    return result


def distance(result_test, result_base):
    x = 1
    y = 2
    return x, y


if __name__ == '__main__':
    # post_ocr('http://api.image.sogou/v1/ocr/basic.json', 'http://api.image.sogou/v1/ocr/basic.json', 'zh-CHS')
    # post_image('en', 'zh-CHS', base64, filename, url, type)
    pass