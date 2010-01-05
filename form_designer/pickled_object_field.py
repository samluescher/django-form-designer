# http://www.smipple.net/snippet/IanLewis/Django%20Pickled%20Object%20Field

try:
    import cPickle as pickle
except ImportError:
    import pickle

import base64

from django.db import models

class PickledObjectField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None: return None
        if not isinstance(value, basestring): return value
        try:
            return pickle.loads(base64.b64decode(value))
        except:
            return None

    def get_db_prep_save(self, value):
        if value is None: return
        return base64.b64encode(pickle.dumps(value))
