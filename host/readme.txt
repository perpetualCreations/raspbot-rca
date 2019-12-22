This directory contains the software for running the host server-side remote control application on a bot.
To install, copy contents into the user "pi"'s home directory.
Next, to add a start-up script to automatically start the host RCA upon booting the bot, run "sudo ./boot_run.sh", not "rca-startup.sh".
Afterwards please ensure you have Python 3 installed, and all necessary Python and Linux packages. See requirements.txt for more details.
Reboot your bot. If you setup auto-run it should be already running. Upon first run, the RCA will ask you to enter a password.
This password is the authentication key expected when the bot receives any requests or commands from the client application.
It can be edited afterwards if you have access to the bot's computer, by editing the config file and replacing the SHA3-256 hash with a new one of your choosing.
After entering your password, enter the port number the RCA should listen to. The default is 67777. This may also be edited later in the config file.
For additional convenience, you may want to set the bot's network interface to be static. Please see online resources on how to this and why.
To access outside of your local network, set up port forwarding on your router to pass TCP connections on your selected port (default is 67777 as mentioned) to your bot IP.
See your router manual if this feature exists and how to use it.
This is the end of the install instructions. If you have questions send an email to an attached contact from the main portfolio.
