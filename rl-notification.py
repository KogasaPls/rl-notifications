#!/usr/bin/env pypy3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib
import sys
import os
import subprocess
import re
import screeninfo
import socket
import time

socket_path = '/tmp/rl-notification'

timers = {"Potapto": 0, "Maldemort": 0, "Potaptwo": 0}

nord0 = '46,52,64'  # darkest gray
nord1 = '59,66,82'  # darkerer gray
nord2 = '67,76,94'  # darker gray
nord3 = '76,86,106'  # dark gray
nord4 = '216,222,233'  # gray
nord5 = '229,233,240'  # light gray
nord6 = '236,239,244'  # white
nord7 = '143,188,187'  # blue-green
nord8 = '136,192,208'  # cyan
nord9 = '129,161,193'  # pale blue
nord10 = '94,129,172'  # dark blue
nord11 = '191,97,106'  # red
nord12 = '208,135,112'  # orange
nord13 = '235,203,139'  # yellow
nord14 = '163,190,140'  # green
nord15 = '180,142,173'  # magenta
fgColor = nord6


def bgColor(message):
    if re.match("You have low hitpoints!", message):
        return nord11
    elif re.match("You have low prayer!", message):
        return nord8
    elif re.match(".*antifire.*", message):
        return nord15
    elif re.match(".*divine.*", message):
        return nord14
    else:
        return nord10


# Make sure the socket does not already exist
try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.bind(socket_path)
s.listen()


# In Sway, creating a new window causes a brief stutter. Make it tiny and
# transparent instead of hiding it.


def blank(user):
    lookup = {"Potapto": Potapto, "Maldemort": Maldemort, "Potaptwo": Potaptwo}
    win = lookup.get(user, None)
    if win is not None:
        Gtk.Widget.set_opacity(win, 0.0)
        win.set_size_request(0, 0)
        win.label.set_text('')
        css = "window.background.{} * {{ " \
            "opacity: 0; padding: 0px 0px 0px 0px; border: 0px; font-size: 0; }}".format(user)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        winContext = win.get_style_context()
        winContext.add_class(user)
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        timers[user] = 0  # clear timer


def redrawBox(user, message=''):
    lookup = {"Potapto": Potapto, "Maldemort": Maldemort, "Potaptwo": Potaptwo}
    win = lookup.get(user, None)
    if win is not None:
        win.set_size_request(300, 60)
        win.label.set_text(message)
        css = "window.background.{} * {{ " \
            "opacity: 1; font-family: Iosevka; font-weight: 500; font-size: 12pt; " \
            "padding: 15px 15px 15px 15px; border: 2px solid rgba(216, 222, 233, 1); " \
            "background-color: rgba({}, 1); color: rgb({}); }}".format(user, bgColor(message), fgColor)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        winContext = win.get_style_context()
        winContext.add_class(user)
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        Gtk.Widget.set_opacity(win, 1)
        ## blank after 3 seconds, starting over if there's already a timer
        if timers[user] != 0:
            GLib.source_remove(timers[user])
        timers[user] = GLib.timeout_add_seconds(3, lambda: blank(user))


def listener(io, cond, sock):
    conn = sock.accept()[0]
    GLib.io_add_watch(GLib.IOChannel(conn.fileno()), 0, GLib.IOCondition.IN, handler, conn)
    return True


def handler(io, cond, sock):
    line = sock.recv(4096).strip().decode('utf-8')
    if not line:
        return False
    else:
        user = line.split(' ', 1)[0]
        message = line.split(' ', 1)[1]
        lookup = {"Potapto": Potapto, "Maldemort": Maldemort, "Potaptwo": Potaptwo}
        win = lookup.get(user, None)
        timer = timers.get(user, None)
#        print("User: {}\nMessage: {}".format(user, message))
        redrawBox(user, message)
        return True


for user in ["Potapto", "Maldemort", "Potaptwo"]:
    exec(user + ' = Gtk.Window()')
    win = eval(user)
    Gtk.Window.set_title(win, user)
    Gtk.Widget.set_opacity(win, 0.0)
    win.set_size_request(0, 0)
    win.set_resizable(False)
    win.label = Gtk.Label(
        label=''
    )
    win.label.set_line_wrap(True)
    win.label.set_max_width_chars(32)
    win.label.set_justify(2)
    win.box = Gtk.EventBox()
    win.box.connect('button-press-event', lambda x, y, z=user: blank(z))
    win.add(win.box)
    win.box.add(win.label)
    win.show_all()

GLib.io_add_watch(GLib.IOChannel(s.fileno()), 0, GLib.IOCondition.IN, listener, s)
Gtk.main()
