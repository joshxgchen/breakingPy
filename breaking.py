
from typing import Tuple
from time import perf_counter_ns
from string import ascii_lowercase

import scipy
import numpy

from e5utils import LockBox, Facade


# NOTE: Returns a pair (password, contents) corresponding to
#  the password that opens the lockbox and the actual contents of the
#  lockbox. The only action that it can take with a `LockBox` is
#  calling the `try_password` method. Any other properties (like
#  field names, number of fields, etc.) can change at test time.
def break_lockbox(lockbox: LockBox) -> Tuple[str, str]:
    discovered_password = ''
    while True:
        times = []
        for char in ascii_lowercase:
            start_time = perf_counter_ns()
            lockbox.try_password(discovered_password + char)
            end_time = perf_counter_ns()
            times.append((end_time - start_time, char))
        
        times.sort(reverse=True)
        next_char = times[0][1]
        discovered_password += next_char
        if lockbox.try_password(discovered_password):
            return (discovered_password, lockbox.try_password(discovered_password))
    

# NOTE: Returns a string corresponding to the result from successfully
# calling `takeover` on a `CaerfilyDesinedSurvis`. 
def break_facade(facade: Facade) -> str:
    injected_command = "name\ndumpcodeword"
    results = facade.greet(injected_command)
    codeword = results[1]  # Assuming the second line of output is the codeword
    takeover_command = f"takeover {codeword}"
    takeover_results = facade.__service.execute(takeover_command)
    return takeover_results[0]
    
    
    
    
    
