# Custom Script Debugging
The following guide will explain how to debug [custom interception scripts](../admin-guide/custom-script.md). 

## Prepare Eclipse

  1. Install the PyDev Eclispe plugin from the Eclipse Markeplace
  1. Open Debug perspective
  1. Start the remote debugger server by navigating to `Menu` > `PyDev` > `Start Debug Server`

## Prepare CE

  1. Log into the CE chroot container 
  1. Change directory into the opt folder: `cd /opt`  
  1. Download [pydevd-1.1.1.tar.gz](https://pypi.python.org/packages/39/66/ef4821f24953ef4e9be73de99209fa74d14b4fa90559571553c7c7ecaf61/pydevd-1.1.1.tar.gz) or later    
  1. `tar -xzf pydevd-1.1.1.tar.gz` 
  1. `rm -rf pydevd-1.1.1.tar.gz` 
  1. `ln -sf /opt/pydevd-1.1.1 /opt/pydevd` 

## Enable Remote Debug in Custom Script

  1. After the import section, add:   
  
        ```
        REMOTE_DEBUG = True
  
        if REMOTE_DEBUG:
            try:
                import sys
                sys.path.append('/opt/pydevd')
                import pydevd
            except ImportError as ex:
                print "Failed to import pydevd: %s" % ex
                raise
        ```     
      
  1. Add the following lines wherever breakpoints are needed:   
  
        ```
        if REMOTE_DEBUG:
            pydevd.settrace('DEV_IP', port=5678, stdoutToServer=True, stderrToServer=True)
        ```

## Start Flow to Trigger Breakpoint
  1. Enable script  
  1. Start authentication process 
  1. After executing line with `pydevd.settrace`, Eclipse should show a dialog to select script source  
  1. Select the appropriate script file and debug  

## Additional Resources
1. [Remote debugger](http://www.pydev.org/manual_adv_remote_debugger.html)





## Setup

The following instructions assume Gluu Server 3.1.4 is already installed and available. If not, perform a standard [Gluu Server installation](../installation-guide/index.md), then proceed: 

1. Install `http://c1.gluu.org:8999/tools-intall.sh`
1. Logout from CE
1. Run `/opt/gluu-server-3.1.4/opt/gluu/bin/prepare-dev-tools.py`
1. Login into CE
1. Run `/opt/gluu/bin/eclipse.sh`

Once complete, start the PyDev debug server:

1. Open Eclispe Debug perspective   
1. Run from menu: `Pydev` > `Start Debug Server`

## Development & Debugging

Now we are ready to perform script developement and debugging. Here is a quick overview:

1. In order to simplify developement put the script into a shared location like `/root/eclipse-workspace`.
1. Then instruct oxAuth to load the script from the file system *instead* of LDAP
1. Add debug instructions to the script, as specified [in the developer guide]](./intro.md)
1. Trigger script execution.

## Sample Scenario

1. Log int oxAuth 
1. Navigate to `Manage Custom Script Section`
1. Expand `Basic` script section  
1. Copy the script to `/root/eclipse-workspace/basic.py`  
1. Change script `Location type` to `File`.
1. Specify the `Script Path` location to: `/root/eclipse-workspace/basic.py`.
1. Enable the script 
1. Check the following log to verify that oxAuth loaded the script properly: `/opt/gluu/jetty/oxauth/logs/oxauth_script.log`. It should look this this:
    

    ```
    ...(PythonService.java:239) - Basic. Initialization

    ... (PythonService.java:239) - Basic. Initialized successfully
   
    ```

1. Open the following file in Eclipse: `/root/eclipse-workspace/basic.py` 
1. Specify Jython type and set the location to: `/opt/jython`
1. Open basic.py in a file editor, and after the import section add the following lines to load the pydev libraries:

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

1. Add break condition to the first line in authenticate method:

    ```
    if REMOTE_DEBUG:
        pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)

    ```

1. Save `basic.py`   
1. Within one minute oxAuth should load the changed file. Check the following log file again to make sure there are no load errors: `/opt/gluu/jetty/oxauth/logs/oxauth_script.log`    
1. To check if the script works, update the default authentication method to Basic Authentication. This can be performed in oxTrust by navigating to `Manage Authentication` > `Default Authentication Method`   
1. Open another browser or session and try to login. 
    !!! Warning
    Make sure to keep the first session open in order to disable basic authentication method in case the script doesn't work as expected.        
1. After executing `pydevd.settrace` the script will transfer execution control to the PyDev server in Eclipse    
1. After debuggng is finished, resume script execution to transfer execution control back to oxAuth     
