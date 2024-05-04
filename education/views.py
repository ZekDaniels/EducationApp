from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.contrib import messages

class AdaptationList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        if not request.user.profile.is_allowed_user():
            messages.error(request, 'Bu işlemi yapmak için izniniz bulunmuyor.')
            return redirect('dashboard')
        return render(request, 'adaptation/professor/adaptation_list.html', context)