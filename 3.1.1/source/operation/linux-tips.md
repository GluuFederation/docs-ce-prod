# Gluu Server Linux Tips [ Work in Progress ] 

This documentation is for system administrators who are in charge of Linux servers where Gluu Servers are hosted. 

## Minimum requirements of being a Linux System Administrator of Gluu Servers. 

 - Need to be fluent with linux/unix commands through terminal ( not GUI )
 - Need to be fluent with network administration
 - Basic Linux security knowledge would be a big plus

## Installation of Gluu Server

Gluu Server require a minimum resources to be performed flawlessly; those requirements are available in `Installation Guide`. 
As System Administration ( or, SysAdmin ) you need to perform couple of tasks before deployer move forward for Gluu Server installation. 

 - Installation of VM with supported OS. 
   - We are not going to cover 'How to install Linux server' here because that's pretty straight forward and very easy now a days. 
 - Put a specific IP for your linux server
   - You need to remmember that this IP *must be* a static IP; Gluu Server *can not* perform well in dynamic IP / DHCP setup. 
   - You need to make sure that port 443 is open from Internet OR from those machines from where Gluu Server operations will be performed. This is inbound tcp/443
   - Make sure you restrict SSH ports ( tcp/22 ) for those IP/machines which will be connected ( in a sense to perform daily operation and/or installation ) in your Gluu Server VM. 
   - You may/may not need to open / close few other ports according to your Gluu Server setup. 
 - Disk space



## Tweaking of Gluu Servers

## Maintenance of Gluu Servers 


