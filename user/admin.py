from django.contrib import admin
import openpyxl
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Society, Grievance, Request
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from django.http import HttpResponse



def export_selected_objects(modeladmin, request, queryset):
    # Get all field names for the model
    fields = ['email','username', 'is_paid' ,'state','district','society_type','registered_address','area_of_operation', 'pan_no', 'tan_no','officer_authorized', 'designation','service_tax_no',]

    # Create a new workbook and get the active sheet
    wb = openpyxl.Workbook()
    sheet = wb.active

    # Write the header row
    sheet.append(fields)

    # Write data rows
    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        sheet.append(row)

    # Create a response object with Excel content
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_objects.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response

admin.site.add_action(export_selected_objects)

class ProfileAdmin(UserAdmin):
    list_display = ('email','username', 'is_paid', 'mobile_no', 'pan_no', 'tan_no', 'service_tax_no')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ('is_paid',)
    fieldsets = ()
    actions = [export_selected_objects]
    actions_description = "Export selected objects"
    actions_selection_counter = True

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile


admin.site.register(Request)


@admin.register(Grievance)
class CustomGrievanceAdmin(UserAdmin):
    list_display = ('name', 'email', 'complain_date', 'mob_no', 'complain_type', 'complain_soc', 'complainXfeedback')
    search_fields = ('name', 'email', 'complain_type', 'complain_soc')
    ordering = ['name']  # Update with a valid field name from the Grievance model
    readonly_fields = ('name',)  # Update with valid fields from the Grievance model
    filter_horizontal = ()
    list_filter = ('complain_type', 'complain_soc')
    fieldsets = ()
    actions = [export_selected_objects]
    actions_description = "Export selected objects"
    actions_selection_counter = True

admin.site.register(Profile, ProfileAdmin)

@admin.register(Society)
class SocietyAdmin(ImportExportModelAdmin):
    pass
