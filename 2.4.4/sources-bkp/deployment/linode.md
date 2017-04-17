# Linode VM
As mentioned earlier that the Linode VMs come with a custom kernel and they are not compatiable with Gluu Server. The following steps will help to update your kernel so that Gluu Server can be installed.

## Update Kernel

It is a recommended to check for the current version. Run the following command to check for kernel version:

```
# uname -a
```

If the output contains the `-Linode` then it is a custom kernel and it is mandate to run the following command:

```
# apt-get install linux-image-virtual grub2
```

### Modify Grub2
After the installation of the new kernel and grub2, grub2 has to be configured.

Edit the file `grub` under the `/etc/default/` folder.

```
# vim /etc/default/grub
```

Please ensure that the following lines are present in the `grub` file
```
GRUB_TIMEOUT=10
GRUB_CMDLINE_LINUX="console=ttyS0,19200n8"
GRUB_DISABLE_LINUX_UUID=true
GRUB_SERIAL_COMMAND="serial --speed=19200 --unit=0 --word=8 --parity=no --stop=1"
```

Run the following command to update grub and reboot VM.
```
# update-grub
```
