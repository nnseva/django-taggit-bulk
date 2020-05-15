[![Build Status](https://api.travis-ci.com/nnseva/django-taggit-bulk.svg?branch=master)](https://travis-ci.com/github/nnseva/django-taggit-bulk)



# Django Taggit Bulk

The [Django Taggit Bulk](https://github.com/nnseva/django-taggit-bulk) package provides an admin action to tag or untag selected instances from the model admin list page.

## Installation

*Stable version* from the PyPi package repository
```bash
pip install django-taggit-bulk
```

*Last development version* from the GitHub source version control system
```
pip install git+git://github.com/nnseva/django-taggit-bulk.git
```

## Configuration

Include the `taggit_bulk` application into the `INSTALLED_APPS` list, like:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'taggit_bulk',
    ...
]
```

Include urlconf into the project root urlconf file, like:

```python
urlpatterns = [
    ...
    url('^taggit/', include('taggit_bulk.urls')),
]
```

Install the `tag_wizard` action to list of actions for every admin class which controls model with installed `TaggableManager`.

For example, let's some your model has a `TaggableManager` installed:

`models.py`
```python
class MyModel(models.Model):
    ...
    tags = TaggableManager(
        blank=True,
        verbose_name=_('Tags'), help_text=_('A comma-separated list of tags')
    )
    ...
```

Then your `admin.py` file should look like:

```python
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import MyModel

from taggit_bulk.actions import tag_wizard


class MyModelAdmin(ModelAdmin):
    ...
    actions = [
        tag_wizard
    ]
    ...


admin.site.register(MyModel, MyModelAdmin)
```

That's it!

## Usage

Select some number of instances in your model instance list view, choose an action
"Bulk tag/untag selected objects" from the dropdown menu, and press the "Go" button.

You will see a simple dialog to setup tags for all of the selected instances.

You can either add, or remove tags for all instances, depending on the "Clear" flag in the dialog.

When deleting, if the tag is not found for a separate instance, nothing happens for this instance.

When adding, if the tag already present for a separate instance, nothing happens for this instance.

You can add or clear several tags together, just enlist them in a dialog separating by the comma.

The tags input string behaves exactly the same as for the [taggit package](https://django-taggit.readthedocs.io/en/latest/index.html).

## Customization

### settings.py

You can setup `TAGGIT_BULK_SETTINGS` attribute of the settings.py file in your project.

```python
TAGGIT_BULK_SETTINGS = {
    'session_prefix': 'tag_wizard_data',
}
```

The `session_prefix` key controls the session key where the data is stored for the dialog call.

### Access restriction

You can restrict access to the objects to be changed by the wizard overloading a `tag_wizard` action.

Just use your own action function restricting `QuerySet` passed as a parameter, and call the original
`tag_wizard` inside. For example:

```python
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import MyModel

from taggit_bulk.actions import tag_wizard


class MyModelAdmin(ModelAdmin):
    ...
    actions = [
        "tag_wizard_restricted"
    ]
    def tag_wizard_restricted(self, request, queryset):
        queryset = queryset.filter(owner=request.user)
        return tag_wizard(self, request, queryset)
    tag_wizard_restricted.short_description = tag_wizard.short_description
    ...


admin.site.register(MyModel, MyModelAdmin)
```

### Templating

You can overload the form template for the tag wizard.

Just install your own template named as one of the following:

- `'taggit_bulk_wizard_form.html'`
- `'taggit_bulk/wizard_form.html'`

You also can use the original name of the template found in the package installing it in any application following the `taggit_bulk` in the `INSTALLED_APPS`, or in the common project template directory:

- `'taggit_bulk/wizard/form.html'`
