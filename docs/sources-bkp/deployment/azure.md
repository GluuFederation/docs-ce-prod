# Installing Gluu Server in Azure

Accessing the Gluu Server on Azure can be a little bit tricky because of
the Public/Private IP. Here is the step by step guide to creating a VM,
installing Gluu Server and accessing the same. These steps are OS
independent.

## Setting up VM

1. Log into Windows Azure Administrative Panel

2. Click on `Virtual Machines` tab, and click `Create a Virtual Machine` link

3. From the menu, choose `Compute` --> `Virtual Machine` --> `From Gallery` branch.

4. Choose Ubuntu Server 14.04 LTS or CentOS 6.7. Remember to set selinux
   to permissive if you choose CentOS.

5. Provide a name for the VM in the `Virtual Machine Name` field and use
`Standard` for `Tier`.

6. Select at least `A2` variant equipped with 3.5GB RAM in the `Size`
dropdown menu.

7. Provide an username to connect via ssh, and define an according
   access password, or upload a certificate for an authentification 
   without passwords. Then, click `Next`.

8. Create a new cloud service and select `None` for `Availability Set`
   option.
	* Endpoints Section: This is where the port forwarding is set so 
      that the internal IP address could be selectively reachable from 
      the outside world. By default, only ssh tcp port 22 is there. The
      public ports for http and https (tcp ports 80 and 443) have to be 
      added and mapped to the same private ports. If the cloud mappings
      are flagged conflicting, proceed without setting them. Remember to 
      set them after the creation of the VM. Then, click `Next`.

9. Choose not to install `VM Agent` and click the `tick` button to
   finalize the VM.

10. Go to the `Dashboard` tab of VM Management Panel and copy the `DNS
    Name`. This is the name that is used to access the Gluu Server.

11. SSH into the VM and install the Gluu Server. See our [Deployment
    Guide](../deployment/) for installation instructions.

## Setup.py Configuration

This section describes what to put in the prompt when `setup.py` is run
after installing Gluu Server.

* IP Address: Do not change the default IP address; just press `enter`.

* hostname: Use the DNS name that was copied from the `VM Management Panel.

* Update hostname: Choose to update hostname for Ubuntu, but do not
  change if you are running CentOS.
	* For CentOS, manually update the file `/etc/sysconfig/networking`,
      and add the full DNS name.

* Other Settings: The other settings can be left to the default values.
	* Recommendation: the Gluu Server requires a 64bit OS, and allocates
      at least 4GB of RAM for Apache Tomcat in production environments.

* Now the chosen DNS name can be used to access the Gluu Server.

