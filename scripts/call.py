"""
Call a database function, send its output to standard out as a CSV.
"""

import sys

from config import from_config
import sql


class DatabaseFunctionCall(object):
    """A database function call."""
    
    def __init__(self, name, signature):
        self.func = sql.DatabaseFunction(name)
        self.signature = signature
    
    def __enter__(self):
        """Wrap the database function call in a transaction."""
        return self.func.__enter__()
    
    def __exit__(self, type_, value, traceback):
        """Rollback on error, else commit."""
        self.func.__exit__(type_, value, traceback)
    
    def get_arguments(self, kwargs):
        """Get a list of function arguments according to its signature."""
        return [kwargs[param] for param in self.signature]
    
    def execute(self, **kwargs):
        """Execute the database function call according to keyword arguments."""
        args = self.get_arguments(kwargs)
        return self.func(*args)


def main(dec_file, call_file):
    """Call a database function, send its output to standard out as a CSV."""
    
    # Instantiate a database function call with its declaration
    with from_config(DatabaseFunctionCall)(dec_file) as call:
    
        # Call it with the arguments described in the call file
        rows = from_config(call.execute)(call_file)
    
        # Write the output of the function to standard out
        sql.to_csv(rows, stream=sys.stdout)


if __name__ == '__main__':
    main(*sys.argv[1:])
