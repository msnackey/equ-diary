# commenting this out to prevent them showing in PRs.
# show again when we support new python versions
# E0001 = {
#     'report': "Syntax error",
#     'first': "Syntax error",
#     'short': "Syntax error",
# }

# C1xxx is for dependencies

C2000 = {
    "report": "{name}: Nullable string field",
    "first": (
        "`null=True` on a string field causes inconsistent data types because the value can be either `str` "
        'or `None`. This adds complexity and maybe bugs, but can be solved by replacing `null=True` with `default=""`.'
    ),
    "short": 'consider replacing `null=True` with `default=""` (and `blank=True` to pass validation checks).',
}

C2001 = {
    "report": "Model has too many fields ({count}); consider splitting model",
    "first": "This model has lots of fields. Consider splitting into multiple models.",
    "short": "consider splitting into multiple models.",
}

C2002 = {
    "report": "{name}: {option}={value} is redundant",
    "first": "`{value}` is the default value Django uses for `{option}`, so `{option}={value}` can be removed.",
    "short": "redundant default arguments can be removed.",
}

C2003 = {
    "report": "{name}: Field is nullable but blank=False",
    "first": (
        "Expect unwanted behavior if `null` and `blank` are different values: `null` controls if the "
        "_database_ allows no value for `{name}` and `blank` controls if the _application_ allows no value for "
        "`{name}`. Consider setting `null` and `blank` to the same value for `{name}`."
    ),
    "short": "Maybe setting `null` and `blank` to the same value.",
}

C2004 = {
    "report": "{name}: uses brittle {option}",
    "first": (
        "`{option}` is brittle:\n"
        "* The constraint is not enforced by the database.\n"
        "* It is checked during `Model.validate_unique()` and so will not occur if `Model.save()` is called without first calling `Model.validate_unique()`.\n"
        "* The constraint will not be checked even if `Model.validate_unique()` is called when using a `ModelForm` that does no include a field involved in the check.\n"
        "* Only the date portion of the field will be considered, even when validating a `DateTimeField`."
    ),
    "short": "{option} is brittle.",
}

C2005 = {
    "report": "{name}: ForeignKey missing related_name",
    "first": (
        "Django automatically creates a `related_name` if it's not set. If it were set then a more readable "
        "and explicit relationship is set up."
    ),
    "short": "with an explicit `related_name` would be better.",
}

C2006 = {
    "report": "{name}: Using CharField with huge max_length instead of TextField",
    "first": "`TextField` might be better used here, instead of `CharField` with a huge `max_length`.",
    "short": "consider using a `TextField`.",
}

C2008 = {
    "report": "{name}: NullBooleanField instead of BooleanField with null=True and default=None",
    "first": (
        "`NullBooleanField` is discouraged and will likely to be deprecated in a future version of Django. "
        "Instead use BooleanField(null=True, blank=True)."
    ),
    "short": "consider not using `NullBooleanField`.",
}


C2011 = {
    "report": "{name}: primary_key=True should imply unique=True",
    "first": (
        "If `primary_key` is `True` then `unique` should be `True` too otherwise the field cannot uniquely "
        "identity the database record."
    ),
    "short": "`primary_key` should be unique.",
}

C3000 = {
    "report": "Many models ({count}); consider splitting application",
    "first": "There's a lot of models here. Consider splitting into multiple files.",
    "short": "consider splitting.",
}

C3002 = {
    "report": "{before} should come before {after}",
    "first": "According to Django internal style guide, `{before}` should come before `{after}`.",
    "short": "`{before}` should come before `{after}`.",
}

C3003 = {
    "report": "{count} models have common prefix ({prefix}) - rename them or split application.",
    "first": "`{prefix}` model prefix is used quite a lot. Maybe split the models into multiple files.",
    "short": "consider splitting into multiple files.",
}

C4000 = {
    "report": "{before} should come before {after}",
    "first": "`{before}` should come before `{after}` otherwise it may not work as expected.",
    "short": "`{before}` should come before `{after}`.",
}

C4001 = {
    "report": "Non-absolute directory {value} in TEMPLATE_DIRS",
    "first": "`TEMPLATE_DIRS` should use absolute paths otherwise it may not work as expected.",
    "short": "should use absolute paths.",
}

C4002 = {
    "report": "{value} in TEMPLATE_DIRS should use forward slashes",
    "first": "`TEMPLATE_DIRS` should not use backward slashes. Even on Windows use forward slashes.",
    "short": "should use forward slashes",
}

C4003 = {
    "report": "{name} should be near the end of middlewares",
    "first": "`{name}` should be near the end of middleware otherwise it may not work as expected.",
    "short": "`{name}` should be in the end.",
}

C4004 = {
    "report": "{name} should be near the start of middlewares",
    "first": "`{name}` should be near the start of middleware otherwise it may not work as expected.",
    "short": "`{name}` should be near the start.",
}

