# -*- coding: utf-8 -*-

# Scrapy settings for metrosCubicos project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'metrosCubicos'
DOWNLOAD_TIMEOUT = 6000
CONCURRENT_REQUESTS = 5

SPIDER_MODULES = ['metrosCubicos.spiders']
NEWSPIDER_MODULE = 'metrosCubicos.spiders'

ITEM_PIPELINES = {

    'metrosCubicos.pipelines.MetrosCubicosPipeline': 300,
}
