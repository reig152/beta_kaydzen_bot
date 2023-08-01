from django.db import models


class Company(models.Model):
    """Модель списка компаний."""
    company_name = models.TextField(
        verbose_name="Название компании"
    )
    legal_company_name = models.TextField(
        verbose_name="Юридичиское имя компании",
        null=True,
        blank=True
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


class Department(models.Model):
    """
    Модель департаментов.
    """
    company_name = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания департамента",
        null=True,
        blank=True
    )
    department_name = models.CharField(
        max_length=256,
        verbose_name="Название департамента"
    )

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'

    def __str__(self) -> str:
        return self.department_name