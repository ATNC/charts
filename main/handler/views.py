from handler.models import Group
from django.shortcuts import render_to_response
from django.http import Http404


def charts_list_view(request):
    if request.method == 'GET':
        group = Group.objects.get_or_default(request.GET.get('group'))

        list_of_groups = list(Group.objects.values('name', 'id').exclude(name=group.name))
        list_of_groups.insert(0, group)

        result = group.for_googlecharts
        return render_to_response('index.html', {
            'values': result,
            'groups': list_of_groups,
        })
    else:
        raise Http404
