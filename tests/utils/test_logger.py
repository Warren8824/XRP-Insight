import unittest
from unittest.mock import patch, MagicMock
import os
import logging
from src.utils.logger import setup_logger, configure_loggers, get_loggers


class TestLogger(unittest.TestCase):
    """
    A test suite for the logger module.

    This class contains unit tests for the logger setup, configuration,
    and retrieval functions in the logger module.
    """

    @patch('src.utils.logger.RotatingFileHandler')
    @patch('src.utils.logger.logging.StreamHandler')
    @patch('src.utils.logger.os.getenv')
    def test_setup_logger(self, mock_getenv, mock_stream_handler, mock_file_handler):
        """
        Test the setup_logger function.

        This test verifies that:
        1. The logger is created with the correct name.
        2. The logger has the expected number of handlers (file and stream).
        3. The handlers are properly configured with formatters.
        4. The environment is correctly retrieved.

        Args:
            mock_getenv (MagicMock): Mock for os.getenv function.
            mock_stream_handler (MagicMock): Mock for logging.StreamHandler.
            mock_file_handler (MagicMock): Mock for RotatingFileHandler.
        """
        mock_getenv.return_value = 'development'
        mock_file_handler_instance = MagicMock()
        mock_stream_handler_instance = MagicMock()
        mock_file_handler.return_value = mock_file_handler_instance
        mock_stream_handler.return_value = mock_stream_handler_instance

        # Set the level attribute for our mock handlers
        mock_file_handler_instance.level = logging.INFO
        mock_stream_handler_instance.level = logging.DEBUG

        logger = setup_logger('test_logger', 'test_dir')

        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, 'test_logger')
        self.assertEqual(len(logger.handlers), 2)

        mock_file_handler.assert_called_once()
        mock_stream_handler.assert_called_once()
        mock_file_handler_instance.setFormatter.assert_called_once()
        mock_stream_handler_instance.setFormatter.assert_called_once()
        mock_getenv.assert_called_with('APP_ENV', 'development')

    @patch('src.utils.logger.os.path.exists')
    @patch('src.utils.logger.os.makedirs')
    @patch('src.utils.logger.setup_logger')
    @patch('src.utils.logger.os.getenv')
    def test_configure_loggers(self, mock_getenv, mock_setup_logger, mock_makedirs, mock_exists):
        """
        Test the configure_loggers function.

        This test verifies that:
        1. The correct number of loggers are created.
        2. The log directory is created if it doesn't exist.
        3. The setup_logger function is called for each logger.
        4. The environment is correctly retrieved.

        Args:
            mock_getenv (MagicMock): Mock for os.getenv function.
            mock_setup_logger (MagicMock): Mock for setup_logger function.
            mock_makedirs (MagicMock): Mock for os.makedirs function.
            mock_exists (MagicMock): Mock for os.path.exists function.
        """
        mock_getenv.return_value = 'development'
        mock_exists.return_value = False

        loggers = configure_loggers()

        expected_loggers = ['ai_integration', 'analysis', 'api', 'content_generation',
                            'data_collection', 'data_processing', 'models', 'scheduler',
                            'utils', 'scripts']

        self.assertEqual(set(loggers.keys()), set(expected_loggers))
        mock_makedirs.assert_called_once_with('logs')
        self.assertEqual(mock_setup_logger.call_count, len(expected_loggers))
        mock_exists.assert_called_once_with('logs')
        mock_getenv.assert_called_with('APP_ENV', 'development')

    @patch('src.utils.logger.configure_loggers')
    def test_get_loggers(self, mock_configure_loggers):
        """
        Test the get_loggers function.

        This test verifies that:
        1. The function returns the correct set of loggers.
        2. The configure_loggers function is called only once (on first invocation).
        3. Subsequent calls to get_loggers use the cached value.

        Args:
            mock_configure_loggers (MagicMock): Mock for configure_loggers function.
        """
        # Reset the global loggers variable
        import src.utils.logger
        src.utils.logger.loggers = None

        mock_loggers = {
            'ai_integration': logging.getLogger('ai_integration'),
            'analysis': logging.getLogger('analysis'),
            'api': logging.getLogger('api'),
            'content_generation': logging.getLogger('content_generation'),
            'data_collection': logging.getLogger('data_collection'),
            'data_processing': logging.getLogger('data_processing'),
            'models': logging.getLogger('models'),
            'scheduler': logging.getLogger('scheduler'),
            'utils': logging.getLogger('utils'),
            'scripts': logging.getLogger('scripts'),
        }
        mock_configure_loggers.return_value = mock_loggers

        # First call to get_loggers
        loggers = get_loggers()
        self.assertEqual(set(loggers.keys()), set(mock_loggers.keys()))
        mock_configure_loggers.assert_called_once()

        # Reset the mock to check it's not called again
        mock_configure_loggers.reset_mock()

        # Second call to get_loggers (should use cached value)
        loggers = get_loggers()
        self.assertEqual(set(loggers.keys()), set(mock_loggers.keys()))
        mock_configure_loggers.assert_not_called()


if __name__ == '__main__':
    unittest.main()
