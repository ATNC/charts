from django.db import models


class CustomGroupManager(models.Manager):

    def get_or_default(self, group_id=None):
        if group_id:
            group = Group.objects.get(id=group_id)
        else:
            group = Group.objects.first()
        return group


class Group(models.Model):
    name = models.CharField(max_length=255)

    objects = CustomGroupManager()
    
    def __str__(self):
        return f'{self.name}'

    @property
    def for_googlecharts(self):
        return [[*item.values()] for item in self.data.values('name', 'value')]


class Data(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=4, decimal_places=2)
    group = models.ForeignKey(Group, related_name='data')

    def __str__(self):
        return f'{self.name}- {self.value}'


