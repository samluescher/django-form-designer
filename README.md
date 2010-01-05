Django Form Designer
====================

A Django app for building many kinds of forms visually, without any programming knowledge.

Features:

* Design contact forms, search forms etc from the Django admin, without writing any code
* Form data can be logged, sent via e-mail or forwarded to any web address
* Integration with Django CMS (add forms to any page)
* Use drag & drop to change the position of your form fields
* Fully collapsible admin interface for better overview over your form 
* Implements many form fields included with Django (TextField, EmailField, DateField etc)
* Validation rules as supplied by Django are fully configurable (maximum length, regular expression etc) 
* Customizable messages and labels
* Supports POST and GET forms

Installation
------------

Add the form_designer app to your INSTALLED_APPS setting.

    "form_designer",
    
Add the form_designer URLs to your URL conf. For instance, in order to make a form "example-form" available under http://domain.com/forms/example-form, add the following line:

    (r'^forms/', include('form_designer.urls')),

If you are using the form_designer plugin for Django CMS, this second step is not necessary.

Optional requirements
---------------------

* form_designer supports [django-notify](http://code.google.com/p/django-notify/). If it is installed in your project, it will be used for success and error notifications. 

* The form_designer admin form requires jQuery and the jQuery UI Sortable plugin to make building forms a lot more user-friendly. The two Javascript files are bundled with the form_designer app. If you want to use you own jquery-*.js and jquery-ui-*.js instead, define JQUERY_JS and JQUERY_UI_JS in your settings file. For instance:

JQUERY_JS = 'jquery/jquery-latest.js'

Known issues
------------

* Redirection after successful form submission currently doesn't work if used with Django CMS.

Missing features
----------------

* File upload fields will be implemented
