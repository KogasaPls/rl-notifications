# rl-notifications
RuneLite notification daemon for Linux. Intended to aid in multi-logging, by allowing each RuneLite client to have its own visually distinct and customizable notifications. See the demo: https://streamable.com/yx2m3c

For personal use; useless without some tinkering. In particular, my usernames are hardcoded, and I position the notification windows externally via Sway.

This program (rl-notification.py) listens to a socket (/tmp/rl-notification) for a string formatted as "$user $message", then displays a GTK3 window with title $user and message $message. It creates a separate persistent window for each different $user, so that they can be positioned on top of their respective RuneLite clients of origin. The script automatically colors the notification box according to the content of the message. 

The auxiliary program rl-notification-client.py should be triggered by Dunst, e.g. via
```
### ~/.config/dunst/dunstrc
...
[runelite]
  summary = "RuneLite*"
  script = "~/git/runelite-notifications/rl-notification-client.py"
  skip_display = yes
```
and will send RuneLite notifications' username and body text to the socket. 


* Instead of hiding or destroying the window, the script shrinks it to a tiny size (~1x3 pixels) and makes it transparent. This eliminates an annoying microstutter in Sway which I believe is related to the use of Sway to position the windows.
* The use of pypy3 over cython is nonessential.
* My Sway config includes the following code to set up my Workspace 4 as seen in the demo, and position the notification windows. With 1-pixel borders and a 2560x1440 monitor, this configuration can be used to create one 1280x720 window and two smaller 16x9 windows (ideal for streaming). The large side gaps and thin inner gaps are intended to center the windows and reduce eye/mouse travel between them. This is my preferred layout for playing 1 account + 2 rune dragon alts.
```
### ~/.config/sway/config
...
#RuneLite workspace on workspace 4
workspace 4 gaps inner 10
workspace 4 gaps outer 10
workspace 4 gaps left 239
workspace 4 gaps right 239
workspace 4 gaps top 40
workspace 4 gaps bottom 40
for_window [class="net-runelite-client-RuneLite"] move to workspace 4
...
# rl-notifications
no_focus [app_id="rl-notification.py"]
for_window [app_id="rl-notification.py" title="Potapto"] floating enable, border none, move to workspace 4, move absolute position 2810 81, sticky disable
for_window [app_id="rl-notification.py" title="Maldemort"] floating enable, border none, move absolute position 2810 813, sticky disable
for_window [app_id="rl-notification.py" title="Potaptwo"] floating enable, border none, move absolute position 3846 813, sticky disable
```

* You must enable notifications in RuneLite, as well as the setting "show username in title bar." I also recommend the stock plugin "Idle Notifications" and the Plugin Hub plugin "Chat Notifications," which I use as follows:

![image](https://user-images.githubusercontent.com/87504405/149544548-35e32e22-cd5f-498a-b1ae-0b67ee9d9257.png)

