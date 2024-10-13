from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from management.models import User_details
from student.models import PaymentDetails
# Registering the User_details model
admin.site.register(User_details)


class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_paid', 'payment_date', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('user__username',)
    actions = ['approve_payments', 'deny_payments']

    def approve_payments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected payments have been approved.")
    approve_payments.short_description = "Approve selected payments"

    def deny_payments(self, request, queryset):
        deleted_count, _ = queryset.delete()
        self.message_user(request, f"{deleted_count} payment(s) have been denied and deleted.")
    deny_payments.short_description = "Deny and delete selected payments"

admin.site.register(PaymentDetails, PaymentDetailsAdmin)


# in the management panel need to set the aprovil according to the dtabase!!!!!~