from form_designer import settings as app_settings
from django.core.files.base import File
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.files import FieldFile
from django.template.defaultfilters import filesizeformat
import os
import hashlib, uuid


def get_storage():
    return app_settings.FILE_STORAGE_CLASS()


def clean_files(form):
    for field in form.file_fields:
        uploaded_file = form.cleaned_data.get(field.name, None)
        msg = None
        if uploaded_file is None:
            if field.required:
                msg = _('This field is required.')
            else:
                continue
        elif not os.path.splitext(uploaded_file.name)[1].lstrip('.').lower() in  \
            app_settings.ALLOWED_FILE_TYPES:
                msg = _('This file type is not allowed.')
        elif uploaded_file._size > app_settings.MAX_UPLOAD_SIZE:
            msg = _('Please keep file size under %(max_size)s. Current size is %(size)s.') %  \
                {'max_size': filesizeformat(app_settings.MAX_UPLOAD_SIZE), 
                'size': filesizeformat(uploaded_file._size)}
        if msg:
            form._errors[field.name] = form.error_class([msg])

    return form.cleaned_data
    

def handle_uploaded_files(form_definition, form):
    files = []
    if form_definition.save_uploaded_files and len(form.file_fields):
        storage = get_storage()
        secret_hash = hashlib.sha1(str(uuid.uuid4())).hexdigest()[:10]
        for field in form.file_fields:
            uploaded_file = form.cleaned_data.get(field.name, None)
            if uploaded_file is None:
                continue
            valid_file_name = storage.get_valid_name(uploaded_file.name)
            root, ext = os.path.splitext(valid_file_name)
            filename = storage.get_available_name(
                os.path.join(app_settings.FILE_STORAGE_DIR, 
                form_definition.name, 
                '%s_%s%s' % (root, secret_hash, ext)))
            storage.save(filename, uploaded_file)
            form.cleaned_data[field.name] = StoredUploadedFile(filename)
            files.append(storage.path(filename))
    return files


class StoredUploadedFile(FieldFile):
    """
    A wrapper for uploaded files that is compatible to the FieldFile class, i.e.
    you can use instances of this class in templates just like you use the value
    of FileFields (e.g. `{{ my_file.url }}`) 
    """
    def __init__(self, name):
        File.__init__(self, None, name)
        self.field = self

    @property
    def storage(self):
        return get_storage()
        
    def save(self, *args, **kwargs):
        raise NotImplementedError('Static files are read-only')

    def delete(self, *args, **kwargs):
        raise NotImplementedError('Static files are read-only')

    def __unicode__(self):
        return self.name
