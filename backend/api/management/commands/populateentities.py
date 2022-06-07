import os
from functools import reduce
from os import path
from glob import glob
from django.conf import settings
from django.core.management.base import BaseCommand

try:
    from backend.api.models import Project, Entity
except ImportError:
    from api.models import Project, Entity


def _reducer(accumulator: dict, file: str):
    name, extension = path.splitext(path.basename(file))
    if extension == '.json':
        return accumulator
    return {**accumulator, name: extension[1:]}


class Command(BaseCommand):
    help = 'Index all entities on disk and import then to the database.'

    def _init_projects(self):
        db_codes = set(map(lambda proj: proj['code'], Project.objects.values()))
        fs_codes = set(map(lambda p: path.basename(path.dirname(p)), glob(path.join(settings.ENTITIES_ROOT, '*', ''))))

        for missing_in_fs in db_codes - fs_codes:
            self.stdout.write(f'Creating project directory: {missing_in_fs}...', ending=' ')
            os.mkdir(path.join(settings.ENTITIES_ROOT, missing_in_fs))
            self.stdout.write(self.style.SUCCESS('OK'))

        for missing_in_db in fs_codes - db_codes:
            self.stdout.write(f'Creating project record: {missing_in_db}...', ending=' ')
            project = Project(name=missing_in_db, code=missing_in_db)
            project.save()
            self.stdout.write(self.style.SUCCESS('OK'))

        return db_codes | fs_codes

    def handle(self, *args, **kwargs):
        projects = self._init_projects()

        for project in projects:
            project_id = Project.objects.get(code=project).id

            self.stdout.write(self.style.MIGRATE_HEADING(f'Indexing {project}:'))
            files = reduce(_reducer, glob(path.join(settings.ENTITIES_ROOT, project, '*')), {})
            saved = set(map(lambda x: x['uuid'], Entity.objects.filter(project_id=project_id).values('uuid')))
            out_of_sync = set(files.keys()) - saved

            if not len(out_of_sync):
                self.stdout.write(' Project is up to date.')
                continue

            self.stdout.write(f' {len(out_of_sync)} files are missing in database, pushing them', ending='... ')

            for entity_file in out_of_sync:
                entity = Entity(uuid=entity_file, extension=files[entity_file], project_id=project_id)
                entity.save()

            self.stdout.write(self.style.SUCCESS('OK'))
