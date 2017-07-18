import os
import json

from django.conf import settings
from django.core.management import BaseCommand

from handler.models import Group, Data


class Command(BaseCommand):
    help = 'load data'

    GROUP_DICT = {}

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'fixtures', 'data.json')
        with open(file_path, 'r') as f:
            data = json.loads(f.read())

        data_list = list()
        for item in data.get('data'):
            data_list.append(self._create_data_instance(item))

        Data.objects.bulk_create(data_list)

    def _create_data_instance(self, item):

        group, country, value = item.values()
        group_id = self._create_group_instance(group)
        data = Data(
            name=country,
            value=value,
            group_id=group_id
        )
        return data

    def _create_group_instance(self, group_name):
        if self.GROUP_DICT.get(group_name):
            return self.GROUP_DICT.get(group_name)
        else:
            group = Group.objects.create(name=group_name)
            self.GROUP_DICT[group_name] = group.id
            return group.id


