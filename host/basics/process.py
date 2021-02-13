"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multithreading, and editing configs.
Made by perpetualCreations

Handles multithreading.
"""

from basics import objects
from typing import Union

def create_process(target: Union[classmethod, staticmethod, object], args: tuple = ()) -> Union[None, object]:
    """
    Creates a new thread from multithreading.
    @param target: the function being processed.
    @param args: the arguments for said function being processed.
    @return: if failed, returns nothing. otherwise returns dummy variable.
    """
    if __name__ == "basics.process":
        try:
            dummy = objects.threading.Thread(target = target, args = args, daemon = True)
            dummy.start()
        except objects.threading.ThreadError as ThreadErrorMessage:
            print("[FAIL]: Process creation failed! Details below.")
            print(ThreadErrorMessage)
            return None
        pass
        return dummy
    else: pass
pass

def stop_process(target: object) -> True:
    """
    Returns True for termination flag for a thread, joins given target.
    Use as thread_flag = stop_process(thread_object).
    @param target: process to be stopped.
    @return: bool, True
    """
    target.join()
    return True
pass
