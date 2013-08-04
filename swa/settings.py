# Scrapy settings for swa project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'swa'

SPIDER_MODULES = ['swa.spiders']
NEWSPIDER_MODULE = 'swa.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# Chrome 28
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
USER_AGENT = " "

ITEM_PIPELINES = [
	'swa.pipelines.CheckDuplicatesPipeline'
]