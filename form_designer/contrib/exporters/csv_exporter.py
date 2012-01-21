from form_designer.contrib.exporters import FormLogExporterBase
from form_designer import settings
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

import csv

class CsvExporter(FormLogExporterBase):

    @staticmethod
    def export_format():
        return 'CSV'

    def init_writer(self):
        self.writer = csv.writer(self.response, delimiter=settings.CSV_EXPORT_DELIMITER)

    def init_response(self):
        self.response = HttpResponse(mimetype='text/csv')
        self.response['Content-Disposition'] = 'attachment; filename=%s.csv' %  \
            unicode(self.model._meta.verbose_name_plural)

    def writerow(self, row):
        self.writer.writerow(row)

    def export(self, request, queryset=None):
        return super(CsvExporter, self).export(request, queryset)
