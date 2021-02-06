"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by perpetualCreations

This script handles interfacing functions.
"""

from comms import objects, acknowledge
from basics import restart_shutdown
from typing import Union

def encrypt(byte_input: Union[str, bytes]) -> list:
    """
    Takes byte input and returns encrypted input using a key and encryption nonce.
    :param byte_input: byte string to be encrypted.
    :return: encrypted string, nonce, and HMAC validation.
    """
    if isinstance(byte_input, str): byte_input = byte_input.encode(encoding = "ascii", errors = "replace")
    ciphering = objects.Salsa20.new(objects.key)
    encrypted = ciphering.encrypt(byte_input)
    validation = objects.HMAC.new(objects.hmac_key.encode(encoding = "ascii", errors = "replace"), msg = encrypted, digestmod = objects.SHA256)
    return [encrypted, ciphering.nonce, (validation.hexdigest()).encode(encoding = "ascii")]
pass

def decrypt(encrypted_input: bytes, validate: bytes, nonce: bytes) -> bytes:
    """
    Decrypts given encrypted message and validates message with HMAC and nonce from encryption.
    :param encrypted_input: encrypted string to be decrypted.
    :param validate: HMAC validation byte string.
    :param nonce: nonce, additional security feature to prevent replay attacks.
    """
    validation = objects.HMAC.new(objects.hmac_key.encode(encoding = "ascii", errors = "replace"), msg = encrypted_input, digestmod = objects.SHA256)
    try:
        validation.hexverify(validate.decode(encoding = "utf-8", errors = "replace"))
    except ValueError:
        print("[FAIL]: Message is not authentic, failed HMAC validation!")
        acknowledge.send_acknowledgement(2001)
        restart_shutdown.restart()
    pass
    ciphering = objects.Salsa20.new(objects.key, nonce = nonce)
    return ciphering.decrypt(encrypted_input)
pass

def send(message: Union[str, bytes], socket_object: object = None) -> None:
    """
    Wrapper for encrypt, formats output to be readable for sending, and accesses objects.socket_main to send it.
    This no longer requires to be used as socket.sendall(interface.send(self, b"message")).
    :param socket_object: socket object for message to be sent through, default socket_main
    :param message: message to be encrypted.
    :return: none
    """
    if socket_object is None: socket_object = objects.socket_main
    encrypted = encrypt(message)
    socket_object.sendall(encrypted[1] + b" div " + encrypted[2] + b" div " + encrypted[0])
pass

def receive(socket_object: object = None) -> bytes:
    """
    Wrapper for decrypt, formats received input and returns decrypted message. socket.socket_main.recv is now built-in.
    This no longer requires to be used as host.receive(self, socket.receive(integer)).
    :param socket_object: socket object for message to be received through, default socket_main
    :return: decrypted message.
    """
    if socket_object is None: socket_object = objects.socket_main
    socket_input_spliced = socket_object.recv(8192).split(b" div ")
    return decrypt(socket_input_spliced[2], socket_input_spliced[1], socket_input_spliced[0])
pass
