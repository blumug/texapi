from django.utils.translation import ugettext_lazy as _

TEXT_STATUS_PENDING = 'pending'
TEXT_STATUS_PROCESSING = 'processing'
TEXT_STATUS_FINISHED = 'finished'

TEXT_STATUS_CHOICES = (
    (TEXT_STATUS_PENDING, _('Pending')),
    (TEXT_STATUS_PROCESSING, _('Processing')),
    (TEXT_STATUS_FINISHED, _('Finished')),
)
