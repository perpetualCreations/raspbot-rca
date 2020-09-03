"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

Evaluates objects.net_status_data and returns True/False boolean.
After importing utilize as net_status_data_evaluate.evaluate().

I wrote this at 4 AM, I'm not sure why.
I think I was trying to add some sort of check to prevent connect/disconnect from being invoked when they're not supposed to.
(i.e: preventing disconnecting twice)
I'll just leave it here, its just 12 lines, I wouldn't call it random bulk.
- pc
"""

from comms import objects

def evaluate():
    """
    Evaluates objects.net_status_Data and returns True/False boolean.
    Logic is nestled in a function to allow for return.
    """
    if objects.net_status_data.get() is "Status: Connected":
        return True
    else:
        return False
    pass
pass
