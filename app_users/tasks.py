from celery import shared_task

# from config.logger import logger

from app_users.user import del_anonymous_users


@shared_task(name="del_anonymous")
def del_anonymous():
    # logger.info("Удаление анонимных пользователей")
    print("Удаление анонимных пользователей")
    del_anonymous_users()
