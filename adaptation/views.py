from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from adaptation.forms import AdaptationUpdateForm, DisableAdaptationClassForm, DisableStudentClassForm, DisableAdaptationForm, StudentClassForm, ProtoAdaptionForm
from adaptation.models import AdapatationClass, Adaptation

class AdaptationCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.adaptation is not None:
                return redirect('adaptation:adaptation_manage', request.user.adaptation.get().id)
        except:
            context = {'adaptation_create_form': ProtoAdaptionForm()}
            return render(request, 'adaptation/student/adaptation_create.html', context)
    
class AdaptationManageView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        if not request.user.adaptation:
             return redirect('adaptation:adaptation_create')
        adaptation = get_object_or_404(Adaptation, pk=id, user=request.user)
        adaptation_create_form = AdaptationUpdateForm(instance=adaptation)
        adaptation_classes = AdapatationClass.objects.order_by("id")
        
        class_form = StudentClassForm()
        disable_student_class_form = DisableStudentClassForm()
        disable_adaptation_class_form = DisableAdaptationClassForm()

        context = {
            'adaptation_create_form': adaptation_create_form,
            'class_form': class_form,
            'disable_student_class_form': disable_student_class_form,
            'disable_adaptation_class_form': disable_adaptation_class_form,
            'adaptation':adaptation,
            'adaptation_classes':adaptation_classes,
            }
        return render(request, 'adaptation/student/adaptation_manage.html', context)


class AdaptationList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'adaptation/professor/adaptation_list.html', context)


class AdaptationConfirmationView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        adaptation = get_object_or_404(Adaptation, pk=id)
        adaptation_classes = AdapatationClass.objects.order_by("id")
        disable_student_class_form = DisableStudentClassForm()
        disable_adaptation_class_form = DisableAdaptationClassForm()
        disable_adaptation_form = DisableAdaptationForm(instance=adaptation)
        context = {
            'adaptation': adaptation,
            'adaptation_classes':adaptation_classes,
            'disable_student_class_form': disable_student_class_form,
            'disable_adaptation_class_form': disable_adaptation_class_form,
            'disable_adaptation_form': disable_adaptation_form,
        }
        return render(request, 'adaptation/professor/adaptation_confirmation.html', context)

