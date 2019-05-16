# oxd

!!! Attention
    The official support end-of-life (EOL) date for Gluu Server 2.4.4 is December 31, 2018. Starting January 1, 2019, no further security updates or bug-fixes will be provided for Gluu Server 2.X. We strongly recommend [upgrading](https://gluu.org/docs/ce/upgrade/) to the newest version.

## Overview 
[oxd](https://oxd.gluu.org) is a middleware service that makes it easy to securely implement login to your application using any standard OpenID Connect Provider (OP), like the Gluu Server. oxd is not a proxy--sometimes it makes API calls on behalf of an application, but other times it just forms the right URLs and returns them to the application.

Your application can use any client software that implements the open standards the Gluu Server supports, but you may want to consider using oxd for the following reasons:

(1). oxd is super-easy to use;

(2). We keep updating oxd to address the latest OAuth 2.0 security knowledge;

(3). We can provide more complete end-to-end support if we know both the client and server software;

(4). oxd subscriptions help support this project so you can see more enhancements faster;

(5). There are oxd libraries for Php, Python, Java, Node, Ruby, C#, Perl and Go. If your application is programmed in another language, oxd has a simple JSON/REST API;

(6). There are oxd plugins for many popular applications like: Wordpress, Drupal, Magento, OpenCart, SugarCRM, SuiteCRM, Roundcube, Shopify, and Kong. More are being added too. Next on the list are: MatterMost, RocketChat, NextCloud, and Liferay.

## Docs
oxd docs can be found at: [https://oxd.gluu.org/docs](https://oxd.gluu.org/docs).   

## License
oxd is commercial software licensed by Gluu. Learn more on the [oxd website](https://oxd.gluu.org).
