from django.db import models


class File(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    type = models.CharField(
        max_length=6,
        choices=(
            ('FILE', 'FILE'),
            ('FOLDER', 'FOLDER')
        )

    )
    url = models.CharField(unique=True, max_length=255, default=None, null=True)
    size = models.IntegerField(default=None, null=True)
    parentId = models.ForeignKey('self',
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 default=None
                                 )
    date = models.DateTimeField(default=None, null=True)
    # date = models.DateTimeField()