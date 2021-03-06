Tech Overview
=============

cc.engine uses a very minimalist "web framework"... perhaps more
correctly, it does not use a framework at all, and instead provides a
very minimal WSGI application that pulls together several generic
libraries.  Despite this, the structure of the system is very similar
to a Pylons or a Django application.  If you have written a Pylons of
Django application before, all of this should look fairly familiar
with little extra information.

(However, if you are really curious about how this works, or would
like to try writing your own framework or minimalist un-framework web
application, I recommend reading `Another Do-It-Yourself Framework
<http://pythonpaste.org/webob/do-it-yourself.html>`_)


Components used
---------------

The components that are used are:

* `Zope Page Templates <http://pypi.python.org/pypi/zope.pagetemplate/3.5.0>`_
  for templating
* `Routes <http://routes.groovie.org/>`_ for url dispatching
* `WebOb <http://pythonpaste.org/webob/>`_ for making request objecst
  within WSGI pleasant.
* `Nose <http://somethingaboutorange.com/mrl/projects/nose/0.11.1/>`_
  for nice unit testing


How the app is structured
-------------------------

The meat of the application is all housed in cc/engine/.  Several
parts of the application are broken into "subapplications", such as
cc/engine/licenses/, which houses the routing information and views
for the actual licenses and their deeds, and cc/engine/chooser/, which
houses the views and routing information for the license chooser.


WSGI Application
~~~~~~~~~~~~~~~~

The WSGI application is housed in cc/engine/app.py.

It is a very minimalist WSGI application... it simply takes an
incoming request, passes the path to the routing system and sees if it
can find a result.  If it can't find a result at that URL, but can
find one if it appends a slash, it'll redirect to that url (thus
adding Django-style APPEND_SLASH=True functionality).  The application
will then pass a WebOb Request object to the view/controller specified
by the matching route's "controller" field.


URL Dispatching / Routing
~~~~~~~~~~~~~~~~~~~~~~~~~

The root mapper for routes is set up in the cc.engine.routing module
as the "mapping" global variable.  Some routes may be provided here,
but the majority are actually housed in the "subapplication"
routing.py files.  For example, routing for the chooser is provided in
cc/engine/chooser/routing.py and routing for the license is provided
in cc/engine/chooser/license.py.  These are then "pulled in" to the
global routing mapper via the mapping.extend() method.  The "results"
of the routing match will then be appended to the webob.Request object
that is passed to the view as the "matchdict" attribute.  See the
`documentation for the Routes library
<http://routes.groovie.org/manual.html>`_ to find out more about how
this works.

Generally, you can provide any information here, but there is one
attribute which is *required* as part of cc.engine's WSGI application:
"controller".  This field should be structured as:
"module.path.to:controller_name", where the portion before the colon
is the module and the portion after the colon is the
function/method/callable object instance that is to process this
method.


Views / Controllers
~~~~~~~~~~~~~~~~~~~

Views / controllers are simply methods.  They must accept a single
method, "request", which will be the webob.Request method passed from
the WSGI application.  In turn, they are expected to return a
webob.Response object.  (Or, in the case of an redirect or error,
webob.exc.HTTPTemporaryRedirect or something else from webob.exc.)

Views technically *can* be placed anywhere, but by convention you
should probably put them in a 'views' file (ie,
cc.engine.license.views, or cc.engine.chooser.views).


Templates
~~~~~~~~~

Templates are kept in cc/engine/templates/.  All templates are
currently Zope Page Template based.

To load a template, use the cc.engine.util.get_zpt_template() method.
Pass in a filename that is relative to cc/engine/templates/.  For
example, to import the template at
cc/engine/templates/myth_profiles/phoenix.zpt run::

  phoenix_template = util.get_zpt_template('myth_profiles/phoenix.zpt')

If you know the target language that your template should render to,
pass that in as the second argument (see I18N below).

To render, use::

  context = {
      'request': request,
      'some_other_context_var': 'bla bla bla'}
  phoenix_template.pt_render(context)


cc.engine tries to be fairly minimal in the amount of Zope machinery
it pulls in (ie, currently it does not use the zope component system),
so currently if your template relies on metal macros, you should
provide those in the context like so::

  context = {
      'request': request,
      'base_template': util.get_zpt_template(
          'myth_profiles/base.pt')}

Then in your template, use metal:use-macro like::

  <html xmlns="http://www.w3.org/1999/xhtml"
        xmlns:tal="http://xml.zope.org/namespaces/tal"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        xmlns:metal="http://xml.zope.org/namespaces/metal"
        metal:use-macro="base_template/macros/page"
        i18n:domain="cc_org">

Obviously replacing "page" with whatever macro is appropriate.

Assets
~~~~~~

Staticdirect: finding static files dynamically
++++++++++++++++++++++++++++++++++++++++++++++

To pull in an asset (such as javascript, images, css), you just need
to use request.staticdirect.  For example, in
templates/licenses/standard_deed.pt::

  <img tal:attributes="src python:request.staticdirect('images/information.png')"
       i18n:attributes="alt"
       alt="Information" />

Provided you're somewhat familiar with zpt, what's happening here
should be very clear: the src attribute is being set with the value
returned by request.staticdirect('images/information.png').

