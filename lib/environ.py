import os
import sys
import logging

ROOT_PATH = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))
DATASTORE_PATH = os.path.join(ROOT_PATH, 'tmp', 'data')


def setup_environ():

    # lib
    sys.path.insert(0, os.path.join(ROOT_PATH, 'lib'))

    # SDK (this will be simpler if SDK is in the codebase)
    sdk_path = None
    for path in os.environ.get('PATH').split(os.pathsep):
        if 'dev_appserver.py' in os.listdir(path):
            test_path = os.path.join(path, 'dev_appserver.py')
            sdk_path = os.path.dirname(
                os.readlink(test_path) if os.path.islink(test_path) else test_path)
            break

    if not sdk_path:
        logging.critical("Can't find sdk_path")
        sys.exit(1)
    sys.path.insert(0, sdk_path)

    # Use dev_appserver to set up the python path
    from dev_appserver import fix_sys_path
    fix_sys_path()

    try:
        from google.appengine.tools import dev_appserver as tools_dev_appserver
    except ImportError:
        from google.appengine.tools import old_dev_appserver as tools_dev_appserver
    from google.appengine import dist

    # Parse `app.yaml`
    appinfo, url_matcher, from_cache = tools_dev_appserver.LoadAppConfig(
        ROOT_PATH, {}, default_partition='dev')
    app_id = appinfo.application

    # Useful for later scripts
    os.environ['APPLICATION_ID'] = app_id
    os.environ['APPLICATION_VERSION'] = appinfo.version

    # Third party libraries on the path
    if appinfo.libraries:
        for library in appinfo.libraries:
            try:
                dist.use_library(library.name, library.version)
            except ValueError, e:
                if library.name == 'django' and library.version == '1.4':
                    # Work around an SDK issue
                    sys.path.insert(0, os.path.join(sdk_path, 'lib', 'django-1.4'))
                else:
                    logging.warn('Unsupported library:\n%s\n' % e)

            # Extra setup for django
            if library.name == 'django':
                try:
                    import settings
                    from django.core.management import setup_environ
                    setup_environ(settings, original_settings_path='settings')
                except ImportError:
                    logging.error("Could not import django settings")
