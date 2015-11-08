from django import forms
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.db import models
from django.forms.widgets import RadioChoiceInput
from helpdesk.models import Client, Incident, IncidentLog


class ClientAdmin(admin.ModelAdmin):
    radio_fields = {"status": admin.HORIZONTAL}
    list_display = ('name', 'status', 'account_manager', 'notify',)
    list_filter = ('status',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "account_manager":
            kwargs["queryset"] = User.objects.filter(groups__name='Account Managers')
        return super(ClientAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class IncidentLogInlineFormset(forms.models.BaseInlineFormSet):
    def save_new(self, form, commit=True):
        obj = super(IncidentLogInlineFormset, self).save_new(form, commit=False)
        obj.responsible = self.request.user
        if commit:
            obj.save()
        return obj


class IncidentLogInline(admin.TabularInline):
    model = IncidentLog
    fields = ('date', 'responsible', 'description',)
    readonly_fields = ('date', 'responsible',)
    can_delete = False
    formset = IncidentLogInlineFormset
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(IncidentLogInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


class IncidentAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "pax_name", "date", "status",)
    list_filter = ("client", "responsible")
    search_fields = ("pax_name", "pax_email", "pcc", "locator",)
    date_hierarchy = "date"
    ordering = ("-date",)
    inlines = (IncidentLogInline,)

    fieldsets = (
        (None, {
            'fields': ('client', 'pax_name', 'pax_email', 'pcc', 'locator', 'subject', 'status',)
        }),
        ('Billing', {
            'classes': ('collapse',),
            'fields': ('charge', 'bill_to', 'bill_address', 'tax_number', 'invoice_number',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.responsible:
            obj.responsible = request.user
        obj.save()


admin.site.register(Client, ClientAdmin)
admin.site.register(Incident, IncidentAdmin)
