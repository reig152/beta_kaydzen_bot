from django.db import models


class Company(models.Model):
    """Модель списка компаний."""
    company_name = models.TextField(
        verbose_name="Название компании"
    )
    added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления в базу данных'
    )

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-added']

    def __str__(self) -> str:
        return self.company_name
