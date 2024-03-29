import scrapy
from scrapy import signals
from selenium import webdriver
from foody.items import FoodyItem
from selenium.webdriver.common.action_chains import ActionChains
import time
import shutil


items = FoodyItem()
user_name = #
password = #
number_foods = 1992
# driver_path = r'C:\Users\tranv\Desktop\Python Project\chromedriver.exe'
driver_path = r'path\to\webdriver'


def configure_driver():
    # Web driver for Chrome
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)

    # Web driver for FireFox
    # BROWSER_EXE = 'path/to/driver'
    # FirefoxBinary = FirefoxBinary(BROWSER_EXE)
    # options = webdriver.FirefoxOptions()
    # driver = webdriver.Firefox(firefox_options=options)
    return driver


def get_food_info(element):
    title = element.find_element_by_xpath('.//div[contains(@class, "title")]')
    href = title.find_element_by_xpath('./a').get_attribute('href')
    return href


def get_all_shops(driver, shop_xpath, url):
    driver.get(url)
    while True:
        foods = driver.find_elements_by_xpath(shop_xpath)
        if len(foods) == number_foods:
            break
        else:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(3)
            more_btn = driver.find_element_by_xpath('//div[@class = "pn-loadmore fd-clearbox ng-scope"]/a[@class = "fd-btn-more"]')
            actions = ActionChains(driver)
            actions.move_to_element(more_btn).click().perform()
            time.sleep(2)
    for f in foods:
        get_food_info(f)
    return foods


def find_reviews_points(driver):
    dict = {}
    points = driver.find_elements_by_xpath('//div[@class="microsite-top-points"]')
    for p in points:
        es = p.find_elements_by_xpath('.//div')
        cat = es[1].text
        score = es[0].text
        dict[cat] = [score]
    items['Quality'] = dict['Chất lượng']
    items['Position'] = dict['Vị trí']
    items['Price'] = dict['Giá cả']
    items['Service'] = dict['Phục vụ']
    items['Space'] = dict['Không gian']

    point_avg = driver.find_element_by_xpath('//div[contains(@class, "microsite-point-avg")]').text
    items['ZAvg_Score'] = point_avg


def find_food_name(driver):
    name = driver.find_element_by_xpath('//div[contains(@class, "main-info-title")]/h1').text
    items['Name'] = name


def log_in(driver, response):
    driver.get('https://id.foody.vn/account/login?returnUrl=https://www.foody.vn//')
    driver.find_element_by_xpath('//input[contains(@id, "Email")]').send_keys(user_name)
    driver.find_element_by_xpath('//input[contains(@id, "Password")]').send_keys(password)
    driver.find_element_by_xpath('//input[contains(@id, "bt_submit")]').click()
    time.sleep(3)
    url = 'https://www.foody.vn//'
    return url


class FoodHcmSpider(scrapy.Spider):
    name = 'food_hcm'
    allowed_domains = ['www.foody.vn//']
    start_urls = ['https://www.foody.vn//']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FoodHcmSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        shutil.move("FOOD_HCM.csv", 'path\\to\\Report directory')
        # shutil.move("FOOD_HCM.csv", 'C:\\Users\\tranv\\Desktop\\Python Project\\Data Challenge 1\\foody\Report')

    def parse(self, response):
        driver = configure_driver()
        redirect_url = log_in(driver, response)
        shop_xpath = '//div[contains(@class, "content-item")]'
        shops = get_all_shops(driver, shop_xpath, redirect_url)
        urls = [get_food_info(s) for s in shops]

        for url in urls:
            if url is not None:
                driver.get(url)
                find_food_name(driver)
                find_reviews_points(driver)
                yield items
                time.sleep(0.5)
        pass
