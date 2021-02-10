import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.http import Http404

from openedx.core.djangoapps.programs.models import ProgramsApiConfig
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication

from openedx.core.djangoapps.programs.utils import (
    ProgramProgressMeter,
    get_program_marketing_url,
)


def _reformat_progress(progress_list):
    simplified_progress = {}
    for progress in progress_list:
        uuid = progress.get('uuid', None)
        print('UUID ' + uuid)
        if uuid:
            simplified_progress[uuid] = {
                'completed': progress.get('completed', ''),
                'in_progress': progress.get('in_progress', ''),
                'not_started': progress.get('not_started', ''),
            }
    return simplified_progress


def _prepare_program_context(programs, progress):
    context = {}
    short_program_list = []
    for program in programs:
        uuid = program.get('uuid', '')
        progress_update = _reformat_progress(progress)
        program_progress = progress_update.get(uuid, {})
        short_program = {
            'uuid': uuid,
            'title': program.get('title', ''),
            'subtitle': program.get('subtitle', ''),
            'type': program.get('type', ''),
            'type_attrs': program.get('type_attrs', {}),
            'marketing_url': program.get('marketing_url', ''),
            'banner_image': program.get('banner_image', {}),
            'authoring_organizations': program.get('authoring_organizations', {}),
            'progress': program_progress,
        }
        short_program_list.append(short_program)
    context['programs'] = short_program_list
    return context


class ProgramListView(APIView):
    authentication_classes = (
        JwtAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        """
        Return a list programs a user is enrolled in.
        """
        user = request.user
        try:
            mobile_only = json.loads(request.GET.get('mobile_only', 'false'))
        except ValueError:
            mobile_only = False

        programs_config = ProgramsApiConfig.current()
        if not programs_config.enabled:
            raise Http404

        meter = ProgramProgressMeter(site=request.site, user=user, mobile_only=mobile_only)
        context = _prepare_program_context(meter.engaged_programs, meter.progress())
        context['marketing_url'] = get_program_marketing_url(programs_config, mobile_only),

        return Response(context)
