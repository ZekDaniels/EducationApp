from user.models import Profile, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from education.forms import StudentClassForm
from django.contrib import messages
from utilities.render_pdf import render_to_pdf
import re

from io import BytesIO
from django.core.files import File



class AdaptationList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        if not request.user.profile.is_allowed_user():
            messages.error(request, 'Bu işlemi yapmak için izniniz bulunmuyor.')
            return redirect('dashboard')
        return render(request, 'adaptation/professor/adaptation_list.html', context)