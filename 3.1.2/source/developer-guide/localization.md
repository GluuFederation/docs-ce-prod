# Localization of Gluu Server Admin UI

oxAuth contains the following resource bundles: 

- [oxauth_en.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/oxauth_en.properties)   
- [oxauth_bg.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/oxauth_bg.properties)  
- [oxauth_de.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/oxauth_de.properties)   
- [oxauth_es.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/oxauth_es.properties)    
- [oxauth_fr.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/oxauth_fr.properties)    
- [oxauth_it.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/oxauth_it.properties)   
- [oxauth_ru.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/oxauth_ru.properties)     
- [oxauth_tr.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/oxauth_tr.properties)   

These properties files store the translatable text of the messages to be displayed.
The default properties file, which is called [messages_en.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/messages_en.properties), contains the following lines:
```
.......
login.login=Login
login.register=Register
.......
```
Now that the messages are in a properties file, they can be translated into various languages. No changes to the source code are required. For example to use the French version of the oxAuth the [messages_fr.properties](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/resources/messages_fr.properties) should contains these lines:
```
.......
login.login=S'identifier
login.register=Registre
.......
```
Notice that the values to the right side of the equal sign have been translated but that the keys on the left side have not been changed. These keys must not change, because they will be referenced when oxAuth fetches the translated text.

To add translation for not yet supported languages, just create new properties file in [resource](https://github.com/GluuFederation/oxAuth/tree/master/Server/src/main/resources) folder and name it messages_[language_code].properties, then add language code as supported-locale to the [faces-config.xml](https://github.com/GluuFederation/oxAuth/blob/master/Server/src/main/webapp/WEB-INF/faces-config.xml#L9).




