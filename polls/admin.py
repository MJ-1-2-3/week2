from django.contrib import admin

from .models import Choice, Question,Tags


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
class PollInline(admin.TabularInline):
    model = Tags
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline,PollInline]
    list_filter = ['pub_date']
    list_display = ('question_text', 'pub_date')
    search_fields = ['question_text']
    
admin.site.register(Question, QuestionAdmin)

# from django.contrib import admin
# from django.template.loader import get_template
# from django.utils.safestring import mark_safe

# from .models import Choice, Question, Polls


# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3
#     template = 'admin/inline_horizontal.html'


# class PollsInline(admin.TabularInline):
#     model = Polls
#     extra = 3
#     template = 'admin/inline_horizontal.html'


# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline, PollsInline]
#     list_filter = ['pub_date']
#     list_display = ('question_text', 'pub_date')
#     search_fields = ['question_text']

#     def get_inline_instances(self, request, obj=None):
#         inline_instances = super().get_inline_instances(request, obj)
#         for inline in inline_instances:
#             if isinstance(inline, (ChoiceInline, PollsInline)):
#                 inline.template = get_template(inline.template).render({'inline_admin_formset': inline.get_formset(request, obj)})
#         return inline_instances


# admin.site.register(Question, QuestionAdmin)
