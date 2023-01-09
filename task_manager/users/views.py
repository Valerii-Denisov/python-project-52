from django.shortcuts import render
from django.views import View


class UsersView(View):
    template_name = 'users.html'

    def get(self, request):
        return render(request, self.template_name)
