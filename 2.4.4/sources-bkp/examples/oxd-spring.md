# oxd-spring
This is a sample project that demonstrates how to authenticate using Gluu as an authentication provider in spring project.

## Dependencies
Before you can run or build this project, you must install and configure the following dependencies on your machine:

1. [oxd-server-2.4.3.Final](https://ox.gluu.org/maven/org/xdi/oxd-server/2.4.3.Final/). Configure `${install_dir}/oxd-server/conf/oxd-conf.json`->
 change `op_host` to your openid provider domain e.g `"op_host": "https://ce-dev.gluu.org"`

2. [gluu-server-2.4.3](https://www.gluu.org/docs/deployment/)


## Building&Running
Clone this repo to your computer, and cd into the project directory:
```
git clone https://github.com/GluuFederation/oxd-spring.git
cd oxd-spring 
```
Run maven task

```
mvn clean package
```
if dependencies are not installed yet, you can skip the tests
```
mvn clean package -Dmaven.test.skip=true
```
Run application
```
java -jar target/oxd-spring-0.0.1-SNAPSHOT.jar
```
And point browser to `https://127.0.0.1:8443/`.

***Note:*** oxd-server must run on *localhost* and be bound to port: *8099*, otherwise you'll need to configure `oxd-spring/src/main/resources/application.properties` file.

## How it works

The app is using [oxd-java](https://gluu.org/docs-oxd/plugin/java/) library that helps to communicate with Gluu openid connect provider. This example uses the following functions defined in `org/xdi/oxd/spring/service/OxdService.java`
### OxdService.java
```java
public interface OxdService {

    CommandResponse registerSite(String redirectUrl, String logoutUrl, String postLogoutRedirectUrl);

    CommandResponse updateSite(String oxdId, String redirectUrl);

    CommandResponse getAuthorizationUrl(String oxdId);

    CommandResponse getTokenByCode(String oxdId, String code);

    CommandResponse getUserInfo(String oxdId, String accessToken);

    CommandResponse getLogoutUrl(String oxdId, String idToken);
}

```
The first time app is starting, it registers a new site and stores oxd_id for the site in database.
### Settings.java
```java
@EventListener({ ContextRefreshedEvent.class })
private void onContextStarted() {
  	AppSettings appSettings = appSettingsRepository.findOneByType(SettingsType.OXD_ID);
  	if (appSettings != null) {
  	    this.oxdId = appSettings.getValue();
  	    return;
  	}
  
  	CommandResponse commandResponse = oxdService.registerSite(redirectUrl, logoutUrl, postLogoutUrl);
  	if (commandResponse.getStatus().equals(ResponseStatus.ERROR))
  	    throw new RuntimeException("Can not register site");
  
  	RegisterSiteResponse response = commandResponse.dataAsResponse(RegisterSiteResponse.class);
  	this.oxdId = response.getOxdId();
  
  	appSettings = new AppSettings();
  	appSettings.setType(SettingsType.OXD_ID);
  	appSettings.setValue(oxdId);
  	appSettings = appSettingsRepository.save(appSettings);
}
```
When user goes to home page, authorization_url is generated (using stored oxd_id)
![/home page](https://github.com/worm333/docs/blob/master/sources/img/examples/oxd-spring/Screen%20Shot%202016-05-23%20at%2012.30.15%20AM.png)

When user hits "Login with Gluu" button, app redirects to gluu server and invites the user to log in.
![login page](https://github.com/worm333/docs/blob/master/sources/img/examples/oxd-spring/Screen%20Shot%202016-05-23%20at%2012.37.21%20AM.png)

If logging in is successful, then gluu redirects back to `/gluu/redirect`(this url was declared as redirectUrl param in oxdService.registerSite). This path is mapped by `GluuController.redirect` and here is user get authorized by spring security with ROLE_USER.

### GluuController.java
```java
@RequestMapping(path = "/redirect", method = RequestMethod.GET)
public String redirect(@RequestParam(name = "session_state", required = false) String sessionState,
	    @RequestParam(name = "scope", required = false) String scope,
	    @RequestParam(name = "state", required = false) String state,
	    @RequestParam(name = "code", required = false) String code) {

	Optional<GetTokensByCodeResponse> tokenResponse = Optional.of(oxdService)
		.map(c -> c.getTokenByCode(settings.getOxdId(), code))
		.map(c -> c.dataAsResponse(GetTokensByCodeResponse.class));
	GetUserInfoResponse userInfoResponse = tokenResponse
		.map(c -> oxdService.getUserInfo(settings.getOxdId(), c.getAccessToken()))
		.map(c -> c.dataAsResponse(GetUserInfoResponse.class))
		.orElseThrow(() -> new BadCredentialsException("Can't get user info"));

	Collection<GrantedAuthority> authorities = Arrays
		.asList(new GrantedAuthority[] { new SimpleGrantedAuthority(AuthoritiesConstants.USER) });

	GluuUser user = new GluuUser(tokenResponse.get().getIdToken(), userInfoResponse.getClaims(), authorities);
	SecurityContextHolder.getContext()
		.setAuthentication(new UsernamePasswordAuthenticationToken(user, "", authorities));

	return "redirect:/user";
}
```

And gets redirected to /user page
![/user page](https://github.com/worm333/docs/blob/master/sources/img/examples/oxd-spring/Screen%20Shot%202016-05-23%20at%2012.37.48%20AM.png)



