try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ['^form_designer\.pickled_object_field\.PickledObjectField'])
    add_introspection_rules([], ['^form_designer\.model_name_field\.ModelNameField'])
    add_introspection_rules([], ['^form_designer\.template_field\.TemplateCharField'])
    add_introspection_rules([], ['^form_designer\.template_field\.TemplateTextField'])
