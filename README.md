Spawnkill Plugin for BigBrotherBot
==================================

BigBrotherBot plugin useful to automatically manage spawnkilling on game servers.<br>
**NOTE**: *this plugin has not been tested on a game server yet: if you wish to try it, please report any bug.*


## How to install

### Installing the plugin

* Copy **spawnkill.py** into **b3/extplugins**
* Copy **plugin_spawnkill.ini** into **b3/extplugins/conf**
* Load the plugin in your **b3.xml** configuration file

### Requirements

In order to use this plugins you need to have b3 1.10-dev installed: http://files.cucurb.net/b3/daily/.<br>
You need to have a b3 version released after the 21st December 2013: the plugin makes use of several changes provided in the plugin.py module which are available as form this release date.<br>
The plugin works with all the game providing **b3.events.EVT_CLIENT_SPAWN** event. Here is a list of currently supported games:
* iourt42
* bfbc2
* bf3
* bf4

## Support

For support regarding this very plugin you can find me on IRC on #goreclan** @ **Quakenet**<br>
For support regarding Big Brother Bot you may ask for help on the official website: http://www.bigbrotherbot.net