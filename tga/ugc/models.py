from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Account ID',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Name',
        default=None,
        blank=True,
        null=True,
    )
    first_name = models.TextField(
        verbose_name='First Name',
        default=None,
        blank=True,
        null=True,
    )
    l_name = models.TextField(
        verbose_name='Last Name',
        default=None,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Collect date',
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return f'#{self.external_id} {self.name} {self.first_name} {self.l_name} {self.created_at}'

    class Meta:
        verbose_name = 'Profile'


class Message_url(models.Model):
    profile = models.PositiveIntegerField(
        verbose_name='Profile',
    )

    text = models.TextField(
        verbose_name='Text'
    )

    created_at = models.DateTimeField(
        verbose_name='Collect date',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Message {self.pk} from {self.profile}'

    class Meta:
        verbose_name = 'Message_url'
        verbose_name_plural = 'Message_url'
