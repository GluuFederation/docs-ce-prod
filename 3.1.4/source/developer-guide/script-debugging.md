# Custom Script Debugging
The following guide will explain how to debug [custom interception scripts](../admin-guide/custom-script.md). 

## Setup

The following instructions assume Gluu Server 3.1.4 is already installed and available. If not, perform a standard [Gluu Server installation](../installation-guide/index.md), then do the following: 

1. Install `https://repo.gluu.org/tools/tools-install.sh`
1. Log out of CE
1. Run `/opt/gluu-server-3.1.4/opt/gluu/bin/prepare-dev-tools.py`
1. Log in to CE
1. Run `/opt/gluu/bin/eclipse.sh`

Once complete, start the PyDev debug server:

1. Open the Eclipse Debug perspective   
1. Run this command from the menu: `Pydev` > `Start Debug Server`

## Development & Debugging

Now we are ready to perform script development and debugging. Here is a quick overview:

1. In order to simplify development, put the script into a shared folder like `/root/eclipse-workspace`
1. Then instruct oxAuth to load the script from the file system *instead* of LDAP
1. Add debug instructions to the script, as specified in the next section
1. Execute the script

## Enable Remote Debug in Custom Script

1. After the import section, add:   
  
        ```
        REMOTE_DEBUG = True
  
        if REMOTE_DEBUG:
            try:
                import sys
                sys.path.append('/opt/libs/pydevd')
                import pydevd
            except ImportError as ex:
                print "Failed to import pydevd: %s" % ex
                raise
        ```     
      
1. Add the following lines wherever breakpoints are needed:   
  
        ```
        if REMOTE_DEBUG:
            pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)
        ```

## Sample Scenario

1. Log in to oxAuth 
1. Navigate to `Manage Custom Script Section`  
1. Expand `Basic` script section  
1. Copy the script to `/root/eclipse-workspace/basic.py`  
1. Change script `Location type` to `File`  
1. Specify the `Script Path` location to: `/root/eclipse-workspace/basic.py`  
1. Enable the script  
1. Check the following log to verify that oxAuth loaded the script properly: `/opt/gluu/jetty/oxauth/logs/oxauth_script.log`. It should look like this:    

    ```
    ... (PythonService.java:239) - Basic. Initialization

    ... (PythonService.java:239) - Basic. Initialized successfully
   
    ```

1. Open the following file in Eclipse: `/root/eclipse-workspace/basic.py` 
1. When opening the Python file for the first time, we need to instruct Eclipse to use a specific interpreter. Follow these steps:
  
    - Press the "Manual Config" button in the dialog box after opening the Python file
    - Open "PyDev->Interpreters->Jython Interpreters"
    - Click the "New..." button in the right panel. Name it "Jython" and specify the interpreter executable "/opt/jython/jython.jar"
    - Click "OK", then confirm the settings by clicking "OK" again, then "Apply and Close"
    - In the final dialog, confirm the settings by clicking "OK"

1. Open basic.py in a file editor. After the import section, add the following lines to load the PyDev libraries:

    ```  
    REMOTE_DEBUG = True  
  
    if REMOTE_DEBUG:  
        try:  
            import sys  
            sys.path.append('/opt/libs/pydevd')  
            import pydevd  
        except ImportError as ex:  
            print "Failed to import pydevd: %s" % ex  
            raise  
    ```    

1. Add this break condition to the first line in the authenticate method:

    ```  
    if REMOTE_DEBUG:   
        pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)  

    ```

1. Save `basic.py`   
1. Within one minute, oxAuth should load the changed file. Check the following log file again to make sure there are no load errors: `/opt/gluu/jetty/oxauth/logs/oxauth_script.log`    
1. To check if the script works, update the default authentication method to Basic Authentication. This can be performed in oxTrust by navigating to `Manage Authentication` > `Default Authentication Method`   
1. Open another browser or session and try to log in 
    
  !!! Warning
      Make sure to keep the first session open in order to disable the Basic Authentication method in case the script doesn't work as expected.        
    
1. After executing `pydevd.settrace` the script will transfer execution control to the PyDev server in Eclipse. You can use any debug commands. For example: Step Over (F6), Resume (F8), etc     
1. After debugging is finished, resume script execution to transfer execution control back to oxAuth

## Additional Resources
- [Remote debugger](http://www.pydev.org/manual_adv_remote_debugger.html)

## X Server troubleshooting
Running `/opt/gluu-server-3.1.4/opt/gluu/bin/prepare-dev-tools.py` allows Eclipse to access X server. 

It runs the following commands:

```
# Only this one key is needed to access from chroot 
xauth -f /root/.Xauthority-gluu generate :0 . trusted 2>1 >> /root/prepare-dev-tools.log

# Generate our own key, xauth requires 128 bit hex encoding
xauth -f /root/.Xauthority-gluu add ${HOST}:0 . $(xxd -l 16 -p /dev/urandom)

# Copy result key to chroot
cp -f /root/.Xauthority-gluu /opt/gluu-server-3.1.4/root/.Xauthority

# Allow to access local server X11   
sudo su $(logname) -c "xhost +local:
```

### Unable to access x11

If Eclipse is unable to access X11, run the following command from the host to check if it has the necessary permissisons:

```
user@u144:~$ xhost +local:
non-network local connections being added to access control list
user@u144:~$ xhost 
access control enabled, only authorized clients can connect
LOCAL:
SI:localuser:user
```

If the user is still unable to access X11, remove `.Xauthority` from user home and log out/log in again.
