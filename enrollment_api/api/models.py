from django.db import models


# class Folder(models.Model):
#     name = models.CharField(max_length=200)
#     type = models.CharField(max_length=200)
#     url = models.SlugField(unique=True, max_length=255)
#     size = models.CharField(max_length=200)
#     parentId = models.ForeignKey('self', null=True, blank=True,
#                                  on_delete=models.CASCADE, default=None,
#                                  related_name='childId')
#     date = models.CharField(max_length=200)

class File(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
#    name = models.CharField(max_length=200)
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
    # children = models.ForeignKey('self',
    #                              on_delete=models.CASCADE,
    #                              blank=True,
    #                              null=True,
    #                              default=None
    #                              )
    # date = models.CharField(max_length=200, default=None)
    updateDate = models.DateTimeField(default=None, null=True)


# class Item:
#     def __init__(self, id, type, date, size=None,  url=None,  parent_id=None):
#         self.id = id
#         self.type = type
#         self.url = url
#         self.size = size
#         self.parent_id = parent_id
#         self.children = list()
#         self.date = date
