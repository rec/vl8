import os
import unittest

IS_TRAVIS = os.getenv('TRAVIS', '').lower().startswith('t')
if_travis = unittest.skipIf(IS_TRAVIS, 'Test does not work in travis')
