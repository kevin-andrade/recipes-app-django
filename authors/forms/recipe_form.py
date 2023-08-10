from collections import defaultdict
from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.string_positive_number import is_positive_nummber


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
        cd = self.cleaned_data

        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Must have at least a 5 chars.')

        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get('preparation_time')

        if not is_positive_nummber(field_value):
            self._my_errors[field_name].append(
                'Must be a positive number'
            )

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get('servings')

        if not is_positive_nummber(field_value):
            self._my_errors[field_name].append(
                'Must be a positive number'
            )

        return field_value
