Django Form Designer
********************

A Django admin app with a GUI to create complex forms without any programming skills; 
complete with logging, validation, and redirects.

**Key features**:

* Design contact forms, search forms etc from the Django admin, without writing any code
* Form data can be logged and CSV-exported, sent via e-mail, or forwarded to any web address
* Integration with `Django CMS <http://www.django-cms.org>`_: Add forms to any page
* Use drag & drop to change the position of your form fields
* Fully collapsible admin interface for better overview over your form 
* Implements many form fields included with Django (TextField, EmailField, DateField etc)
* Validation rules as supplied by Django are fully configurable (maximum length, regular 
  expression etc) 
* Customizable messages and labels
* Supports POST and GET forms
* Signals on form render, submission, success, error.


Installation
============

This install guide assumes that you are familiar with Python and Django.

- Install the module using pip::

    $ pip install git+git://github.com/philomat/django-form-designer.git#egg=django-form-designer

  **or** download it from http://github.com/philomat/django-form-designer, and run the installation 
  script::

    $ python setup.py install


Basic setup
===========

- Add ``form_designer`` to your ``INSTALLED_APPS`` setting::

        INSTALLED_APPS = (
            ...
            'form_designer',
        )

- Set up the database tables using::

    $ manage.py syncdb

  **or**, if you are using South::

    $ manage.py migrate form_designer

- If you are using ``django.contrib.staticfiles`` (recommended), just run the
  usual command to collect static files::

    $ python manage.py collectstatic

  .. Note::
     Please refer to the Django documentation on how to `set up the static files
     app <https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>`_ if
     you have not done that yet.

  If you are **not** going to use the ``staticfiles`` app, you will have to copy
  the contents of the ``static`` folder to the location you are serving static
  files from.

- Add the URLs to your URL conf. For instance, in order to make a form named
  ``example-form``   available under ``http://domain.com/forms/example-form``,
  add the following line to your    project's ``urls.py``::

    urlpatterns = patterns('',
        (r'^forms/', include('form_designer.urls')),
        ...
    )

  .. Note::
     If you are using the form_designer plugin for Django CMS for making forms
     public, this step is not necessary.


Using Django Form Designer with Django CMS 
==========================================

- Add ``form_designer.contrib.cms_plugins.form_designer_form`` to your ``INSTALLED_APPS`` 
  setting::

        INSTALLED_APPS = (
            ...
            'form_designer.contrib.cms_plugins.form_designer_form',
        )

- Set up the database tables using::

    $ manage.py syncdb

You can now add forms to pages created with Django CMS. 


Optional requirements
=====================

The form_designer admin interface requires jQuery and the jQuery UI Sortable
plugin to make building forms a lot more user-friendly. The two Javascript
files are bundled with form_designer. If you want to use you own jquery.js
instead because you're already including it anyway, define JQUERY\_JS in your
settings file. For instance::

    JQUERY_JS = 'jquery/jquery-latest.js'
