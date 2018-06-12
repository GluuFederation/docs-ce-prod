# Using the lua-resty-openidc Nginx Library as a Relying Party With Gluu Server

As a brief explanation, we will have two servers. One is the Identity Provider(IDP), the Gluu Server; the other is the Relying Party(RP), the Nginx OpenResty server with the lua-resty-openidc library. The lua-resty-openidc Nginx library uses the OpenID Connect [Authorization Code Flow](http://openid.net/specs/openid-connect-core-1_0.html#CodeFlowSteps). Upon the user giving consent, the RP will gather user information from the IDP and if the user is authorized, forward the user to a redirect URI.

Requirements:  
- Gluu Server ([Installation Instructions](https://gluu.org/docs/ce/3.1.3/installation-guide/install/#1-install-gluu-server-package))  
- OpenResty 1.11.2.5  
- gcc  
- libpcre3 libpcre3-dev  
- libssl-dev  
- lua5.2  
- lua-resty-http  
- lua-resty-session  
- lua-resty-jwt  

## Installing OpenResty

First, you'll need to install a few dependencies for lua-resty-openidc. The [dependencies list](https://github.com/zmartzone/lua-resty-openidc#dependencies) is, for the most part, covered by `OpenResty`. As of writing this (5 June 2018) there is an API conflict with OpenResty 1.13.6's `OpenSSL 1.1.0` implementation  and `lua-resty-jwt` which used `OpenSSL 1.0.2`. So, we must build OpenResty 1.11.2.5, as this includes `OpenSSL 1.0.2`.

```
apt update
apt-get install gcc libssl-dev libpcre3 libpcre3-dev
wget https://openresty.org/download/openresty-1.11.2.5.tar.gz
tar -xvf openresty-1.11.2.5.tar.gz 
cd openresty-1.11.2.5
./configure -j2
make -j2
sudo make install
```

Then we can add the OpenResty bin to PATH:

```
export PATH=/usr/local/openresty/bin:$PATH
```

After that, we can download the lua-resty dependencies with OPM (OpenResty Package Manager):

```
opm install bungle/lua-resty-session 
opm install SkyLothar/lua-resty-jwt 
opm install pintsized/lua-resty-http 
opm install zmartzone/lua-resty-openidc
```

## Configuring a Gluu Server OpenID Connect Client

At this point, we need to register an OpenID Connect client, lua-resty-openidc, in Gluu Server. We also need to configure Nginx with lua-resty-openidc to use Gluu Server as its Identity Provider.

Navigate to your Gluu Server, and click `OpenID Connect` -> `Clients`.

Here, we want to click the `Add Client` button on the top.

Now, name the client anything you want. I chose lua-resty-openidc for convenience, but this is only for human recognition. The `Client Description` can be more thorough to describe the purpose of the client. `Client Secret` can be anything you want it to be. You can increase the entropy and difficulty of your secret by running this in a terminal:

```
gpg --gen-random --armor 1 30
```

And using it as your secret. Make sure to store this somewhere, as it won't be retrievable in the Identity UI.

Moving forward, we can skip a lot of configuration examples for the sake of simplicity in this tutorial and jump down to the bottom, where we will `Add Login Redirect URI`, `Add Scope`, `Add Response Type` and `Add Grant Type`. For our example, our `Redirect Login URI` will be:

```
https://$HOSTNAME/welcome
```

Now, click `Add Scope` and `Search` to display all scope options. Check `email`, `openid` and `profile`.

Next, click `Add Response Type` and check `code` and `id_token`.

Click `Add Grant Type` and check `authorization_code`.

For our simple example, this is enough, and we can click the `Add` button at the bottom of the page. Once we've done this, we can gather our inum from the `OpenID Connect/Clients` dashboard next to the Display Name of the client we created. We will need this later for the lua-resty-openidc Nginx configuration's `client_id`.

## Configuring OpenResty's Nginx

Now, on our Relying Party Server (Not the Gluu Server), let's create some SSL certificates and then use those in our Nginx configuration.

```
mkdir -p /usr/local/openresty/nginx/ssl/
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /usr/local/openresty/nginx/ssl/nginx.key -out /usr/local/openresty/nginx/ssl/nginx.crt
```

Fill out the prompts for your certificates. We'll use them in the following Nginx configuration.

Now, we can finally make our configuration in OpenResty's Nginx. This nginx.conf can be found at `/usr/local/openresty/nginx/conf/nginx.conf`. Replace `$INUM` and `$SECRET` with the inum and client secret from the OpenID client we just created in Gluu Server. Replace `${GLUU_SERVER}` with the hostname of your Gluu Server.

```
events {
  worker_connections 1024;
}

http {

  lua_package_path "/usr/local/openresty/?.lua;;";

  resolver 8.8.8.8;

  lua_ssl_trusted_certificate /etc/ssl/certs/ca-certificates.crt;
  lua_ssl_verify_depth 5;

  # cache for discovery metadata documents
  lua_shared_dict discovery 1m;
  # cache for JWKs
  lua_shared_dict jwks 1m;

  server {
	listen 80 default_server;
	server_name _;
	return 301 https://$host$request_uri;
  }
  server {
    listen 443 ssl;

    ssl_certificate /usr/local/openresty/nginx/ssl/nginx.crt;
    ssl_certificate_key /usr/local/openresty/nginx/ssl/nginx.key;

    location / {

      access_by_lua_block {

          local opts = {
             redirect_uri_path = "/welcome",
             discovery = "https://${GLUU_SERVER}/.well-known/openid-configuration",
             client_id = "$INUM",
             client_secret = "$SECRET",
             ssl_verify = "no",
             scope = "openid email profile",
             redirect_uri_scheme = "https",
          }

          -- call authenticate for OpenID Connect user authentication
          local res, err = require("resty.openidc").authenticate(opts)

          if err then
            ngx.status = 500
            ngx.say(err)
            ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
          end

          ngx.req.set_header("X-USER", res.id_token.sub)
      }
    }
  }
}
```

After we've saved this configuration file, let's run the `openresty` command we added to our path.

Now navigate to the RP, which will redirect you to your IDP, where you can log in, authorize the RP to gather information and be directed back to the OpenResty default `index.html`, which is located at `/usr/local/openresty/nginx/html/index.html`.

Of course, this is a limited and simplified proof of concept. Further customization and optionality can be added. Please refer to the [official documentation](https://github.com/zmartzone/lua-resty-openidc) for the `lua-resty-openidc` library to add more extensibility for your use case. There are a multitude of examples on the main README.md. Also, check out the [Gluu Server OpenID Connect API](https://gluu.org/docs/ce/3.1.3/api-guide/openid-connect-api/) documentation for help with ~1:1 configuration settings that need to be set to match the libary.
