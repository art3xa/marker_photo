import kronos
from datetime import datetime
from math import floor
from .models import Entity


@kronos.register('* * * * *')
def unlock_entities():
    Entity.objects.filter(state=Entity.EntityState.LOCKED, lock_ts__lte=floor(datetime.now().timestamp()) - 600)\
        .update(state=Entity.EntityState.UNANNOTATED, lock_ts=0)
