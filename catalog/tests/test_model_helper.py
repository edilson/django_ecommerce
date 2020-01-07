from django.urls import reverse

def helper_test_get_absolute_url(instance_tested, model, url_to_reverse):
    instance_tested.assertEqual(
        model.get_absolute_url(),
        reverse(url_to_reverse, kwargs={'slug': model.slug})
    )

def helper_test_ordering(instance_tested, model, field_ordering):
    instance_tested.assertEqual(
        model._meta.ordering[0], field_ordering
    )
