Django Form Designer
====================

A Django app for building many kinds of forms visually, without any programming knowledge.

__Features__:

* Design contact forms, search forms etc from the Django admin, without writing any code
* Form data can be logged and CSV-exported, sent via e-mail, or forwarded to any web address
* Integration with [Django CMS](http://www.django-cms.org): Add forms to any page
* Use drag & drop to change the position of your form fields
* Fully collapsible admin interface for better overview over your form 
* Implements many form fields included with Django (TextField, EmailField, DateField etc)
* Validation rules as supplied by Django are fully configurable (maximum length, regular expression etc) 
* Customizable messages and labels
* Supports POST and GET forms

Installation
------------

This document assumes that you are familiar with Python and Django.

1. Make sure `form_designer` is on your `PYTHONPATH`.
2. Make the directory `form_designer/media/form_designer` available under your `MEDIA_ROOT`.
3. Add `form_designer` to your `INSTALLED_APPS` setting.

        INSTALLED_APPS = (
            ...
            'form_designer',
        )
4. Add the form_designer URLs to your URL conf. For instance, in order to make a form named `example-form` available under `http://domain.com/forms/example-form`, add the following line to `urls.py`. __Note__: If you are using the form_designer plugin for Django CMS, step 4 is __not__ necessary:

        urlpatterns = patterns('',
            (r'^forms/', include('form_designer.urls')),
            ...
        )
   
5. Add the form_designer admin URLs to your URL conf if you want to use CSV export. Add the following line to `urls.py` _before_ the admin URLs:

        urlpatterns = patterns('',
            (r'^admin/form_designer/', include('form_designer.admin_urls')),
            ...
            (r'^admin/', include(admin.site.urls)),
        )

Optional requirements
---------------------

* form_designer supports [django-notify](http://code.google.com/p/django-notify/) for error messages and notifications. If it is installed in your project, it will be used for success and error notifications.
* The form_designer admin interface requires jQuery and the jQuery UI Sortable plugin to make building forms a lot more user-friendly. The two Javascript files are bundled with form_designer. If you want to use you own jquery-*.js and jquery-ui-*.js instead, define JQUERY_JS and JQUERY_UI_JS in your settings file. For instance:

        JQUERY_JS = 'jquery/jquery-latest.js'

Known issues
------------

* Redirection after successful form submission currently doesn't work if used with Django CMS.
* It should be possible to edit a form directly from the Django CMS page form.

Missing features
----------------
  
* File upload fields will be implemented
