# From http://vanderwijk.info/blog/adding-css-classes-formfields-in-django-templates/#comment-1193609278
# https://gist.github.com/TimFletcher/034e799c19eb763fa859

from django import template
register = template.Library()

@register.filter(name='add_css_class')
def add_css_class(field, css):
		old_class = field.field.widget.attrs.get('class', None)
		new_class = old_class + ' ' + css.strip()

		return field.as_widget(attrs={"class": new_class})

@register.filter(name='add_attribute')
def add_attribute(field, css):
		attrs = field.field.widget.attrs
		definition = css.split(',')

		for d in definition:
				if ':' not in d:
						attrs['class'] += ' ' + d
				else:
						t, v = d.split(':')
						attrs[t] = v

		return field.as_widget(attrs=attrs)