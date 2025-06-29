from celery import shared_task

from app_users.user import del_anonymous_users


@shared_task(name="del_anonymous")
def del_anonymous():
    """Удаление анонимных пользователей"""
    del_anonymous_users()
