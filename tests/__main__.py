import unittest

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.', pattern='test_*.py', top_level_dir='.')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Exit with non-zero code if tests failed
    exit(not result.wasSuccessful())