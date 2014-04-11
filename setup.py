# encoding=utf8
import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.rst')

setup(
    name = "django-form-designer",
    version = "0.8.0",
    url = 'http://github.com/philomat/django-form-designer',
    license = 'BSD',
    description = "Design contact forms, search forms etc from the Django admin, without writing any code. Integrates with Django CMS.",
    long_description = README,

    author = 'Samuel Luescher',
    author_email = 'sam at luescher dot org',
    packages = [
        'form_designer',
        'form_designer.migrations',
        'form_designer.templatetags',
        'form_designer.contrib',
        'form_designer.contrib.exporters',
        'form_designer.contrib.cms_plugins',
        'form_designer.contrib.cms_plugins.form_designer_form',
    ],
    package_data = {
        'form_designer': [
            'static/form_designer/js/*.js',
            'templates/admin/form_designer/formlog/change_list.html',
            'templates/html/formdefinition/*.html',
            'templates/html/formdefinition/forms/*.html',
            'templates/html/formdefinition/forms/includes/*.html',
            'templates/txt/formdefinition/*.txt',
            'locale/*/LC_MESSAGES/*',
        ],
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
