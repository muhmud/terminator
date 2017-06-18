#!/usr/bin/python
# Terminator by Chris Jones <cmsj@tenshu.net>
# GPL v2 only
"""sqlmode.py - Terminator Plugin creating an editor + sql client in the terminal"""

import time
import subprocess

from gi.repository import Gtk, GObject

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
        sqlMode = Gtk.MenuItem("SQL Mode")
        sqlModeMenu = Gtk.Menu()
        sqlMode.set_submenu(sqlModeMenu)
        mySql = Gtk.CheckMenuItem("MySQL")
        psql = Gtk.CheckMenuItem("PostgreSQL")
        mssql = Gtk.CheckMenuItem("SQL Server")
        if terminal.keypress_callback != None:
            mySql.set_active(terminal.keypress_callback == self.mysql_keypress)
            psql.set_active(terminal.keypress_callback == self.psql_keypress)
            mssql.set_active(terminal.keypress_callback == self.mssql_keypress)    
        mySql.connect("activate", self.setMySqlMode, terminal)
        psql.connect("activate", self.setPostgresqlMode, terminal)
        mssql.connect("activate", self.setSQLServerMode, terminal)
        sqlModeMenu.append(mySql)
        sqlModeMenu.append(psql)
        sqlModeMenu.append(mssql)
        menuitems.append(Gtk.SeparatorMenuItem())
        menuitems.append(sqlMode)

    def psql_operation(self, terminal, code):
        self.start_operation(terminal, code)
        self.wait_on_operation()
        terminal.emit('print', 'next', '\n#q\n\\i /tmp/buffer.sql\n')
        
    def start_operation(self, terminal, code):
        with open('/tmp/buffer-status', 'w') as f: f.write("...")
        terminal.vte.feed_child_binary(code)
        
    def wait_on_operation(self):
        counter = 0
        while counter < 50:
            subprocess.call(['sync'])
            with open('/tmp/buffer-status', 'r') as f:
                if f.read() == 'DONE':
                    break
                else:
                    time.sleep(0.1)
                    counter += 1
        
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
        counter = 0
        if (event.keyval == 65474 and event.state == 16):
            self.psql_operation(terminal, b'\x1b\x5b\x31\x35\x7e')
        # Check for Alt + F1
        if (event.keyval == 65470 and event.state == 24):
            # ^[O1;3P
            self.psql_operation(terminal, b'\x1b\x4f\x31\x3b\x33\x50')
        # Check for Alt + F2
        if (event.keyval == 65471 and event.state == 24):
            # ^[O1;3Q
            self.psql_operation(terminal, b'\x1b\x4f\x31\x3b\x33\x51')
        # Check for Alt + F5
        if (event.keyval == 65474 and event.state == 24):
            # ^[[15;3~
            self.psql_operation(terminal, b'\x1b\x5b\x31\x35\x3b\x33\x7e')
        # Check for Alt + F6
        if (event.keyval == 65475 and event.state == 24):
            # ^[[17;3~
            self.psql_operation(terminal, b'\x1b\x5b\x31\x37\x3b\x33\x7e')
        # Check for Alt + F7
        if (event.keyval == 65476 and event.state == 24):
            # ^[[18;3~
            self.psql_operation(terminal, b'\x1b\x5b\x31\x38\x3b\x33\x7e')
        # Check for Alt + D
        if (event.keyval == 100 and event.state == 24):
            # ^[[24;9{
            self.psql_operation(terminal, b'\x1b\x5b\x32\x34\x3b\x39\x7b')
        # Check for Alt + Shift + D
        if (event.keyval == 68 and event.state == 25):
            # ^[[24;9}
            self.psql_operation(terminal, b'\x1b\x5b\x32\x34\x3b\x39\x7d')
        # Check for Alt + Space
        if (event.keyval == 32 and event.state == 24):
            # ^[
            self.psql_operation(terminal, b'\x1b\x20')
        # Check for Ctrl + Enter
        if (event.keyval == 65293 and event.state == 20):
            # ^[[24;9~
            self.psql_operation(terminal, b'\x1b\x5b\x32\x34\x3b\x39\x7e')

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
