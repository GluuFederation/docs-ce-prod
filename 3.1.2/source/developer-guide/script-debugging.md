# Remote custom script debugging
The following guide will explain how to debug [custom interception scripts](../admin-guide/custom-script.md). 

## Prepare Eclipse.

  1. Install PyDev Eclispe plugin from Eclipse Markeplace
  1. Open Debug perspective.
  1. Start the remote debugger server. Menu: PyDev->Start Debug Server.

## Prepare CE

  1. Log into the CE chroot container 
  1. cd /opt  
  1. Download pydevd-1.1.1.tar.gz or more recent. [Link](https://pypi.python.org/packages/39/66/ef4821f24953ef4e9be73de99209fa74d14b4fa90559571553c7c7ecaf61/pydevd-1.1.1.tar.gz)
  1. tar -xzf pydevd-1.1.1.tar.gz 
  1. rm -rf pydevd-1.1.1.tar.gz 
  1. ln -sf /opt/pydevd-1.1.1 /opt/pydevd 

## Enable remote debug in custom script.

  1. Add ater import section:
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
  1. Add next lines to all place where you need to add breakpoints
      ```
      if REMOTE_DEBUG:
          pydevd.settrace('DEV_IP', port=5678, stdoutToServer=True, stderrToServer=True)
      ```

## Start flow to trigger breakpoint
  1. Enable script  
  1. Start authentication process 
  1. After executing line with `pydevd.settrace`, Eclipse should show dialog to select script source  
  1. After selecting script file it's possible to debug it  

## Additional sources
1. [Remote debugger](http://www.pydev.org/manual_adv_remote_debugger.html)

