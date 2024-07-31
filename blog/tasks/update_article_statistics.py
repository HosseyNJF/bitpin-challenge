from celery import shared_task

from blog.services import AttackMitigationService


@shared_task
def update_article_statistics():
    AttackMitigationService.update_article_statistics()
