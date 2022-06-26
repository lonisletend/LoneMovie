import random
import string


class RandomUtil:
    # 生成从a-zA-Z0-9的指定长度的随机字符串
    @staticmethod
    def get_random_string(length: int):
        return ''.join(random.sample(string.ascii_letters + string.digits, length))

    @staticmethod
    def get_random_captcha():
        return RandomUtil.get_random_string(4)
