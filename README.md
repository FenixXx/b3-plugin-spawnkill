Spawnkill Plugin for BigBrotherBot [![BigBrotherBot](http://i.imgur.com/7sljo4G.png)][B3]
==================================

A [BigBrotherBot][B3] plugin useful to automatically manage spawnkilling on Urban Terror 4.2 game servers.

Download
--------

Latest version available [here](https://github.com/FenixXx/b3-plugin-spawnkill/archive/master.zip).

Installation
------------

* copy the `spawnkill.py` file into `b3/extplugins`
* copy the `plugin_spawnkill.ini` file in `b3/extplugins/conf`
* add to the `plugins` section of your `b3.xml` config file:

  ```xml
  <plugin name="spawnkill" config="@b3/extplugins/conf/plugin_spawnkill.ini" />
  ```

Requirements
------------

* Urban Terror 4.2 server [g_modversion >= 4.2.015]
* iourt42 parser [version >= 1.19]

Support
-------

If you have found a bug or have a suggestion for this plugin, please report it on the [B3 forums][Support].

[B3]: http://www.bigbrotherbot.net/ "BigBrotherBot (B3)"
[Support]: http://forum.bigbrotherbot.net/releases/spawnkill-plugin/ "Support topic on the B3 forums"

[![Build Status](https://travis-ci.org/FenixXx/b3-plugin-spawnkill.svg?branch=master)](https://travis-ci.org/FenixXx/b3-plugin-spawnkill)