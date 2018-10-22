import celery
from twitterinterface import tweetextract,geocoding

@celery.task()
def print_hello():
    logger = print_hello.get_logger()
    tweetextract.gettweetbytag()
    logger.info("Hello")
    print('hellooooooooooooooooos')
