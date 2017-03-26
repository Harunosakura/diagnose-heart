import logging
from datetime import datetime
import inspect
import os
import json


class DiagnoseHeartLog(object):
    START_FUNCTION = 'S'
    END_FUNCTION = 'N'
    _DEFAULT_SETTINGS_FILE = 'log.json'

    _DATE_FORMAT = '%m%d%Y'
    _TIME_FORMAT = '%H%M%S|%f'
    _LOG_DIR = 'logs'
    _STATE_ERROR_MESSAGE = 'State should indicate "S" for the start of a function, "N" for the end of a function, ' \
                           'or should be Integer for indicate the loop iteration.'

    def __init__(self, file_name=_DEFAULT_SETTINGS_FILE):
        """
        The name of the file that contains the log settings.
        If a name is not given, it will try to load the default file log.json
        """
        param = self._load_settings(file_name)
        self.p_func = param['print_function']
        self.p_loop = param['print_loop']
        self.p_ifstm = param['print_if_statement']
        self.p_tc = param['print_time_complexity']

        # Turn
        self._current_turn = 1

        # Stack for record the levels of function called
        self._stack = []

        # Will create a log file with the name in the format YYYYMMDD_HHMMSSFFF
        file_name = '%s.log' % datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]

        # Check if the folder logs exists, if not, create
        log_folder = os.path.join('.', self._LOG_DIR)
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        logging.basicConfig(filename=os.path.join(log_folder, file_name), level=logging.INFO, format='%(message)s')

    def _load_settings(self, file_name):
        """
        Load the log settings from a json file.

        Args:
            file_name: The name of the file to load

        Returns:
            a dictionary with all the settings
        """
        with open(file_name) as f:
            d = json.load(f)
            return d['LogParameters']

    def inc_turn(self):
        """
        Explicitly increments the log turn
        """
        self._current_turn += 1

    def turn(self):
        """
        Get the current log turn

        Return:
            return the current turn for the log
        """
        return self._current_turn

    def log(self, description):
        """
        Decorator for easily log the beginning and ending of a function

        Returns:
            The wrapper function
        """
        def wrap(func):
            def log_wraper(*args, **kwargs):
                # Discover the name of the function that the decorator was used
                file_name = inspect.getfile(func)

                # Discover if it was a function or a method. If is a method, discover the name of the class
                spec = inspect.getargspec(func)
                class_name = ''
                if spec.args and spec.args[0] == 'self':
                    class_name = args[0].__class__.__name__

                # Get the name of the class
                function_name = func.__name__

                # Get current turn and insert it in the stack
                x = self.turn()
                self._stack.append(x)

                # Log the information on the beginning of the function
                self.log_time_stamp(x, file_name, class_name, function_name, DiagnoseHeartLog.START_FUNCTION, description)

                # Call the function
                func(*args, **kwargs)

                # Log the information on the ending of the function
                self.log_time_stamp(x, file_name, class_name, function_name, DiagnoseHeartLog.END_FUNCTION, description)

                # If function call stack is empty increment the turn counter
                self._stack.pop()
                if not self._stack:
                    self.inc_turn()
            return log_wraper
        return wrap

    def log_time_stamp(self, turn, file_name, class_name, function_name, state, description, date_stamp=None,
                       time_stamp=None):
        """
        Log the information received; and depending on configuration, could print the log.

        Both arguments, date_stamp and time_stamp, could be omited, and the current values will be calculated. But, or
        both values is given or none of them should be given.

        Args:
            turn:
            file_name:
            class_name:
            function_name:
            state:
            description:
            date_stamp:
            time_stamp:

        Returns:
            None

        Raises:
            AttributeError
        """
        # Check the state parameter if has a valid type or value
        if not isinstance(state, (str, int)):
            raise AttributeError(self._ERROR_MESSAGE)

        if isinstance(state, str):
            if state not in ['S', 'N']:
                raise AttributeError(self._ERROR_MESSAGE)

        # Check if both time and date was given of if both was not given
        if (not date_stamp and time_stamp) or (date_stamp and not time_stamp):
            raise AttributeError('Both date_stamp and time_stamp should be filled or both should not be passed.')

        # If needed, create the stamps
        if not all([date_stamp, time_stamp]):
            now = datetime.now()
            date_stamp = now.strftime(self._DATE_FORMAT)
            time_stamp = now.strftime(self._TIME_FORMAT)

        # Format the message
        m = '[%d]|[%s]|[%s]|[%s]|[%s]|[%s]|[%s]|[%s]' % (turn, file_name, class_name, function_name, state,
                                                         date_stamp, time_stamp, description)

        # Check if have to print
        if self.p_func and state in ['S', 'N']:
            print m
        elif self.p_loop and isinstance(state, int):
            print m

        # Log the information
        logging.info(m)

    def log_complexity(self, turn, file_name, class_name, function_name, complexity):
        """
        Log the complexity
        """
        # Format the message
        m = '[%d]|[%s]|[%s]|[%s]|[%s]|[%s]' % (turn, file_name, class_name, function_name, 'C',complexity)

        # Check if it should be printed
        if self.p_tc:
            print m

        # Log the information
        logging.info(m)


dhl = DiagnoseHeartLog()