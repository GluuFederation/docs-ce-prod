# Gluu Server Linux Tips [ Work in Progress ] 

This documentation is for system administrators who are in charge of Linux servers where Gluu Servers are hosted. 

## Minimum requirements Gluu Server system administrator 

 - Need to be fluent with linux/unix commands through terminal ( not GUI )
 - Need to be fluent with network administration
 - Basic Linux security knowledge would be a big plus

## Installation of Gluu Server

Gluu Server require a minimum resources to be performed flawlessly; those requirements are available in `Installation Guide`. 
As System Administration ( or, SysAdmin ) you need to perform couple of tasks before deployer move forward for Gluu Server installation. 

 - Installation of VM with supported OS. 
   - We are not going to cover 'How to install Linux server' here because that's pretty straight forward and very easy now a days. 
   - Disk space: Minium required disk space is 40GB in /root OR .............................................
 - Put a specific IP for your linux server
   - You need to remmember that this IP *must be* a static IP; Gluu Server *can not* perform well in dynamic IP / DHCP setup. 
   - You need to make sure that port 443 is open from Internet OR from those machines from where Gluu Server operations will be performed. This is inbound tcp/443
   - Make sure you restrict SSH ports ( tcp/22 ) for those IP/machines which will be connected ( in a sense to perform daily operation and/or installation ) in your Gluu Server VM. Also it's better to establish cert-based SSH into your Gluu Server linux boxes than general username/password SSH. 
   - You may/may not need to open / close few other ports according to your Gluu Server setup. 
   - Here is a simple method how you can configure Ubuntu Server for static IP, 192.168.150.131 is the static IP for our Ubuntu Server. 

```
zico@test3:~$ cat /etc/network/interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.150.131
netmask 255.255.255.0
gateway 192.168.150.2
zico@test3:~$
```
   -  Sample method of configuring CentOS/RHEL server for static IP: 
 



## Tweaking of Gluu Servers

## Maintenance of Gluu Servers 