C4005 = {
    "report": "{option}={value} is the django default. Consider deleting this",
    "first": "`{value}` is the default value Django uses for `{option}`, so can be removed.",
    "short": "this is redundant.",
}

C4006 = {
    "report": "`from django.conf import settings is preferable to importing the settings file directly.",
    "first": (
        "It's preferable to use `from django.conf import settings` instead of importing from `{modpath}` directly. "
        "Importing directly can trigger a race condition when your code imports settings before the app is ready.\n\n"
        "Also, using `django.conf.settings` simplies working with settings in tests as you can then use Django's "
        "`modify_settings` and `django-pytest`'s `settings` fixture, which rely on the code using "
        "`django.conf.settings`."
    ),
    "short": "`from django.conf import settings` would be better.",
}

C4007 = {
    "report": "MIDDLEWARE missing SecurityMiddleware",
    "first": (
        "`MIDDLEWARE` is missing `django.middleware.security.SecurityMiddleware` so the follow security settings will "
        "have no effect: `SECURE_HSTS_SECONDS`, `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER`, "
        "`SECURE_REFERRER_POLICY`, and `SECURE_SSL_REDIRECT`."
    ),
    "short": "`MIDDLEWARE` missing `django.middleware.security.SecurityMiddleware`.",
}

C4008 = {
    "report": "MIDDLEWARE missing XFrameOptionsMiddleware",
    "first": (
        "`MIDDLEWARE` is missing `django.middleware.clickjacking.XFrameOptionsMiddleware` so the website is not "
        "protected against click jacking"

    ),
    "short": "`MIDDLEWARE` missing `django.middleware.clickjacking.XFrameOptionsMiddleware`.",
}

C4009 = {
    "report": "MIDDLEWARE missing CsrfViewMiddleware",
    "first": "`MIDDLEWARE` is missing `django.middleware.csrf.CsrfViewMiddleware` so the website is not CSRF attacks",
    "short": "`MIDDLEWARE` missing `django.middleware.csrf.CsrfViewMiddleware`.",
}

C4010 = {
    "report": "SECURE_HSTS_SECONDS not set",
    "first": (
        "Consider setting `SECURE_HSTS_SECONDS` if the website is to be accessed exclusively via HTTPS. This reduces "
        "the chance of a Man In The Middle attack because modern browsers will block HTTP requests to your website. "
        "Start with a small number and increase once you're confident HTTPS works on your website."
    ),
    "short": "consider setting `SECURE_HSTS_SECONDS`.",
}

C4011 = {
    "report": "SECURE_HSTS_INCLUDE_SUBDOMAINS not set",
    "first": (
        "Consider setting `SECURE_HSTS_INCLUDE_SUBDOMAINS` if all subbdomains of the website are to be accessed "
        "exclusively via HTTPS. This extends the HSTS protection to subdomains too, further reducing the chance of a "
        "Man In The Middle attack because modern browsers will block HTTP requests to your website. "
    ),
    "short": "consider setting `SECURE_HSTS_INCLUDE_SUBDOMAINS`.",
}

C4012 = {
    "report": "SECURE_CONTENT_TYPE_NOSNIFF not set",
    "first": (
        "Consider setting `SECURE_CONTENT_TYPE_NOSNIFF` to prevent the security hole that if the MIME type is missing "
        "from a response's `content-type` header then the browser will infer the MIME type based on the content and "
        "so execute any nefarious javascript/html that a bad actor managed to upload to your website."
    ),
    "short": "consider setting `SECURE_CONTENT_TYPE_NOSNIFF`.",
}

C4013 = {
    "report": "SECURE_SSL_REDIRECT not set",
    "first": (
        "Consider setting `SECURE_SSL_REDIRECT` to prevent users from accessing the website over HTTP. HTTP "
        "connections allow bad actors to intercept passwords and session cookies, and to easily change the contents "
        "of the request or response."
    ),
    "short": "consider setting `SECURE_SSL_REDIRECT`.",
}

C4014 = {
    "report": "SESSION_COOKIE_SECURE not set",
    "first": (
        "Consider setting `SESSION_COOKIE_SECURE` to prevent cookies from being sent over non HTTPS connections. "
        "Cookies sent over insecure HTTP connections can be intercepted by hackers."
    ),
    "short": "consider setting `SESSION_COOKIE_SECURE`.",
}

C4015 = {
    "report": "SESSION_COOKIE_HTTPONLY not set",
    "first": "Consider setting `SESSION_COOKIE_HTTPONLY` to prevent cookies from being vulnerable to XSS attacks.",
    "short": "consider setting `SESSION_COOKIE_HTTPONLY`.",
}

C4016 = {
    "report": "CSRF_COOKIE_SECURE not set",
    "first": "Consider setting `CSRF_COOKIE_SECURE` to prevent the CSRF cookies from being vulnerable to packet sniff attack.",
    "short": "consider setting `CSRF_COOKIE_SECURE`.",
}

