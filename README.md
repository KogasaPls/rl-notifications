# rl-notifications
RuneLite notification daemon for Linux, using Python/GTK3 (Pypy3/PyGObject). Intended as a visual aid while multi-logging, by allowing each RuneLite client to have its own visually distinct and customizable notifications. 

![image](https://user-images.githubusercontent.com/87504405/149548736-b27dadf6-6dde-4f1f-a8b9-74f4de3edc24.png)

See it in action: https://streamable.com/yx2m3c

* For personal use; useless without some tinkering. In particular: my usernames are hardcoded, and I position the notification windows externally via Sway.

* The main script (rl-notification.py) listens to a socket for notifications, then displays a GTK3 window with title $user and message $message. It creates a separate persistent window for each different $user, so that they can be positioned on top of their respective RuneLite clients. The script automatically colors the notification box according to the content of the message, and this can be easily tweaked/customized.

* The auxiliary script rl-notification-client.py sends RuneLite notifications to the socket. It should be triggered by Dunst, e.g. via
```
### ~/.config/dunst/dunstrc
...
[runelite]
  summary = "RuneLite*"
  script = "~/git/runelite-notifications/rl-notification-client.py"
  skip_display = yes
```

* You must enable notifications in RuneLite, as well as the setting "show username in title bar." I also recommend the stock plugin "Idle Notifications" and the Plugin Hub plugin "Chat Notifications," which I use as follows:

![image](https://user-images.githubusercontent.com/87504405/149544548-35e32e22-cd5f-498a-b1ae-0b67ee9d9257.png)

* Instead of hiding or destroying the window, the script shrinks it to a tiny size (~1x3 pixels) and makes it transparent. This eliminates an annoying microstutter in Sway which I believe is related to the use of Sway to position the windows.
* The use of pypy3 over cython is nonessential.
* The windows disappear after 3 seconds without a new notification on the same client. Clicking them will cause them to disappear instantly.
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

I am not a programmer; these scripts were hobbled together through trial, error, and Google. As such, there are things I've done suboptimally, so please let me know if you have any suggestions.
