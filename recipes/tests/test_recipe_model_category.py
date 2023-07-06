from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    def test_recipe_category_model_string_representation_is_name_field(self):
        needed = 'Testing Category'
        self.category.name = needed
        self.assertEqual(
            str(self.category),
            needed
        )

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'K' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
