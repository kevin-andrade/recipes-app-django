from collections import defaultdict
from django import forms
from django.core.exceptions import ValidationError

from authors.validators import AuthorRecipeValidator
from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('title'), 'class', 'span-2')
        add_attr(self.fields.get('description'), 'class', 'span-2')
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2',
                }
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutes', 'Minutes'),
                    ('Hours', 'Hours')
                )
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Slices', 'Slices'),
                    ('Pieces', 'Pieces'),
                    ('Portions', 'Portions'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorRecipeValidator(
            data=self.cleaned_data,
            ErrorClass=ValidationError
        )
        return super_clean
