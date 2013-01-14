Permissive CSRF for Django
==========================

Are you using Django and trying to POST from a normal HTTP page 
to an HTTPS, only to be hit by the puzzling 
*"Referer checking failed - http://example.com/ does not match https://example.com/"*?

First, you should know that there are `good reasons why this is happening`_,
and in understanding them you can decide whether trading off security 
for convenience is worth it.

Second, the best way to solve this issue is to 
use HTTPS on all your pages and with packages like `django-sslify`_
you have no excuse not to.

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


*Prepend* PermissiveCSRF to your ``MIDDLEWARE_CLASSES``::

    MIDDLEWARE_CLASSES = (
        'permissivecsrf.middleware.PermissiveCSRFMiddleware',
        # ...
    )

**Note:** PermissiveCSRF works with `django-sslify`_ too. Although the order doesn't really matter,
you probably want PermissiveCSRF after the django-sslify inclusion::


    MIDDLEWARE_CLASSES = (
        'sslify.middleware.SSLifyMiddleware',
        'permissivecsrf.middleware.PermissiveCSRFMiddleware',
        # ...
    )


How does it work?
-----------------

The `Django CSRF middleware`_ performs an extra-check if the request is over HTTPS to 
ensure that the request came from the same site, i.e. that 
the referrer (HTTP-Referer header) matches the current site.

In other words, in ensures that the call to https://example.com/account/login
came from another page of https://example.com/. As such, if you put your login 
form on your non-secure homepage, http://example.com/, but use a secure target 
for your form's *action* attribute, ``<form action="https://example.com/account/login" method="POST">``,
Django's check will fail because::

'http://example.com/' != ('https://%s/` % request.get_host())

However, Django will not perform the CSRF check at all if the ``request`` object has 
an attribute ``_dont_enforce_csrf_checks`` set to True. That's what PermissiveCSRF relies on:
if the request came from the same site over HTTP it sets ``_dont_enforce_csrf_checks``
to True, thus telling the Django CSRF middleware to skip the CSRF check for that request.

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
2. Restrict the check for only a set of URLs, e.g. login pages.


.. _`good reasons why this is happening`: 

Why is this CSRF HTTP/HTTPS madness happening?
----------------------------------------------

The *tl;dr* answer is: to prevent Man-in-the-Middle (MITM) attacks when using HTTPS, because HTTPS headers are encrypted.

The gist of why this happens is explained in point #4 of the `How it works`_ section of the Django documentation on
Cross Site Request Forgery (emphasis mine):

    4. In addition, for HTTPS requests, strict referer checking is done by CsrfViewMiddleware. 
    This is necessary to address a Man-In-The-Middle attack that is possible under HTTPS 
    when using a session independent nonce, due to the fact that HTTP 'Set-Cookie' headers 
    are (unfortunately) accepted by clients that are talking to a site under HTTPS. 
    **(Referer checking is not done for HTTP requests because the presence of the Referer header is not reliable enough under HTTP.)**

In other words, because the HTTPS headers are encrypted, the *HTTP-Referer* header is resilient 
against MITM attacks, so it can be safely used to check and make sure the CSRF cookie or fields
is originated by the same site that served the page.

The same check could be made on HTTP calls as well, but since HTTP headers are not encrypted, they 
could be easily faked and thus the check would be a useless placebo.

This explanation is also present, in comment form, in this f92a21daa7_ commit by spookylukey aka Luke Plant,
and further detailed by him in a reply_ to a complaint about the strictness of CSRF Referer check 
on the django-developers maillist.

The take away from all this should be: in production use HTTPS (see `django-sslify`_). Period.

**Seriously, don't use PermissiveCSRF in production. It's a bad idea.** And I should know, I have `plenty of them`_.


.. _`django-sslify`: https://github.com/rdegges/django-sslify
.. _`Django CSRF middleware`: https://github.com/django/django/blob/master/django/middleware/csrf.py
.. _`Django 13849`: https://code.djangoproject.com/ticket/13849
.. _reply: https://groups.google.com/d/msg/django-developers/IgWK2vEePtY/R1r3Im4x3UMJ
.. _f92a21daa7: https://github.com/django/django/commit/f92a21daa7
.. _`How it works`: https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#how-it-works
.. _`plenty of them`: http://philipm.at/
