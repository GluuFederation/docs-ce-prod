# Remote custom script debugging
The following guide will explain how to debug [custom interception scripts](../admin-guide/custom-script.md). 

## Prepare Eclipse.

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

## Enable remote debug in custom script.

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

## Start flow to trigger breakpoint
  1. Enable script  
  1. Start authentication process 
  1. After executing line with `pydevd.settrace`, Eclipse should show a dialog to select script source  
  1. Select the appropriate script file and debug  

## Additional resources
1. [Remote debugger](http://www.pydev.org/manual_adv_remote_debugger.html)

