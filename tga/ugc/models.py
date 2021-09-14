from django.db import models


class Profile(models.Model):
    external_id = models.CharField(
        verbose_name='Account ID',
        # unique=True,
        primary_key=True,
        max_length=250
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
        blank=True,
        null=True
    )
    last_url = models.TextField(
        verbose_name='Last URL',
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'#{self.external_id} {self.name} {self.first_name} {self.l_name} {self.created_at} {self.last_url}'

    def get_last_url(self):
        return self.last_url

    class Meta:
        verbose_name = 'Profile'


class Message_url(models.Model):
    profile = models.PositiveIntegerField(
        verbose_name='Profile',
    )

    text = models.TextField(
        verbose_name='Text'
    )

    file_name = models.CharField(
        verbose_name='Video name',
        default=None,
        blank=True,
        null=True,
        max_length=255
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
