#
# Spawnkill Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2013 Daniele Pantaleone <fenix@bigbrotherbot.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__ = 'Fenix'
__version__ = '1.1'

import b3
import b3.plugin
import b3.events
from ConfigParser import NoOptionError


class SpawnkillPlugin(b3.plugin.Plugin):

    _adminPlugin = None

    _penalties = dict()

    _settings = dict(
        hit=dict(
            maxlevel=40,
            delay=2,
            penalty='warn',
            duration=3,
            reason='^7do not shoot to spawning players!'
        ),
        kill=dict(
            maxlevel=40,
            delay=3,
            penalty='warn',
            duration=5,
            reason='^7spawnkilling is not allowed on this server!'
        )
    )

    ####################################################################################################################
    ##                                                                                                                ##
    ##   STARTUP                                                                                                      ##
    ##                                                                                                                ##
    ####################################################################################################################

    def __init__(self, console, config=None):
        """
        Build the plugin object
        """
        b3.plugin.Plugin.__init__(self, console, config)
        if self.console.gameName != 'iourt42':
            self.critical("unsupported game : %s" % self.console.gameName)
            raise SystemExit(220)

    def onLoadConfig(self):
        """\
        Load plugin configuration
        """
        for index in ('hit', 'kill'):

            try:
                self._settings[index]['maxlevel'] = self.console.getGroupLevel(self.config.get(index, 'maxlevel'))
            except (NoOptionError, KeyError), e:
                self.warning('could not load %s/maxlevel from config file: %s' % (index, e))

            try:
                self._settings[index]['delay'] = self.config.getint(index, 'delay')
            except (NoOptionError, ValueError), e:
                self.warning('could not load %s/delay from config file: %s' % (index, e))

            try:
                if self.config.get(index, 'penalty') not in ('warn', 'kick', 'ban'):
                    # specified penalty is not supported by this plugin: fallback to default
                    raise ValueError('invalid penalty specified: %s' % self.config.get(index, 'penalty'))
                self._settings[index]['penalty'] = self.config.get(index, 'penalty')
            except (NoOptionError, ValueError), e:
                self.warning('could not load %s/penalty from config file: %s' % (index, e))

            try:
                self._settings[index]['duration'] = self.config.getDuration(index, 'duration')
            except (NoOptionError, ValueError), e:
                self.warning('could not load %s/duration from config file: %s' % (index, e))

            try:
                self._settings[index]['reason'] = self.config.get(index, 'reason')
            except NoOptionError, e:
                self.warning('could not load %s/reason from config file: %s' % (index, e))

            # print current configuration in the log file for later inspection
            self.debug('setting %s/maxlevel: %s' % (index, self._settings[index]['maxlevel']))
            self.debug('setting %s/delay: %s' % (index, self._settings[index]['delay']))
            self.debug('setting %s/penalty: %s' % (index, self._settings[index]['penalty']))
            self.debug('setting %s/duration: %s' % (index, self._settings[index]['duration']))
            self.debug('setting %s/reason: %s' % (index, self._settings[index]['reason']))

    def onStartup(self):
        """\
        Initialize plugin settings
        """
        # get the admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('could not find admin plugin')
            return False

        # register our commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

        # register the events needed
        self.registerEvent(self.console.getEventID('EVT_CLIENT_SPAWN'), self.onSpawn)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_DAMAGE'), self.onDamage)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_KILL'), self.onKill)

        # register penalty handlers
        self._penalties['warn'] = self.warnClient
        self._penalties['kick'] = self.kickClient
        self._penalties['ban'] = self.banClient

        # notice plugin startup
        self.debug('plugin started')

    ####################################################################################################################
    ##                                                                                                                ##
    ##   EVENTS                                                                                                       ##
    ##                                                                                                                ##
    ####################################################################################################################

    def onSpawn(self, event):
        """\
        Handle EVT_CLIENT_SPAWN
        """
        client = event.client
        client.setvar(self, 'spawntime', self.console.time())

    def onDamage(self, event):
        """\
        Handle EVT_CLIENT_DAMAGE
        """
        self.onSpawnKill('hit', event.client, event.target)

    def onKill(self, event):
        """\
        Handle EVT_CLIENT_KILL
        """
        self.onSpawnKill('kill', event.client, event.target)

    ####################################################################################################################
    ##                                                                                                                ##
    ##   FUNCTIONS                                                           #                                        ##
    ##                                                                                                                ##
    ####################################################################################################################

    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func
        return None

    def onSpawnKill(self, index, client, target):
        """\
        Handle possible spawn(hit|kill) events
        """
        # checking for correct client level
        if client.maxLevel >= self._settings[index]['maxlevel']:
            self.verbose('bypassing spawn%s check: client <%s> is a high group level player' % (index, client.cid))
            return

        # checking for spawntime mark in client object
        if not target.isvar(self, 'spawntime'):
            self.verbose('bypassing spawn%s check: client <%s> has no spawntime marked' % (index, target.cid))
            return

        # if we got a spawn(hit|kill) action, applies the configured penalty
        if self.console.time() - target.var(self, 'spawntime').toInt() < self._settings[index]['delay']:
            self._penalties[self._settings[index]['penalty']](index, client)

    def warnClient(self, index, client):
        """\
        Warn a client for spawnkilling
        """
        self.debug('applying warning penalty on client <%s>: spawn%s detected!' % (client.cid, index))
        self._adminPlugin.warnClient(client,
                                     self._settings[index]['reason'],
                                     admin=None,
                                     timer=False,
                                     newDuration=self._settings[index]['duration'])

    def kickClient(self, index, client):
        """\
        Kick a client for spawnkilling
        """
        self.debug('applying kick penalty on client <%s>: spawn%s detected!' % (client.cid, index))
        client.kick(self._settings[index]['reason'])

    def banClient(self, index, client):
        """\
        Ban a client for spawnkilling
        """
        self.debug('applying ban penalty on client <%s>: spawn%s detected!' % (client.cid, index))
        client.tempban(reason=self._settings[index]['reason'], duration=self._settings[index]['duration'])
