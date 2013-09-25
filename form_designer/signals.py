from django import dispatch

designedform_submit = dispatch.Signal(providing_args=["designed_form"])
designedform_success = dispatch.Signal(providing_args=["designed_form"])
designedform_error = dispatch.Signal(providing_args=["designed_form"])
designedform_render = dispatch.Signal(providing_args=["designed_form"])
