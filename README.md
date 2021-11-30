# Awaaz.De Rest APIs

This repository contains SDKs to consume/call Awaaz.De REST APIs.


## What is  Awaaz.De APIs?

Want to learn more about it ? Check this `http://api.awaaz.de/\<organization\>/v1/docs/`
Here, `\<organization>\` is the name of your registered organization.


## Prerequisites

For Java

Jackson (See http://wiki.fasterxml.com/JacksonHome)
Jersy Bundle (See https://jersey.java.net/)

Use Maven to download dependency and mavenize the java project.

For PHP
   * Guzzle (See https://github.com/guzzle/guzzle)
   * Note that guzzle is already included under vendor folder, but you might want to download and use latest version.
   

For Python
   * Just create virtual env and run command `pip install -r requirements.txt`
   
    
## Usage

To use sample for java language.

   * Copy the java folder on your local environment.
   * Download the required jar dependency using maven. `mvn install` (alternatively you can use your favourite editor and update the maven project)
   * Refer to `APIDemo.java` file for reference on how to call different apis.

To use sample for php language.

   * Copy the php folder on your local environment.
   * Run demo - You can copy paste the demo folder on your server, change the auth details and check various example described there


To use sample for python language.

   * Copy the python folder on your local environment.
   * Refer to `example.py` file for reference on how to call different apis.

## More help

   * [API Reference](http://api.awaaz.de/<organization>/v1/docs/)
   * [Reporting issues / feature requests](https://github.com/awaazde/awaazde-api-client/issues)


###### Note that this Demo works for only v2.0 of Awaaz De app. If you are looking for old version, download release v1.0
