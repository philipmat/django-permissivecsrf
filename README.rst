Permissive CSRF for Django
==========================

Are you using Django and trying to POST from a normal HTTP page 
to an HTTPS on only to be hit by the puzzling 
*"Referer checking failed - http://example.com/ does not match https://example.com/"*?

First, you should know that there are `good reasons why this is happening`_,
and in understanding them you can decide whether trading off security 
for convenience is worth it.

Second, you should know that the best way to solve this issue is to 
use HTTPS on all your pages, and with packages like `django-sslify`_
you have no excuse not to use it.

If, after reading all the above, you're still set on making the trade,
here is how to use PermissiveCSRF in your Django site.


Installation
------------

Install from PyPi::
    
    pip install django-permissivecsrf

.. Or install the version currently in development using pip
      pip install -e git+git://github.com/philipmat/django-permissivecsrf/tarball/master#egg=django-permissivecsrf-dev


Usage
-----

Modify your Django ``settings.py`` file and add ``permissivecsrf`` to 
the list of installed applications::

    INSTALLED_APPS = (
        # ...
        'permissivecsrf',
    )


**Prepend** PermissiveCSRF to your ``MIDDLEWARE_CLASSES``::

    MIDDLEWARE_CLASSES = (
        'permissivecsrf.middleware.DisableCSRFMiddleware',
        # ...
    )

PermissiveCSRF works with `django-sslify`_ too. Although the order doesn't really matter,
you probably want PermissiveCSRF after the ``django-sslify`` inclusion::


    MIDDLEWARE_CLASSES = (
        'sslify.middleware.SSLifyMiddleware',
        'permissivecsrf.middleware.DisableCSRFMiddleware',
        # ...
    )


How does it work?
-----------------

The `Django CSRF middleware`_ perform an extra-check if the request is over HTTPS to 
ensure that the request came from the same site, i.e. that 
the referrer (``HTTP-Referer`` header) matches the current site.

On other words, in ensures that the call to ``https://example.com/account/login``
came from another page of ``https://example.com/``. As such, if you put your login 
form on your un-secured homepage, ``http://example.com/``, but use a secure target 
for your form's *action* attribute, ``form action="https://example.com/account/login"``,
Django's check will fail because: 
``'http://example.com/' != ('https://%s/` % request.get_host())``.

However, Django will not perform the CSRF check at all if the ``request`` object has 
an attribute ``_dont_enforce_csrf_checks`` set to True. That's what PermissiveCSRF relies on:
if the request came from the same site, regardless the protocol, it sets ``_dont_enforce_csrf_checks``
to True thus telling the Django CSRF middleware to skip the CSRF check for that request.

This only happens if:

* ``DEBUG == True``. Your production server should always be HTTPS;
* The ``HTTP-Referer`` header is present;
* The request is for an HTTPS URL (i.e. ``request.is_secure() == True``);
* and the referrer uses HTTP. 

In all other cases it defers to Django for normal processing.


Tests? Yes!
-----------
::
    $ git clone https://github.com/philipmat/django-permissivecsrf
    $ cd django-permissivecsrf
    $ virtualenv --distribute venv
    $ . venv/bin/activate
    $ python setup.py develop
    ...
    $ python manage.py test permissivecsrf
    ...
    Creating test database for alias 'default'...
    .....
    ----------------------------------------------------------------------
    Ran 5 tests in 0.002s

    OK
    Destroying test database for alias 'default'...



How to make it even better?
---------------------------

aka *plans for the future*

1. PermissiveCSRF should still perform the CSRF check rather than instruct Django 
   to skip it altogether.
1. Restrict the check for only a set of URLs, e.g. login pages.


.. _good-reasons-why-this-is-happening:

Why is this CSRF HTTP/HTTPS madness happening?
----------------------------------------------




.. django-sslify: https://github.com/rdegges/django-sslify
.. Django CSRF middleware: https://github.com/django/django/blob/master/django/middleware/csrf.py
