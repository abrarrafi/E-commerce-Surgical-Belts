from django.contrib import admin
from django.contrib.admin import AdminSite

# Customize AdminSite
class MyAdminSite(AdminSite):
    site_header = "Your Custom Admin"
    site_title = "Your Site Admin Portal"
    index_title = "Welcome to Your Admin Dashboard"

# Replace default admin site
admin.site.site_header = "Your Custom Admin"
admin.site.site_title = "Your Site Admin Portal"
admin.site.index_title = "Welcome to Your Admin Dashboard"
