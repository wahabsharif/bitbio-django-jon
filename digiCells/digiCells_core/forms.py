from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "id-login-form"
        self.helper.form_action = ""
        self.helper.include_media = False

        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "style": "max-width: 20em;"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "style": "max-width: 20em;"}
        )

        # Define the layout, include fields and button
        self.helper.layout = Layout(
            Field("username", placeholder="Username"),
            Field("password", placeholder="Password"),
            Submit("submit", "Login", css_class="btn btn-primary mt-3"),
        )
