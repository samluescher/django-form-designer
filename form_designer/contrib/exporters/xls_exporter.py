from form_designer.contrib.exporters import FormLogExporterBase
from form_designer import settings
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.utils.encoding import smart_unicode

try:
    import xlwt
except ImportError:
    XLWT_INSTALLED = False
else:
    XLWT_INSTALLED = True


class XlsExporter(FormLogExporterBase):

    @staticmethod
    def export_format():
        return 'XLS'

    @staticmethod
    def is_enabled():
        return XLWT_INSTALLED 

    def init_writer(self):
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet(unicode(self.model._meta.verbose_name_plural))
        self.rownum = 0

    def init_response(self):
        self.response = HttpResponse(mimetype='application/ms-excel')
        self.response['Content-Disposition'] = 'attachment; filename=%s.xls' %  \
            unicode(self.model._meta.verbose_name_plural)

    def writerow(self, row):
        for i, f in enumerate(row):
            self.ws.write(self.rownum, i, smart_unicode(f, encoding=settings.CSV_EXPORT_ENCODING))
        self.rownum += 1

    def close(self):
        self.wb.save(self.response)

    def export(self, request, queryset=None):
        return super(XlsExporter, self).export(request, queryset)
