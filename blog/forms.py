from django import forms
from blog.models import Comment
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Row
from crispy_forms.bootstrap import FormActions


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.show_form_labels = False
            self.fields['content'].widget.attrs = {'rows': 5, 'cols': 33}

            self.helper.layout = Layout(
            Row(
                FloatingField('content',css_class="form-group col-12", rows="333", cols="33"), css_class="form-row", placeholder="Leave a Comment..."),
            FormActions(
                Submit(name="post-comment", value='Post Comment', css_class="btn btn-outline"),  css_class="form-row"
)
            )
 
    class Meta:
        model = Comment 
        fields = ["content"]
