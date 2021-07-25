# Scrapy settings for Pokemon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Pokemon'

SPIDER_MODULES = ['Pokemon.spiders']
NEWSPIDER_MODULE = 'Pokemon.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Pokemon.middlewares.RandomUserAgentMiddleware': 1,
}

RANDOM_UA_TYPE = "google"

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Pokemon.pipelines.MongoDBTwistedPipeline': 1,
    'Pokemon.pipelines.ElasticSearchPipeline': 2,
}

MONGODB_URI = 'mongodb://10.0.0.22:27017/'
MONGODB_DB = "search_engine"
MONGODB_COLLECTION = "pokemon3"

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.2
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
