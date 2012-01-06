"""
Based on:
 http://ericholscher.com/blog/2009/jun/29/enable-setuppy-test-your-django-apps/
 http://www.travisswicegood.com/2010/01/17/django-virtualenv-pip-and-fabric/
 http://code.djangoproject.com/svn/django/trunk/tests/runtests.py
 https://raw.github.com/jakul/django-rest-framework/autodiscover/djangorestframework/runtests/runtests.py
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'runtests.settings'



from django.conf import settings
from django.test.utils import get_runner

def usage():
    return """
    Usage: python runtests.py [UnitTestClass].[method]
    
    You can pass the Class name of the `UnitTestClass` you want to test.
    
    Append a method name if you only want to test a specific method of that class.
    """
    
def main():
    TestRunner = get_runner(settings)

    test_runner = TestRunner()
    if len(sys.argv) == 2:
        test_case = '.' + sys.argv[1]
    elif len(sys.argv) == 1:
        test_case = ''
    else:
        print usage()
        sys.exit(1)
        
    print test_case
    failures = test_runner.run_tests(['djangotransifex' + test_case])

    sys.exit(failures)

if __name__ == '__main__':
    main()