from celery import shared_task
import logging

from app_users.user import del_anonymous_users

logger = logging.getLogger(__name__)
FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


@shared_task(name="del_anonymous")
def del_anonymous():
    logger.info("Удаление анонимных пользователей")
    del_anonymous_users()
