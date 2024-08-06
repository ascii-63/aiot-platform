# ZEPHYR USEFUL NOTES

## Application development

1. In this document, we’ll assume:

    - your application directory, `<app>`, is something like `<home>/zephyrproject/app`
    - its build directory is `<app>/build`

    Keeping your application inside the workspace (`<home>/zephyrproject`) makes it easier to use west build and other commands with it. 
(You can put your application anywhere as long as `ZEPHYR_BASE` is set appropriately, though.)

2. Here are the files in a simple Zephyr application:

   ```text
    <app>
    ├── CMakeLists.txt
    ├── app.overlay
    ├── prj.conf
    ├── VERSION
    └── src
        └── main.c
   ```

3. Zephyr workspace application

    An application located within a workspace, but outside the zephyr repository itself, is referred to as a Zephyr workspace application. 
    In the following example, app is a Zephyr workspace application:
    ```text
    zephyrproject/
    ├─── .west/
    │    └─── config
    ├─── zephyr/
    ├─── bootloader/
    ├─── modules/
    ├─── tools/
    ├─── <vendor/private-repositories>/
    └─── applications/
        └── app/
    ```

4. Important Build System Variables

    - `ZEPHYR_BASE`: Zephyr base variable used by the build system.
    - `BOARD`: Selects the board that the application’s build will use for the default configuration.
    - `CONF_FILE`: Indicates the name of one or more Kconfig configuration fragment files.
    - `EXTRA_CONF_FILE`: Additional Kconfig configuration fragment files. Multiple filenames can be separated with either spaces or semicolons. 
    This can be useful in order to leave `CONF_FILE` at its default value, but “mix in” some additional configuration options.
    - `DTC_OVERLAY_FILE`: One or more devicetree overlay files to use.
    - `EXTRA_DTC_OVERLAY_FILE`: Additional devicetree overlay files to use. Multiple files can be separated with semicolons. 
    This can be useful to leave `DTC_OVERLAY_FILE` at its default value, but “mix in” some additional overlay files.
    - `ZEPHYR_MODULES`: A *CMakeLists* containing absolute paths of additional directories with source code, Kconfig, etc. 
    that should be used in the application build.
    If you set this variable, it must be a complete list of all modules to use, as the build system will not automatically pick up any modules from west.
    - `EXTRA_ZEPHYR_MODULES`: Like `ZEPHYR_MODULES`, except these will be added to the list of modules found via west, instead of replacing it.
    - `FILE_SUFFIX`: Optional suffix for filenames that will be added to Kconfig fragments and devicetree overlays.

5. The variables `BOARD`, `CONF_FILE`, and `DTC_OVERLAY_FILE` can be supplied to the build system in 3 ways (in order of precedence):
    - As a parameter to the `west build` or `cmake` invocation via the `-D` command-line switch. 
If you have multiple overlay files, you should use quotations, `"file1.overlay;file2.overlay"`
    - As Environment Variables.
    - As a `set(<VARIABLE> <VALUE>)` statement in your `CMakeLists.txt`

6. Simple example `CMakeLists.txt`:
    ```cmake
    set(BOARD qemu_x86)

    find_package(Zephyr)
    project(my_zephyr_app)

    target_sources(app PRIVATE src/main.c)
    ```
 
7. Kconfig Configuration

    Application configuration options are usually set in `prj.conf` in the application directory. 
    For example, C++ support could be enabled with this assignment:
    ```text
    CONFIG_CPP=y
    ```

8. Building an Application

    As an example, let’s build the Hello World sample for the `reel_board`:
    
    Using west:
    ```bash
    west build -b reel_board samples/hello_world
    ```

    Using CMake directly:
    ```bash
    # Use cmake to configure a Make-based buildsystem:
    cmake -Bbuild -DBOARD=reel_board samples/hello_world

    # Now run the build tool on the generated build system:
    make -Cbuild
    ```

9. Rebuilding an Application
    ```bash
    cd <app>/build

    # delete the application’s generated files, except for the .config file
    west build -t clean

    # Or, delete all generated files, including the .config files
    west build -t pristine
    ```

10. Run an Application

    - Running on a Board
    ```bash
    west flash
    ```
    - Running natively (Linux)
    ```bash
    # First, build the app for native_sim
    west build -b native_sim app

    west build -t run
    ```

    - Running in an Emulator:

    Firstly, build the application for x86-based board: Set `BOARD` to `qemu_x86`
    ```
    west build -t run
    ```

## Debugging

1. Application Debugging
    