C4017 = {
    "report": "SECURE_HSTS_PRELOAD  not set",
    "first": (
        "Consider setting ` SECURE_HSTS_PRELOAD ` to facilitate adding your website to the "
        "<a href='https://hstspreload.org/' target='_blank'>browser preload list</a>."
    ),
    "short": "consider setting `SECURE_HSTS_PRELOAD`.",
}

C5000 = {
    "report": "Admin class {name} not in admin.py",
    "first": "The Django convention is to put `{name}` in `admin.py` otherwise circular imports can happen.",
    "short": "move to `admin.py`.",
}

C7000 = {
    "report": "Use {{% url ... %}} intead of a hard-coded URL.",
    "first": (
        "Using `{{% url ... %}}` in templates is preferable because it makes updating urls easier later, and "
        "raises an error loudly if the url does not exist, thus making it less likely a malformed hyperlink "
        "causes a 404 on production."
    ),
    "short": "hard-coded URL used.",
}

C6000 = {
    "report": "Expected {pattern} to resolve to {expected} but got {actual}.",
    "first": "{pattern} should hit `{expected}`, but actually `{actual}` is hit because the URL rule is too broad.",
    "short": "{pattern} should hit `{expected}`, but actually `{actual}` is hit",
}

C6001 = {
    "report": "URL name is not unique",
    "first": (
        'URL names must be unique but multiple `urls.py` entires are called `{name}`. If `reverse("{name}")` '
        "or `{{% url {name} %}}` is ran then only one of those urls will be returned. The user will probably be sent "
        "to the wrong view."
    ),
    "short": "The url name should be unique.",
}

C6002 = {
    "report": "Using reverse_lazy when reverse would be better",
    "first": (
        "`reverse{signature}` would be better here because the url only need to be lazy if it's being reversed "
        "before `URLConf` has been loaded, such as being defined at module level."
    ),
    "short": "`reverse{signature}` would be better.",
}

C7001 = {
    "report": "Use {{% static ... %}} intead of a hard-coded URL.",
    "first": (
        "Hard-coding `{path}` is brittle because the place the files are stored depends on the "
        "`STATICFILES_STORAGE` used - so if in prod the storage backend uploads to S3 or even renames the "
        "file then this hard-coded URL will break. Using `{{% static ... %}}` solves that as it knows exactly "
        "where the files are stored."
    ),
    "short": "hard-coded static URL used.",
}

C8000 = {
    "report": "Using directly imported models instead of apps.get_model",
    "first": (
        "It's better to use `apps.get_model` instead of working on directly-imported `{name}`.\n\n"
        "Directly importing models in migrations is flaky and in a few migrations time will probably fail because "
        "during migrations the code in models.py is out of step with the database schema: the `models.py` can "
        "have a field defined that does not yet exist in the database because the required migration has not yet ran."
    ),
    "short": "use `apps.get_model(...)` instead of importing `{name}`",
}

C8001 = {
    "report": "Migrations missing reverse so migration cannot be reversed",
    "first": (
        "Unless a `reverse_code` function is provided then the migration cannot be ran backwards. Django will throw "
        "an error if you try. This complicates rolling back production to the previous version of the app.\n\n"
        "Solve this by either explicit writing a function that undoes the `fowards` mutations, or simply "
        "do `migrations.RunPython({forwards_name}, migrations.RunPython.noop)`."
    ),
    "short": "consider doing `migrations.RunPython({forwards_name}, migrations.RunPython.noop)`.",
}

C9000 = {
    "report": "Using len(queryset) instead of queryset.count()",
    "first": (
        "`len(queryset)` reads all the records from the database and checks the length at application level. "
        "It would probably be more efficient to do this at database level via `queryset.count()`."
    ),
    "short": "`queryset.count()` may be better",
}

C9001 = {
    "report": "Using model.related_field.id instead of model.related_field_id",
    "first": (
        "`{me}.{related_name}.{pk_attribute}` performs a database read when `{pk_attribute}` is evaluated. You could "
        "take advantage of Django's caching of related fields by using `{me}.{related_name}_id`, which "
        "does not do a database read."
    ),
    "short": "consider `{me}.{related_name}_id`",
}

C9002 = {
    "report": "Comparing queryset.count() where checking queryset.exists() would be better",
    "first": "Comparing `{queryset}.count()` is less efficient than checking `{queryset}.exists()`",
    "short": "consider `{queryset}.exists()`",
}

C9003 = {
    "report": "Checking queryset truthiness where queryset.exists() may be better",
    "first": (
        "Checking `{queryset}` truthiness is less efficient than checking `{queryset}.exists()` or "
        "`{queryset} is not None`. Checking queryset truthiness evaluates the queryset, therefore reading the records "
        "from the database."
    ),
    "short": "consider `{queryset}.exists()`",
}
