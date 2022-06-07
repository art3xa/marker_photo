from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Project(models.Model):
    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'

    name = models.CharField(max_length=64, verbose_name='Имя проекта')
    code = models.CharField(max_length=64, verbose_name='Код проекта', help_text='Является ключом в JSON файлах.')

    def __str__(self):
        return self.name


class Staff(AbstractUser):
    project = models.ForeignKey(Project, null=True, verbose_name='Проект', on_delete=models.DO_NOTHING)


class Classification(models.Model):
    class Meta:
        verbose_name = 'классификация'
        verbose_name_plural = 'классификации'

    name = models.CharField(max_length=64, verbose_name='Название', help_text='Это название видят разетчики.')
    code = models.CharField(max_length=64, verbose_name='Кодовое имя', help_text='Является ключом в JSON файлах.')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.FileField(verbose_name='Иллюстрация',
                             help_text='Должна быть квадратной, разрешение в пределах разумного.')
    project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} [{self.project.name}]'


class Entity(models.Model):
    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    class EntityState(models.TextChoices):
        UNANNOTATED = 'Unannotated', 'Не размечен'
        LOCKED = 'Locked', 'Заблокирован'
        ANNOTATED = 'Annotated', 'Размечен'

    uuid = models.CharField(max_length=128, verbose_name='UUID')
    extension = models.CharField(max_length=4, verbose_name='Расширение файла')
    state = models.CharField(max_length=16, choices=EntityState.choices, default=EntityState.UNANNOTATED,
                             verbose_name='Статус')
    assigned_user = models.ForeignKey(Staff, db_column='user', blank=True, null=True, on_delete=models.DO_NOTHING,
                                      verbose_name='Присвоенный разметчик',
                                      help_text='Этот пользователь разметил изображение.')
    lock_ts = models.BigIntegerField(default=0, editable=False)
    project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.uuid}.{self.extension} [{self.state}] [{self.project.name}]'
