# Create a new project

This section covers the creation of a new Unity project with RPG Power Forge !

```admonish success title="Oh yeah"
This section is up-to-date for Unity 6000.0 !
```

## Summary

## Create a new Unity project

To create a new project, [[open the Unity Hub]] and [[select "Project"]], from the left panel (should be selected by default).

![projects_button.png](./../../../../media/new_project/projects_button.png)

[[Select "New project"]] on the top-right corner.

![new_project_button.png](./../../../../media/new_project/new_project_button.png)

On the setting page, [[mind the steps]] :
1. Check the Unity version you are using (we recommend Unity **VAR_UNITY_MIN_VERSION** at least)
1. Select the "2D Core" project template
1. Fill the project name and location
1. Select your Unity account for "Unity Cloud Organization"
1. Click "Create project" !

![new_project_settings.png](./../../../../media/new_project/new_project_settings.png)

Well done ! The project is loading for the first time...

![new_project_init.png](./../../../../media/new_project/new_project_init.png)

Once loaded, the project will open. Congratulation, you now have a new Unity project set up !

![unity_layout.png](./../../../../media/new_project/unity_layout.png)


## Import RPG Power Forge

```admonish summary title=".unitypackage file"
RPG Power Forge is a Unity package ().unitypackage file. A Unity package contains features to fit the various needs of your Unity project. In the case of RPG Power Forge, the package provides many tools and features to make RPG games easily !
```

To import RPG Power Forge, [[choose Assets > Import Package > Custom Package]]. A file browser appears, prompting you to locate the .unitypackage file.

![import_package.png](./../../../../media/new_project/import_package.png)

In the file browser, [[select the RPG Power Forge Unity package file]] and click Open. Then, Unity will inform you the package you want to install will overwrite the current project setting : it's perfectly normal ! [[select "Import"]].

![import_warning.png](./../../../../media/new_project/import_warning.png)

A new window will display all the items to install. Make sure everything is selected (should be by default) and [[select "Import"]].

![import_list.png](./../../../../media/new_project/import_list.png)

RPG Power Forge package is now importing !

![import_loading.png](./../../../../media/new_project/import_loading.png)

RPG Power Forge will ask you if you are OK to install it. [[select "Install"]].

![import_restart.png](./../../../../media/new_project/import_restart.png)

RPG Power Forge package is installing ! Unity will restart upon completion.

![import_loading_2.png](./../../../../media/new_project/import_loading_2.png)

## Unity Editor recommendations

For an optimal gamedev experience (especially on laptops), we recommend the following settings for the Unity Editor :

 * Edit > Preferences > General > Interation Mode : **Monitor Refresh Rate**

![import_loading_2.png](./../../../media/new_project/unity_ref_settings.png)


## Congratulations

Well done, Unity Editor now has RPG Power Forge installed !

You can now [start making games here](../getting_started/lets_make_a_game.md) !
