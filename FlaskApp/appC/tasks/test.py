import celery
from appC.tasks.twitterinterface import tweetextract,geocoding,database

@celery.task()
def print_hello():
    logger = print_hello.get_logger()
    tweetextract.gettweetbytag()
    #database.checkusertable()
    logger.info("Hello")
    print('hellooooooooooooooooos')
