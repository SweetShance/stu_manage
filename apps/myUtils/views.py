from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View


class Error(View):
    def get(self, request):
        context = {}
        from_url = request.GET.get('from_url')
        if from_url:
            context['from_url'] = from_url
        else:
            context['from_url'] = '/'

        return render(request, template_name="html/error_no_premission.html", context=context)
