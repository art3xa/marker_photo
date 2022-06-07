import json
import os
from datetime import datetime
from math import floor
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from .models import *


@api_view(['GET'])
@permission_classes([])
def get_me(request: Request) -> Response:
    if request.user.is_anonymous:
        return Response(status=401)
    return Response({
        'id': request.user.id,
        'username': request.user.get_username(),
        'name': request.user.get_full_name(),
    })


@api_view(['POST'])
@permission_classes([])
def login(request: Request) -> Response:
    try:
        username = request.POST.get('username', request.data['username'])
        password = request.POST.get('password', request.data['password'])
    except KeyError:
        return Response(status=400)

    user = authenticate(request._request, username=username, password=password)

    if user is None:
        return Response('Invalid credentials.', status=401)

    auth_login(request._request, user)

    return Response('Authenticated.')


@api_view(['GET'])
def get_classifications(request: Request) -> Response:
    if request.user.project is None:
        return Response('User is not assigned to project: nothing to show.', status=403)
    return Response(list(Classification.objects.filter(project_id=request.user.project).values()))


@api_view(['GET'])
def get_next_entity(request: Request) -> Response:
    try:
        latest = Entity.objects.filter(state=Entity.EntityState.UNANNOTATED, project=request.user.project).first()

        if latest is None:
            raise Entity.DoesNotExist()

        latest.state = Entity.EntityState.LOCKED
        latest.lock_ts = floor(datetime.now().timestamp())
        latest.save()

        data = model_to_dict(latest)
        data['project'] = latest.project.code

        return Response(data)
    except Entity.DoesNotExist:
        return Response('No entities available.', status=404)


@api_view(['POST'])
def write_entity_data(request: Request, **kwargs) -> Response:
    entity = Entity.objects.get(uuid=kwargs['uuid'], project=request.user.project)

    entity.state = Entity.EntityState.ANNOTATED
    entity.assigned_user = request.user
    entity.save()

    with open(os.path.join(settings.ENTITIES_ROOT, request.user.project.code, entity.uuid + '.json'), 'w') as f:
        json.dump(request.data, f, sort_keys=True, indent=2)

    return Response(entity.uuid)
