#!/usr/bin/python
# Terminator by Chris Jones <cmsj@tenshu.net>
# GPL v2 only
"""sqlmode.py - Terminator Plugin creating an editor + sql client in the terminal"""

import time
import gtk
import gobject

import terminatorlib.plugin as plugin
from terminatorlib.translation import _
from terminatorlib.util import err, dbg
from terminatorlib.version import APP_NAME

AVAILABLE = ['SqlMode']

class SqlMode(plugin.MenuItem):
    """Add custom commands to the terminal menu"""
    capabilities = ['terminal_menu']

    def __init__(self):
        plugin.MenuItem.__init__(self)

    def callback(self, menuitems, menu, terminal):
        """Add our menu items to the menu"""
        sqlMode = gtk.MenuItem("SQL Mode")
        sqlModeMenu = gtk.Menu()
        sqlMode.set_submenu(sqlModeMenu)
        mySql = gtk.CheckMenuItem("MySQL")
        if terminal.keypress_callback == self.mysql_keypress:
            mySql.set_active(True)
        psql = gtk.CheckMenuItem("PostgreSQL")
        if terminal.keypress_callback == self.psql_keypress:
            psql.set_active(True)
        mssql = gtk.CheckMenuItem("SQL Server")
        if terminal.keypress_callback == self.mssql_keypress:
            mssql.set_active(True)
        mySql.connect("activate", self.setMySqlMode, terminal)
        psql.connect("activate", self.setPostgresqlMode, terminal)
        mssql.connect("activate", self.setSQLServerMode, terminal)
        sqlModeMenu.append(mySql)
        sqlModeMenu.append(psql)
        sqlModeMenu.append(mssql)
        menuitems.append(sqlMode)

    def setMySqlMode(self, _widget, terminal):
        """Set Sql Mode to MySQL"""
        if terminal.keypress_callback != self.mysql_keypress:
            terminal.keypress_callback = self.mysql_keypress
        else:
            terminal.keypress_callback = None

    def mysql_keypress(self, terminal, event):
        # Check for F5
        if (event.keyval == 65474):
            terminal.vte.feed_child_binary(b'\x1b\x5b\x31\x35\x7e')
            time.sleep(0.2)
            terminal.emit('print', 'next', '\n#q\n\\. /tmp/buffer.sql\n')

    def setPostgresqlMode(self, _widget, terminal):
        """Set Sql Mode to PostgreSQL"""
        if terminal.keypress_callback != self.psql_keypress:
            terminal.keypress_callback = self.psql_keypress
        else:
            terminal.keypress_callback = None

    def psql_keypress(self, terminal, event):
        # Check for F5
        if (event.keyval == 65474 and event.state == 16):
            terminal.vte.feed_child_binary(b'\x1b\x5b\x31\x35\x7e')
            time.sleep(0.2)
            terminal.emit('print', 'next', '\n#q\n\\i /ram/buffer.sql\n')
        # Check for Alt + F1
        if (event.keyval == 65470 and event.state == 24):
            # ^[O1;3P
            terminal.vte.feed_child_binary(b'\x1b\x4f\x31\x3b\x33\x50')
            time.sleep(0.2)
            terminal.emit('print', 'next', '\n#q\n\\i /ram/buffer.sql\n')
        # Check for Alt + F2
        if (event.keyval == 65471 and event.state == 24):
            # ^[O1;3Q
            terminal.vte.feed_child_binary(b'\x1b\x4f\x31\x3b\x33\x51')
            time.sleep(0.2)
            terminal.emit('print', 'next', '\n#q\n\\i /ram/buffer.sql\n')
        # Check for Alt + F5
        if (event.keyval == 65474 and event.state == 24):
            # ^[[15;3~
            terminal.vte.feed_child_binary(b'\x1b\x5b\x31\x35\x3b\x33\x7e')
            time.sleep(0.2)
            terminal.emit('print', 'next', '\n#q\n\\i /ram/buffer.sql\n')
        # Check for Alt + Space
        if (event.keyval == 32 and event.state == 24):
            # ^[ 
            terminal.vte.feed_child_binary(b'\x1b\x20')
            time.sleep(0.2)
            terminal.emit('print', 'next', '\n#q\n\\i /ram/buffer.sql\n')
        # Check for Ctrl + Enter
        if (event.keyval == 65293 and event.state == 20):
            # ^[[24;9~
            terminal.vte.feed_child_binary(b'\x1b\x5b\x32\x34\x3b\x39\x7e')
            time.sleep(0.2)
            terminal.emit('print', 'next', '\n#q\n\\i /ram/buffer.sql\n')

    def setSQLServerMode(self, _widget, terminal):
        """Set Sql Mode to SQL Server"""
        if terminal.keypress_callback != self.mssql_keypress:
            terminal.keypress_callback = self.mssql_keypress
        else:
            terminal.keypress_callback = None

    def mssql_keypress(self, terminal, event):
        # Check for F5
        if (event.keyval == 65474):
            terminal.vte.feed_child_binary(b'\x1b\x5b\x31\x35\x7e')
            time.sleep(0.2)
            terminal.emit('print', 'next', '\n#q\n\\shell cat /tmp/buffer.sql > /dev/null\n\\loop /tmp/buffer.sql\n')
