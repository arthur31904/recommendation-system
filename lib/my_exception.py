from .issue import issue
import linecache
import sys
import inspect

class MyException(Exception):
    """
    自定義錯誤源頭
    """
    def __init__(self, message="", code=404, source=""):
        # Call the base class constructor with the parameters it needs
        super(MyException, self).__init__(message)

        # Now for your custom code...
        if issue.get(str(code)):
            this_issue = issue.get(str(code))
            self.message = this_issue.get('message').format(message)
        else:
            self.message = message

        self.code = code
        self.source = source

    def __str__(self):
        return self.message

def print_full_stack(tb=None):
    """
    source :http://blog.dscpl.com.au/2015/03/generating-full-stack-traces-for.html
    :param tb:
    :return:
    """
    if tb is None:
        tb = sys.exc_info()[2]
    print('Traceback (most recent call last):')
    for item in reversed(inspect.getouterframes(tb.tb_frame)[1:]):
        print (' File "{1}", line {2}, in {3}\n'.format(*item))
        for line in item[4]:
            print(' ' + line.lstrip())
        for item in inspect.getinnerframes(tb):
            print(' File "{1}", line {2}, in {3}\n'.format(*item))
        for line in item[4]:
            print(' ' + line.lstrip())

def search_err_stack_source(tb=None):
    if tb is None:
        tb = sys.exc_info()[2]
    item =inspect.getinnerframes(tb)[-1:][0]
    stack_frames_str = ""
    for item in inspect.getinnerframes(tb):
        stack_frames_str = stack_frames_str + '==>( File "{1}", line {2}, in {3})'.format(*item)

    return stack_frames_str
    ##return 'EXCEPTION(File:{1}, LINE:{2} ,IN:{3})'.format(*item)

def get_exception_source():
    """
    serch error source
    :return: string error_line
    """
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
