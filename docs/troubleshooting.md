# Troubleshooting

## missing libxcb-cursor0

when starting the demo on Ubuntu 20.04 by running

```bash
poetry run python pyside_demo
```

you may get the following error:

```bash
qt.qpa.plugin: From 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed to load the Qt xcb platform plugin.
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: minimal, vkkhrdisplay, wayland, eglfs, minimalegl, vnc, xcb, offscreen, wayland-egl, linuxfb.

Aborted (core dumped)
```

The error message indicates that your system is missing a required library for the Qt xcb platform plugin. To resolve this issue, you need to install the `libxcb-cursor0` package. Here are the steps to fix this problem:

1. Open a terminal on your Ubuntu system.

2. Update your package list:

   ```bash
   sudo apt update
   ```

3. Install the required package:

   ```bash
   sudo apt install libxcb-cursor0
   ```

4. If the above package is not found, you may need to install these additional packages:

   ```bash
   sudo apt install libxcb-xinerama0 libxkbcommon-x11-0
   ```

5. After installation, try running your PySide6 project again.

If you're still encountering issues after installing these packages, you may need to install additional Qt dependencies:

   ```bash
   sudo apt install libgl1-mesa-dev
   ```
