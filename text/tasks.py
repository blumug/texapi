from annoying.functions import get_object_or_None
from celery import task
from celery.utils.log import get_task_logger
import settings as text_settings

logger = get_task_logger(__name__)


@task(rate_limit='1/s')
def process_text(text_id):
    from models import Text
    logger.debug('processing text %d' % (text_id))
    text = get_object_or_None(Text, id=text_id)
    if text is not None:
        text.status = text_settings.TEXT_STATUS_PROCESSING
        text.save()

        text.parse()
        text.status = text_settings.TEXT_STATUS_FINISHED
        text.save()
