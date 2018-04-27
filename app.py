import logging_config
import logging

from app_classes import WeChatSubscription, ArticleToPDF

logging_config.init()
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("wechat spider start ")
    names = ["ImportNew", "Java后端技术", "Java编程", "算法与数据结构", "Python中文社区", "Python开发者",
             "Linux中国", "Linux学习", "大数据技术", "黑客技术与网络安全",
             "人民日报", "饭统戴老板", "刘姝威", "DeepTech深科技"]
    #
    wechatUrlsDeal = WeChatSubscription()
    pdfsave = ArticleToPDF()
    for name in names:
        articles = wechatUrlsDeal.get_articles_urls(name)
        logger.info("wechat spider %s articles:%s ", name, articles)
        pdfsave.save(articles)

    wechatUrlsDeal.close_driver()

    logger.info("wechat spider end ..................................................... ")
