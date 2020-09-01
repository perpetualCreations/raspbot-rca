"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
basics module, contains basic application functions such as exiting client software, multiprocessing, and editing configs.
Made by perpetualCreations

Handles exiting and configuration editing.
"""

from basics import objects

def create_process(target, args):
    """
    Creates a new process from multiprocessing.
    :param target: the function being processed.
    :param args: the arguments for said function being processed.
    :return: if failed, returns nothing. otherwise returns dummy variable.
    """
    if __name__ == '__main__':
        try:
            dummy = objects.multiprocessing.Process(target=target, args=args)
            dummy.start()
            dummy.join()
        except objects.multiprocessing.ProcessError as me:
            print("[FAIL]: Process creation failed! Details below.")
            print(me)
            return None
        pass
        return dummy
    else:
        return None
    pass
pass

def stop_process(target, error_ignore):
    """
    Stops target process from multiprocessing.
    :param target: process to be stopped.
    :param error_ignore: boolean to tell the function to throw a failure message or not when failed.
    :return: none.
    """
    if __name__ == '__main__':
        try:
            target.terminate()
        except Exception as spe:
            if error_ignore is True:
                print("[INFO]: Stop process failed, however this is indicated to be normal.")
            else:
                print("[FAIL]: Stop process failed! See details below.")
                print(spe)
            pass
        pass
    pass
pass
