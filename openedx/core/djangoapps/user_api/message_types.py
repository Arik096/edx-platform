"""
Message Types for user_api emails
"""


from django.conf import settings

from openedx.core.djangoapps.ace_common.message import BaseMessageType
from openedx.core.djangoapps.site_configuration import helpers


class DeletionNotificationMessage(BaseMessageType):
    """
    Message to notify learners that their account is queued for deletion.
    """
    def __init__(self, *args, **kwargs):
        super(DeletionNotificationMessage, self).__init__(*args, **kwargs)  # lint-amnesty, pylint: disable=super-with-arguments

        self.options['transactional'] = True  # pylint: disable=unsupported-assignment-operation
        self.options['from_address'] = helpers.get_value(  # pylint: disable=unsupported-assignment-operation
            'email_from_address', settings.DEFAULT_FROM_EMAIL
        )
