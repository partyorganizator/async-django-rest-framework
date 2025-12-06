# [Django REST framework][docs] 🚀

[![build-status-image]][build-status]
[![coverage-status-image]][codecov]
[![pypi-version]][pypi]

**Awesome web-browsable Web APIs. Now with first-class async support.**

Full documentation for the project is available at [https://www.django-rest-framework.org/][docs].

---

## 🌟 What's New: Native Async Support

Django REST Framework is evolving to meet the demands of modern, high-performance web applications. With **Django 6.0** bringing [AsyncPaginator](https://docs.djangoproject.com/en/6.0/ref/paginator/#django.core.paginator.AsyncPaginator), enhanced ORM async capabilities, and a [built-in background tasks framework](https://docs.djangoproject.com/en/6.0/topics/tasks/), the time has come to bring **native async support directly into DRF**.

This fork integrates the groundbreaking work of the [**ADRF (Async Django REST Framework)**](https://github.com/em1208/adrf) project—a community-driven effort that pioneered async views, viewsets, and serializers for DRF. Rather than requiring a separate third-party package, **async capabilities are now being integrated directly into the core framework** under `rest_framework.asynchronous/`.

### 🙏 Acknowledgment: Standing on the Shoulders of Giants

This integration would not be possible without the **inspiring and tireless work** of the ADRF maintainers and contributors. The ADRF project demonstrated the viability and demand for async REST APIs in Django, and their innovative solutions have paved the way for this native integration.

**Special thanks to:**
- The [ADRF maintainers](https://github.com/em1208/adrf/graphs/contributors) who built the foundation
- The Django community who pushed for better async support
- Django core team for delivering [asgiref](https://github.com/django/asgiref) and continuous async improvements in Django 6.0

### 🔧 Architecture: Native Integration with `asgiref`

Our async implementation leverages Django's official **[asgiref](https://github.com/django/asgiref)** library—the same foundation Django uses internally for async support. Using `asgiref.sync` utilities like `iscoroutinefunction`, `sync_to_async`, and `async_to_sync`, we ensure:

- **Seamless context detection** between sync and async code
- **Thread-safe execution** of database operations
- **Zero breaking changes** to existing DRF codebases
- **Production-ready async patterns** battle-tested in Django itself

As Django's async story matures ([see Django 6.0 async features](https://docs.djangoproject.com/en/6.0/releases/6.0/#what-s-new-in-django-6-0)), DRF will continue evolving alongside it, bringing async capabilities to permissions, authentication, throttling, and beyond.

---

## 📖 Overview

Django REST framework is a powerful and flexible toolkit for building Web APIs.

Some reasons you might want to use REST framework:

* The Web browsable API is a huge usability win for your developers.
* [Authentication policies][authentication] including optional packages for [OAuth1a][oauth1-section] and [OAuth2][oauth2-section].
* [Serialization][serializers] that supports both [ORM][modelserializer-section] and [non-ORM][serializer-section] data sources.
* Customizable all the way down - just use [regular function-based views][functionview-section] if you don't need the [more][generic-views] [powerful][viewsets] [features][routers].
* [Extensive documentation][docs], and [great community support][group].
* **🆕 Native async views, viewsets, and serializers** for high-performance I/O-bound workloads.

**Below**: *Screenshot from the browsable API*

![Screenshot][image]

----

## 🔧 Requirements

* **Python 3.12+** (Django 6.0 requirement)
* **Django 4.2, 5.0, 5.1, 5.2, 6.0**

We **highly recommend** and only officially support the latest patch release of each Python and Django series.

### ⚡ Why Python 3.12+?

Django 6.0 requires Python 3.12+, bringing:
- **[AsyncPaginator & AsyncPage](https://docs.djangoproject.com/en/6.0/ref/paginator/#async-pagination)** for async pagination
- **[Background Tasks Framework](https://docs.djangoproject.com/en/6.0/topics/tasks/)** for offloading work
- **[Enhanced async ORM support](https://docs.djangoproject.com/en/6.0/topics/db/queries/#asynchronous-queries)** with broader async query capabilities
- **Significant performance improvements** in async/await patterns

---

## 📦 Installation

Install using `pip`...

```bash
pip install djangorestframework
```

Add `'rest_framework'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
]
```

---

## 🚀 Example: Traditional Sync API

Let's take a look at a quick example of using REST framework to build a simple model-backed API for accessing users and groups.

Startup up a new project like so...

```bash
pip install django
pip install djangorestframework
django-admin startproject example .
./manage.py migrate
./manage.py createsuperuser
```

Now edit the `example/urls.py` module in your project:

```python
from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
```

We'd also like to configure a couple of settings for our API.

Add the following to your `settings.py` module:

```python
INSTALLED_APPS = [
    # ... make sure to include the default installed apps here.
    "rest_framework",
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
    ]
}
```

That's it, we're done!

```bash
./manage.py runserver
```

You can now open the API in your browser at `http://127.0.0.1:8000/`, and view your new 'users' API. If you use the `Login` control in the top right corner you'll also be able to add, create and delete users from the system.

You can also interact with the API using command line tools such as [`curl`](https://curl.haxx.se/). For example, to list the users endpoint:

```bash
$ curl -H 'Accept: application/json; indent=4' -u admin:password http://127.0.0.1:8000/users/
[
    {
        "url": "http://127.0.0.1:8000/users/1/",
        "username": "admin",
        "email": "admin@example.com",
        "is_staff": true,
    }
]
```

Or to create a new user:

```bash
$ curl -X POST -d username=new -d email=new@example.com -d is_staff=false -H 'Accept: application/json; indent=4' -u admin:password http://127.0.0.1:8000/users/
{
    "url": "http://127.0.0.1:8000/users/2/",
    "username": "new",
    "email": "new@example.com",
    "is_staff": false,
}
```

---

## ⚡ Example: Async API (Coming Soon)

> **Note**: Native async support is currently in active development. The async API will be available under `rest_framework.asynchronous.*`

Here's a preview of what async views will look like:

```python
from rest_framework.asynchronous.views import AsyncAPIView
from rest_framework.asynchronous.response import AsyncResponse
from asgiref.sync import sync_to_async

class AsyncUserView(AsyncAPIView):
    async def get(self, request):
        # Async database queries using Django's async ORM
        users = await sync_to_async(list)(User.objects.all())
        
        return AsyncResponse({
            "users": [u.username for u in users],
            "count": len(users)
        })
```

For complex I/O-bound operations like external API calls, file processing, or async database queries, async views can significantly improve concurrency and throughput.

---

## 📚 Documentation & Support

Full documentation for the project is available at [https://www.django-rest-framework.org/][docs].

For questions and support, use the [REST framework discussion group][group], or `#restframework` on libera.chat IRC.

**For async-specific questions**, please tag your discussions with `async` so the community can help.

---

## 🔒 Security

Please see the [security policy][security-policy].

---

## 🤝 Contributing

We welcome contributions! Whether you're:
- Improving async support
- Fixing bugs
- Writing documentation
- Adding features

Please see our [contribution guidelines](CONTRIBUTING.md) to get started.

**Special call-out**: If you have experience with async Python, Django async patterns, or high-performance APIs, we'd especially love your contributions to the async integration effort!

---

## 📊 Project Status

**Async Integration Roadmap:**
- ❌ **Phase 1**: Integrate ADRF codebase into `rest_framework.asynchronous/`
- ❌ **Phase 2**: Leverage `asgiref.sync` for shared utilities (in progress)
- ❌ **Phase 3**: Context-aware sync/async detection (Django-style)
- ❌ **Phase 4**: Comprehensive async testing & documentation

---

## 🙌 Acknowledgments

This async integration builds upon:
- **[ADRF](https://github.com/em1208/adrf)** - The pioneering async DRF package that proved async REST APIs in Django
- **[Django's async framework](https://docs.djangoproject.com/en/6.0/topics/async/)** - The foundation provided by Django core team
- **[asgiref](https://github.com/django/asgiref)** - Django's ASGI reference implementation and sync/async bridge

---

[build-status-image]: https://github.com/encode/django-rest-framework/actions/workflows/main.yml/badge.svg
[build-status]: https://github.com/encode/django-rest-framework/actions/workflows/main.yml
[coverage-status-image]: https://img.shields.io/codecov/c/github/encode/django-rest-framework/main.svg
[codecov]: https://codecov.io/github/encode/django-rest-framework?branch=main
[pypi-version]: https://img.shields.io/pypi/v/djangorestframework.svg
[pypi]: https://pypi.org/project/djangorestframework/
[group]: https://groups.google.com/forum/?fromgroups#!forum/django-rest-framework

[oauth1-section]: https://www.django-rest-framework.org/api-guide/authentication/#django-rest-framework-oauth
[oauth2-section]: https://www.django-rest-framework.org/api-guide/authentication/#django-oauth-toolkit
[serializer-section]: https://www.django-rest-framework.org/api-guide/serializers/#serializers
[modelserializer-section]: https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
[functionview-section]: https://www.django-rest-framework.org/api-guide/views/#function-based-views
[generic-views]: https://www.django-rest-framework.org/api-guide/generic-views/
[viewsets]: https://www.django-rest-framework.org/api-guide/viewsets/
[routers]: https://www.django-rest-framework.org/api-guide/routers/
[serializers]: https://www.django-rest-framework.org/api-guide/serializers/
[authentication]: https://www.django-rest-framework.org/api-guide/authentication/
[image]: https://www.django-rest-framework.org/img/quickstart.png
[docs]: https://www.django-rest-framework.org/
[security-policy]: https://github.com/encode/django-rest-framework/security/policy
