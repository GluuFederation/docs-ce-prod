# Gluu Server Clearing Logs

The option "clear-logs" has been introduced first time in version 3.1.2. This option is used to clear all logs including system logs. All log files with the extension .log are removed. This helps in troubleshooting the gluu-server in case of some trouble. This option is very helpful during research and development purposes. We discourage the use of the option in production in case requisite logs are not backed-up. Later more features are planned to be added. Please consider this as work in progress.

## Usage

`# service gluu-server-3.1.2 clear-logs`
