# -*- coding: utf-8 -*-
from db.redisCurd import RedisQueue
import asyncio
import random
import tkinter
from urllib import request
import cv2
from pyppeteer.launcher import launch
from retrying import retry
from platLogin.jdLogin.config import USERNAME, PASSWORD, LOGIN_URL


def retry_if_result_none(result):
    return result is None

async def get_distance():
    img = cv2.imread('./image.png', 0)
    template = cv2.imread('./template.png', 0)
    res = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
    value = cv2.minMaxLoc(res)[2][0]
    distance = value * 278 / 360
    return distance

# todo 重试
@retry(retry_on_result=retry_if_result_none)
async def mouse_slide(page):
    image_src = await page.Jeval('.JDJRV-bigimg >img', 'el => el.src')
    request.urlretrieve(image_src, './image.png')
    template_src = await page.Jeval('.JDJRV-smallimg >img', 'el => el.src')
    request.urlretrieve(template_src, './template.png')
    await page.waitFor(3000)
    el = await page.J('div.JDJRV-slide-btn')
    box = await el.boundingBox()
    await page.hover('div.JDJRV-slide-btn')
    distance = await get_distance()
    await page.mouse.down()
    await page.mouse.move(box['x'] + distance + random.uniform(30, 33), box['y'], {'steps': 30})
    await page.waitFor(random.randint(300, 700))
    await page.mouse.move(box['x'] + distance + 29, box['y'], {'steps': 30})
    await page.mouse.up()
    await page.waitFor(3000)


class JDLogin():
    def __init__(self, shopId):
        self.shopId = shopId
        self.jdRedisQueue = RedisQueue("jd_cookie")

    def screen_size(self):
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        tk.quit()
        return {'width': width, 'height': height}

    # 滑块的缺口距离识别
    async def get_distance(self):
        img = cv2.imread('./image.png', 0)
        template = cv2.imread('./template.png', 0)
        res = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
        value = cv2.minMaxLoc(res)[2][0]
        distance = value * 278 / 360
        return distance

    async def login(self, username, password, url):
        browser = await launch(
            {
                'headless': False,
                'dumpio': True
            },
            args=['--no-sandbox', '--disable-infobars', '--user-data-dir=./userData'],
        )
        page = await browser.newPage()  # 启动新的浏览器页面

        try:
            await page.setViewport(viewport=self.screen_size())
            await page.setJavaScriptEnabled(enabled=True)  # 启用js
            await page.setUserAgent(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
            )
            await self.page_evaluate(page)
            await page.goto(url)
            await asyncio.sleep(2)

            await page.click('.login-tab-r > a')
            await asyncio.sleep(1)
            # 输入用户名，密码
            await page.evaluate(f'document.querySelector("#loginname").value=""')
            await page.type('#loginname', username, {'delay': self.input_time_random() - 50})  # delay是限制输入的时间
            await page.evaluate('document.querySelector("#nloginpwd").value=""')

            await page.type('#nloginpwd', password, {'delay': self.input_time_random()})
            await page.waitFor(6000)
            await page.click('div.login-btn')
            await page.waitFor(6000)

            # 模拟人工拖动滑块、失败则重试
            while True:
                if await page.J('.live-index'):
                    print('登录成功！')
                    await page.waitFor(3000)
                    await self.get_cookie(page)
                    await page.waitFor(3000)
                    await self.page_close(browser)

                    return {'code': 200, 'msg': '登陆成功'}
                else:
                    await mouse_slide(page)
        except:
            return {'code': -1, 'msg': '出错'}

        finally:
            await page.waitFor(3000)
            await self.page_close(browser)

    # 获取登录后cookie
    async def get_cookie(self, page):
        cookies_list = await page.cookies()
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1}; '
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        self.jdRedisQueue.put_hash(self.shopId, cookies)
        return cookies

    async def page_evaluate(self, page):
        await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')
        await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
        await page.evaluate(
            '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
        await page.waitFor(3000)

    async def page_close(self, browser):
        for _page in await browser.pages():
            await _page.close()
        await browser.close()

    def input_time_random(self):
        return random.randint(100, 151)

    def run(self, username=USERNAME, password=PASSWORD, url=LOGIN_URL):
        loop = asyncio.get_event_loop()
        i_future = asyncio.ensure_future(self.login(username, password, url))
        loop.run_until_complete(i_future)
        return i_future.result()


if __name__ == '__main__':
    Z = JDLogin(shopId="")
    Z.run()
