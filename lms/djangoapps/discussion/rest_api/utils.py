"""
Utils for discussion API.
"""

from lms.djangoapps.discussion.django_comment_client.utils import has_discussion_privileges


def discussion_closed_for_user(course, user):
    """
    Check if course discussion are closed or not for user.
    :param course:
    :param user:
    :return:
    """
    if not course.forum_posts_allowed and not has_discussion_privileges(user, course.id):
        return True
    return False