For CC, in general you can look for the resources you might need in
cc/engine/resources.

If you are setting up an install or development version of cc.engine,
you may need/want to configure the staticdirector as part of the paste
config file (assuming you are using paste).  (Note: you probably don't
*need* to read this section, this package comes with both a deployment
and development config file that probably solves this for you.)  There
are two configuration options you can set.  The first one is
"direct_remote_path"::

  [app:ccengine]
  use = egg:cc.engine#ccengine_app
  direct_remote_path = /statik/

In that example, request.staticdirect('images/information.png') will
resolve to "/statik/images/information.png".  You can also use a full
domain name here if you like; setting direct_remote_path to
http://assets.example.org/statik/ would resolve to
"http://assets.example.org/statik/images/information.png".

However, you may need to be able to handle multiple urls for the
different primary "sections" of media that are hosted under separate
parent urls, you may wish to use direct_remote_paths::

  [app:ccengine]
  use = egg:cc.engine#ccengine_app
  direct_remote_paths =
     images /images/                    
     includes /includes/
     cc3 /wp-content/themes/cc3
     cc4 /wp-content/themes/cc4
     cc5 /wp-content/themes/cc5

Now the URL returned is dependent on the first directory of the
requested URL.  Eg: request.staticdirect('images/information.png')
will now return "/images/information.png" but
request.staticdirect('cc5/style.css') will yield
"/wp-content/themes/cc5/style.css".  You might want to do this, for
example, if you are trying to mirror the creativecommons.org setup,
where the stylesheets used point at very specific directories that
don't all fall under the same parent URL.  (This is what the default
development INI file does.)


Static serving for development
++++++++++++++++++++++++++++++

If you're in development mode and using the development paste config
file, this should be handled for you, but for the sake of
thoroughness, here is part of the config file::

  [composite:main]
  use = egg:Paste#urlmap
  / = ccengine
  /images = images_serve
  /includes = includes_serve
  /wp-content/themes/cc3 = cc3_serve
  /wp-content/themes/cc4 = cc4_serve
  /wp-content/themes/cc5 = cc5_serve

  [app:ccengine]
  use = egg:cc.engine#ccengine_app
  direct_remote_paths =
     images /images/                    
     includes /includes/
     cc3 /wp-content/themes/cc3
     cc4 /wp-content/themes/cc4
     cc5 /wp-content/themes/cc5

  [app:images_serve]
  use = egg:cc.engine#static_app
  resource_path = cc.engine:resources/images

  [app:includes_serve]
  use = egg:cc.engine#static_app
  resource_path = cc.engine:resources/includes

  [app:cc3_serve]
  use = egg:cc.engine#static_app
  resource_path = cc.engine:resources/cc3

  [... cut off here ...]

(Note that this may make more sense if you read the `Paste Deploy
<http://pythonpaste.org/deploy/>`_ documentation.)

What we are doing here is using Paste's composite application setup
stuff to mount things under different URLs.  In this case, we are
mounting the main app under /, and then are setting up separate serve
points for the separate sections of the site.  We then use a wrapper
for serving static content via the `static package
<http://lukearno.com/projects/static/>`_.


I18N
~~~~

Internationalization is handled inside of the cc.i18npkg package.
This package does two things:

* It pulls in the i18n.git package as a submodule and makes it
  accessible via package_resources so that other python modules don't
  have to include that submodule redundancy
* Provides a module that you can import which "sets up"
  internationalization: cc.i18npkg.ccorg_i18n_setup

As for ZPT, If you use util.get_zpt_template to fetch templates, you
don't need to think about it except for passing in the target language
as the second argument in the .pt_render method.

Under the hood, due to the way ZPT is implemented, some manual
subclassing was necessary to get ZPT working with
internationalization.  Unfortunately, while ZPT is fairly decoupled
from Zope in most ways, as in terms of i18n the functionality inside
of ZPT is not provided "out of the box"... when you use the entire
framework of Zope itself, Zope does somesubclassing and adds the
translation feature manually.  And so, we must also do the same.
Since cc.license also does this, these subclasses are actually
implemented in cc.license.formatters.pagetemplate for now.


Models
~~~~~~

Surprise!  Cc.engine is not (at least presently) a database-driven
application.  The only "models" used are actually the licenses pulled
from the RDF files via cc.license.  See the cc.license docs to figure
out how this works.

The one thing that may be interesting is that there is a decorator in
cc.engine.decorators called get_license.  If you pass in "code",
"jursidiction" and "version" to the request's matchdict via your
routes or whatever, this decorator will automatically retreive that
license for you and pass it in as the first argument of your view.


Tests
~~~~~

Tests go in the cc/engine/tests/ directory.  Either add to an existing
test_*.py module or add your own if appropriate.  Tests are set up in
the usual Nose tests fashion.


Checking ZPT context with unit tests
++++++++++++++++++++++++++++++++++++

If you want to look at the context of a request, make sure at the top
of your tests module that you set::

  from cc.engine import util
  util._activate_zpt_testing()

Next, after you render your test, you should do the following::

  context = util.ZPT_TEST_TEMPLATES.pop(
      util.full_zpt_filename('path/to/mytemplate.pt'))

This will give you access to the same dictionary that was last passed
into a a template the last time it was rendered with .pt_render.
