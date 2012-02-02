import os
import sys

#DEBUG = True
DEBUG = False

cwd = os.getcwd()
site_name = 'active'
site_home = os.path.join(cwd, site_name)
env_bin = os.path.join(cwd, site_name, 'env', 'bin')

cmd = 'source %s' % (os.path.join(env_bin, 'activate'))
os.system(cmd)

# Invole the virtualenv
INTERP = '%s' % (os.path.join(env_bin, 'python'))
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Set up the path
sys.stdout = sys.stderr
sys.path.append(site_home)
sys.path.append(os.path.join(site_home, '..'))
sys.path.append(os.path.join(site_home, 'project'))
sys.path.append(os.path.join(env_bin, '/lib/python2.6/site-packages'))
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.project.settings" % site_name

# Set up the django application
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


#Define a test application to check that the ErrorMiddleware is working
def testapplication(environ, start_response):
    status = '200 OK'
    output = 'Hello World! Running Python version %s\n\n' % (sys.version)
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]

    #Check that the ErrorMiddleware works by uncommenting the next line
    #raise("error")
    start_response(status, response_headers)
    return [output]

from paste.exceptions.errormiddleware import ErrorMiddleware
application = ErrorMiddleware(application, debug=DEBUG)
