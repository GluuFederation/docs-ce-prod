# Brute force protection

Starting from version 3.1.4 the Gluu Server has service which can help in protection infrastructure against brute force atttack. It can be enabled in password valation fflow.
In order to control it thee is new section in oxAuth configuration with next default values:

	"authenticationProtectionConfiguration": {
		"attemptExpiration": 15,
		"maximumAllowedAttemptsWithoutDelay": 4,
		"delayTime": 2,
		"bruteForceProtectionEnabled": false
        }

Here is description of each property:
 - `attemptExpiration`. How long store in cache information about particular login attempt. It's needed to count login attempts withing specified period of time
 - `maximumAllowedAttemptsWithoutDelay`. How many attempts application allow without delay
 - `delayTime`. Delay time in seconds after reaching maximumAllowedAttemptsWithoutDelay limit.
 - `bruteForceProtectionEnabled`. Enable or disable service, This functionality can be enabled dynamically. All other values requires restart

