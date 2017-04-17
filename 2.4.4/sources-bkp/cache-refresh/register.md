# Register User
The oxTrust component provides a very basic user registration service for 
the people to sign-up for an account on the Gluu Server. This service is 
disabled by default. The `User Registration` custom script  is used to enable the 
registration feature.

> Note: When possible, we recommend handling user registration in your app locally, then pushing the information to the Gluu Server via [SCIM 2.0](../api/scim-2.0.md). This will give you much more control and flexibility in defining the exact registration process. Also,
frequently oxTrust is not Internet facing--it was primarily designed as an interface for admins.

## Preparing Gluu Server
Navigate to the [custom scripts](../customize/script.md) section of the Admin Panel. Click on the [configuration](../oxtrust/configuration.md) menu and then  `Manage Custom Scripts`.

![image](../img/2.4/config-manage-script_menu.png)

The tabs near the top of the page can be used to navigate to different custom scripts. We are concerned about 
the `User Registration` tab.

![image](../img/2.4/config-manage-script_menu1.png)

Set the `enable_user` value to to `true` so that the user can login as soon as 
the registration is complete, which sets the default status value. You may want to leave this to `false` if you 
want to manually review user registrations before allowing them.

![image](../img/2.4/config-manage-script_enable.png)

Click `Enable` checkbox at the bottom of the page.

![image](../img/2.4/config-manage-script_check.png)

## User Registration
The users can register through the user registration link usually available at `<hostname>/identity/register`.

![image](../img/2.4/config-manage-script_register.png)
