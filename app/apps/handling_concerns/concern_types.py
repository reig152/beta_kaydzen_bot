from django.db import models


class ConcernTypes(models.Model):
    """
    Базовый класс модели с 2 полями:
    pk - описание. PK заводится автоматически.
    """
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        # указываем абстрактную модель,
        # чтобы можно было наследоваться от этой модели
        abstract = True
    
    def __str__(self) -> str:
        return self.description[:20]
