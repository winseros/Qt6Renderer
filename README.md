# QT6 Renderer

The plugin for pretty printing [Qt][qt] types by [CLion][clion] debugger.

[qt]: https://www.qt.io/
[clion]: https://www.jetbrains.com/clion/

## Qt versions support
* 6.x

See the note about some problems with 6.4.2 and below.

## Qt types support
* [See here for lldb](./python/lldb)
* [See here for gdb](./python/gdb)

You can use the [example project](./example-project) for testsing.

## Debuggers support
* LLDB
* GDB

## Operating systems tested on
* Windows
  * Bundled LLDB 9
  * Bundled GDB 13 
* Linux
  * Bundled LLDB 13
  * Bundled GDB 13

## Architectures tested on
* x64

## Requirements

This plugin needs Debug information for Qt.

If you installed Qt with Qt Online installer, ensure you have installed
the `Qt Debug Information files`:

![Checkbox for QtDebug Information files](images/Qt_Debug_Information_files_checkbox.png)

If you are using Arch Linux, you need to install `qt6-base-debug` package.
You can install manually (by specifying the url), or by enabling global repo. See [wiki](https://wiki.archlinux.org/title/Debugging/Getting_traces#Installing_debug_packages).
```
sudo pacman -U https://geo.mirror.pkgbuild.com/extra-debug/os/x86_64/qt6-base-debug-6.7.2-1-x86_64.pkg.tar.zst
```

## Troubleshooting

### Qt Types are not pretty printed

First, ensure you have satisfied [requirements](#Requirements).

Open the example project in CLion. Set a breakpoint somewhere in the `main()` function, and start a debugging session (Shift + F9 by default).

Now click on the debugger console tab (this will be "GDB" or "LLDB" depending on toolchain you use), and enter the command
for a quick check if a specific version includes type metainfo.

For the gdb console, use command:
```
python print(gdb.parse_and_eval('*(&qtHookData)'))
```

For lldb console, use command:
```
script print(lldb.target.FindFirstGlobalVariable('qtHookData').GetPointeeData(2, 1))
```

There are problematic Qt versions, for which the debugger is unable to extract type metadata.

For example, for Qt 6.4.2 in gdb console you will get `<data variable, no debug info>` message:

![No debug info gdb](images/debug_info_gdb_bad.png)

Consider switching to another version of Qt.

For the supported Qt version, you will get some debug info.

For gdb, that looks like `{3, 7, 394754, 0, 0, 0, 22}`:

![Have debug info gdb](images/debug_info_gdb_good.png)

For lldb, that looks like `02 07 06 00 00 00 00 00`:

![Have debug info lldb](images/debug_info_lldb_good.png)
