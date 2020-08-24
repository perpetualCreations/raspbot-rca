"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
comms module, allows for socket communications.
Made by Taian Chen

This script handles interfacing functions.
"""

from comms import objects, disconnect

def send(message):
    """
    Wrapper for host.encrypt, formats output to be readable for sending, and accesses objects.socket_main to send it.
    This no longer requires to be used as socket.sendall(interface.send(self, b"message")).
    :param message: message to be encrypted.
    :return: none
    """
    encrypted = encrypt(message)
    objects.socket_main.sendall(encrypted[1] + b" " + encrypted[2] + b" " + encrypted[0])
pass


def receive():
    """
    Wrapper for host.decrypt, formats received input and returns decrypted message. socket.socket_main.recv is now built-in.
    This no longer requires to be used as host.receive(self, socket.receive(integer)).
    :return: decrypted message.
    """
    socket_input_spliced = objects.socket_main.recv(4096).split() # TODO is this the right usage of recv???
    return decrypt(socket_input_spliced[2], socket_input_spliced[1], socket_input_spliced[0])
pass


def encrypt(byte_input):
    """
    Takes byte input and returns encrypted input using a key and encryption nonce.
    :param byte_input: byte string to be encrypted.
    :return: encrypted string, nonce, and HMAC validation.
    """
    if isinstance(byte_input, bytes):
        pass
    else:
        byte_input.encode(encoding = "ascii", errors = "replace")
    pass
    ciphering = objects.Salsa20.new(objects.key)
    validation = objects.HMAC.new(objects.hmac_key, msg = ciphering.encrypt(byte_input), digestmod = objects.SHA256)
    return [ciphering.encrypt(byte_input), ciphering.nonce, validation.hexdigest()]
pass


def decrypt(encrypted_input, validate, nonce):
    """
    Decrypts given encrypted message and validates message with HMAC and nonce from encryption.
    :param encrypted_input: encrypted string to be decrypted.
    :param validate: HMAC validation byte string.
    :param nonce: nonce, additional security feature to prevent replay attacks.
    """
    validation = objects.HMAC.new(objects.hmac_key, msg = encrypted_input, digestmod = objects.SHA256)
    try:
        validation.hexverify(validate)
    except ValueError:
        disconnect.disconnect()
        raise Exception("[FAIL]: Message is not authentic, failed HMAC validation!")
    pass
    ciphering = objects.Salsa20.new(objects.key, nonce = nonce)
    return ciphering.decrypt(encrypted_input)
pass
