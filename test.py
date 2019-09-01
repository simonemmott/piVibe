import sys
import settings

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for arg in sys.argv:
            args = ['test.py']
            if arg == '--no-skip':
                settings.SKIP = False
            elif arg[2:] == '--':
                setattr(settings, arg[2:arg.index('=')], arg[arg.index('=')+1:])
            else:
                args.append(arg)
        sys.argv = args

from testing import *
import unittest
from logger import configure_logging

configure_logging()

if __name__ == '__main__':
    unittest.main()
