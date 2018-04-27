import logging
import os
import time

from pdfkit.configuration import Configuration
from pdfkit import PDFKit
from selenium import webdriver

search_url = "http://weixin.sogou.com/weixin?type=1&s_from=input&query=%s&ie=utf8&_sug_=n&_sug_type_="
chrome_driver_path = 'drivers/chromedriver.exe'
wkhtmltopdf_path = "D:\\Program Files\\WKhtmltopdf\\bin\\wkhtmltopdf.exe"
here = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


# 查询微信公众号
class WeChatSubscription:

    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.set_headless()
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
        driver.set_window_size(1600, 900)
        self.driver = driver

    def close_driver(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception as e:
            logger.error("close_driver error :%s", e)
            pass

    def get_articles_urls(self, name):
        article_list = []
        try:
            if self.__goto_detail_page__(name):
                article_list = self.__get_urls__(name)
        except Exception as e:
            logger.error("get_articles_urls error :%s", e)
            pass

        return article_list

    # 查询公众号，并跳转到公众号的数据页面
    def __goto_detail_page__(self, name):
        try:
            c_search_url = search_url % name
            logger.info("goto_detail_page driver.get :%s", c_search_url)
            self.driver.get(c_search_url)
            assert name in self.driver.title
            logger.info("goto_detail_page Title 1:%s", self.driver.title)
            tag = self.driver.find_element_by_class_name("news-box"). \
                find_element_by_tag_name("ul").find_element_by_tag_name("li")

            if tag is not None:
                handles1 = self.driver.window_handles
                tag.find_element_by_tag_name("a").click()
                handles2 = self.driver.window_handles
                handle = set(handles2).difference(set(handles1)).pop()
                self.driver.switch_to.window(handle)
                logger.info("goto_detail_page Title 2:%s", self.driver.title)
                while self.driver.title.find("请输入验证码") >= 0:
                    time.sleep(1)

                return True
        except Exception as e:
            logger.error("goto_detail_page error :%s", e)
            pass
        return False

    # 从公众号的数据页面获取历史文章的链接
    def __get_urls__(self, name):
        article_list = []
        try:
            current_url = str(self.driver.current_url)
            pre_url = current_url[0:current_url.index("/", 8, len(current_url))]
            logger.info("get_urls Title:%s pre_url:%s  current_url:%s", self.driver.title, pre_url, current_url)
            card_list_element = self.driver.find_element_by_class_name("weui_msg_card_list")
            article_elements = card_list_element.find_elements_by_class_name("weui_media_bd")

            for element in article_elements:
                title_element = element.find_element_by_class_name("weui_media_title")
                title = title_element.text
                hrefs = title_element.get_attribute("hrefs")

                extra_element = element.find_element_by_class_name("weui_media_extra_info")
                date = extra_element.text

                msg = {"from": name, "title": title, "href": "%s%s" % (pre_url, hrefs), "date": date}
                logger.info("get_urls msg:%s", msg)
                article_list.append(msg)

        except Exception as e:
            logger.error("get_urls error :%s", e)
            pass
        return article_list


class ArticleToPDF:
    def __init__(self):
        wkhtmltopdf_conf = Configuration(wkhtmltopdf=wkhtmltopdf_path)
        self.wkhtmltopdf_conf = wkhtmltopdf_conf
        os.makedirs(os.path.join(here, "Tmp"), exist_ok=True)

    def save(self, articles):
        for article in articles:
            try:
                href = article["href"]
                logger.info("ArticleToPDF save :%s", article["title"])
                file_name = "%s-%s%s" % (article["date"], article["title"], ".pdf")
                file_name = file_name.replace("/", " ").replace("?", "").replace(":", "：").replace("|", " ")

                folder = os.path.join(here, "files", article["from"], )
                os.makedirs(folder, exist_ok=True)
                file_path = os.path.join(folder, file_name)

                if not os.path.exists(file_path):
                    path_tmp = "Tmp/Tmp%s.pdf" % time.time()
                    self.__save_url_to_pdf__(href, path_tmp)

                    os.rename(os.path.join(here, path_tmp), file_path)
                    logger.info("ArticleToPDF save file:%s", file_path)
                else:
                    logger.warning("ArticleToPDF already exists file:%s", file_path)
            except Exception as e:
                logger.error("ArticleToPDF save error : %s", e)
                pass

    def __save_url_to_pdf__(self, url, file):
        try:
            pdf = PDFKit(url_or_file=url, type_='url', configuration=self.wkhtmltopdf_conf)
            pdf.to_pdf(file)
        except Exception as e:
            logger.error("ArticleToPDF save_url_to_pdf error : %s", e)
            pass
