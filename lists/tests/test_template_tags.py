from django.test import TestCase
from lists.forms import (
	DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
	ItemForm, ExistingListItemForm
)
from lists.models import Item, List
import lists.templatetags.form_tweak as Tag

class TemplateTagTest(TestCase):
	def test_template_tag_adds_css_class(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={'text': 'item text'})
		new_class = 'is-invalid'
		changed_field = Tag.add_css_class(form['text'], new_class)
		self.assertIn(new_class, changed_field)
		
	def test_template_tag_does_not_squash_existing_css_classes(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={'text': 'item text'})
		old_css = form['text'].field.widget.attrs['class']
		new_class = 'is-invalid'
		changed_field = Tag.add_css_class(form['text'], new_class)
		self.assertIn(old_css, changed_field)	