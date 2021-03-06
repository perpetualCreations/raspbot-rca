# Host Instructions

## Install
To install, copy contents into the user "pi"'s home directory.

Next, to setup automatic host application start-up on boot, run `sudo bash boot_run.sh`. You can remove the start-up script later upon uninstalling.

Continue with installing Python dependencies listed in `requirements.txt`.

## Configure
Review configuration files `main.cfg`, `hardware.cfg`, `comms/comms.cfg`. 
Specify your hardware configuration under `hardware.cfg` by marking fields as `True` or `False`.
Specify your network port configuration, encryption and authentication keys, and camera feed compression under `comms/comms.cfg`.

Replace placeholders with intended values.
Please note these configuration entries should be uniform with the client's when applicable.

The field for an authentication key in `comms/comms.cfg` should not be manually filled. Use the `auth_key_hasher.py` script to generate the hash required.

## Arduino
Run the Arduino script generation tool, labeled `tool.py`.
You will be asked to provide a path to your hardware configuration file (i.e. `C:/Users/X/Raspbot RCA/client/hardware.cfg` or `/home/X/Raspbot RCA/client/hardware.cfg`).

Please make sure you have edited your hardware configuration file prior, to match your installed hardware.

A script will be generated for uploading. To upload, plug the USB Type A plug on the USB A to USB B cable usually plugged into the Raspberry Pi into your computer and make sure the USB Type B plug is seated nicely into the Arduino's port.

Compile and upload the generated source file with your favorite IDE.

After uploading the script file, you may disconnect the Type A plug and plug it into the Raspberry Pi.

## Additional Notes

### Note about Static IPs
Usually, unless you have already pre-configured your Pi, it will work under an address provided by a DHCP server.
These addresses may change as a device connects and disconnects to and from a network. For your convenience, consider setting a static address to maintain the same address.

See documentation and tutorials online on how to do this.

### Note about Port Forwarding
Although the host application was designed with security in mind, it is not recommended to setup port forwarding.
The security measures in place are by no means perfect, nor are they particularly robust. They are not vetted by any qualified InfoSec professional.

It should also be emphasized regardless how impervious the host application is, port forwarding will expose your device to the open internet. Proceed at your own risk.

If for some reason, you do need remote access from outside your local network, try setting up an OpenVPN tunnel instead of port forwarding.

If you decide to continue anyways, port forward the ports listed in the `comms/comms.cfg` file, by default they are 64220, 64221, and 64222.
Refer to your router manual to see if port forwarding is available, and how to perform it.

## Conclude
This is the end of the installation instructions. At this point, you may restart your Pi.

If you haven't already done so, install the client application.

If you didn't set up the host application to automatically start, manually start it and test it with your client.

Please forward questions and issues to the Github repository's issue tab, or contact project maintainer(s).
