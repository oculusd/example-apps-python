# example-apps-python
Example applications to demonstrate the use of the libraries and services.

## Getting Started

Clone this repository

```vash
$ git clone https://github.com/oculusd/example-apps-python.git
$ cd example-apps-python/
```

Create a Python virtual environment and install required libraries:

```bash
$ virtualenv -p python3 venv
$ source vemv/bin/activate
(venv) $ pip3 install https://github.com/oculusd/odc_pycommons/releases/download/release-0.0.2/odc_pycommons-0.0.2.tar.gz
(venv) $ pip3 install https://github.com/oculusd/odc_pyadminlibs/releases/download/r0.0.3/odc_pyadminlibs-0.0.3.tar.gz
```

The example shows the method of creating a virtual environment using `virtualenv` - for a more pure Python 
alternative, [refer to the documentation](https://docs.python.org/3.6/tutorial/venv.html).

If you intent to run the Python scripts using `cron` or some other scheduler, you may need to 
edit [the `shebang` line](https://en.wikipedia.org/wiki/Shebang_(Unix)) to point to your virtual environment's Python executable. Example:

Change:

```
#!/bin/env python3
```

Pointing to the virtual environment (showing a potential Raspberry Pi example):

```
#!/home/pi/venv/bin/python3
```

## Unix Load Average Logger

### Using the Root Account

Assuming you have registers a root account and `Thing`, you could use the following script to log your Unix based system 
load average to the OculusD service: `nix_load_average_logger/nix_load_average_logger_root_acc.py`.

Sample run:

```bash
(venv) $ python3 nix_load_average_logger/nix_load_average_logger_root_acc.py -e ...your_root_account_email_address... -t ...your_thing_id...
Loading root_account "...your_root_account_email_address..."
Authenticating root_account
    Cached token timestamp: 1542335636
                       now: 1542342883
    Using cached token...
Loading thing
Confirming thing token
    Using cached thing token
Capturing load average
Load Data: (2.0390625, 2.17626953125, 2.08251953125)
    Number of records captured: 3
DONE
```

The script was written in a way to demonstrate the typical steps required to record some sensor data. You can use this 
as a template or modify it to create a library for your solutions.

The actual sensor capturing magic happens in the function `record_load_average()` and this would be the function to 
modify or adapt to suite your own needs.

## Conclusion

It is still early days and the examples will be expanded hopefully significantly in the near future.

Please visit us at [OculusD.com, Inc](https://www.oculusd.com/)
