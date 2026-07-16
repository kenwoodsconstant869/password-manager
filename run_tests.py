import os
import sys
import unittest

os.chdir(r'c:/Users/Kenwo/OneDrive/Documents/cd password-manager')
suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
