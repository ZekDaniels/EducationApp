from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.contrib import messages

class LessonListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        if not request.user.profile.admin_permitted():
            messages.error(request, 'Bu işlemi yapmak için izniniz bulunmuyor.')
            return redirect('dashboard')
        return render(request, 'education/lesson/lesson_list.html', context)