# Install Unity

This section covers the download and installation process for Unity Hub and Unity Editor.

```admonish success title="Oh yeah"
This section is up-to-date with Unity 6000.0 !
```

## Summary

## Recommendations
Software | Version |
--- | --- 
Unity Hub | at least **VAR_UNITY_HUB_MIN_VERSION**
Unity Editor | at least **VAR_UNITY_MIN_VERSION**

```admonish warning title="Follow the above recommendations"
RPG Power Forge is designed to run with Unity version **VAR_UNITY_MIN_VERSION** and above. This is due to Unity fixing bugs and limitations we've raised during RPG Power Forge development. Do not use an older Unity version.
```

## Install Unity Hub

```admonish summary title="Unity Hub"
The Unity Hub is a standalone application that streamlines the way you find, download, and manage your Unity Projects and installations.
```

[[Go to the Unity website]] : [unity.com/download](https://unity.com/download). This page will ask you to download the Unity Hub.

Once installed on your computer, [[launch it]]. The Unity Hub version is diplayed in the top-left window corner :

![unity_hub_version.png](./../../../../media/download/unity_hub_version.png)

## Install Unity Editor

With the Unity Hub installed and opened, [[select "Installs"]] :

![install_button.png](./../../../../media/download/install_button.png)

Then [[select "Install Editor"]] :

![install_editor_button.png](./../../../../media/download/install_editor_button.png)

[[Select Unity VAR_UNITY_SHORT_MIN_VERSION]] (recommended version) :

![install_unity_version.png](./../../../../media/download/install_unity_version.png)


### Additional Unity packages

For a greater experience, we recommend to also select the following packages when installing Unity.

```admonish question title="What if I don't want to install additionnal things now ?"
You can also skip this section and install packages later on. [[Jump to]] [Start the Unity installation](#start-the-unity-installation) !
```

#### WebGL Build Support (optional)

This package allows Unity to build WebGL projects, which is used to publish games on itch.io. [[Select the package "WebGL Build Support"]] :

![install_webgl.png](./../../../../media/download/install_webgl.png)

#### Visual Studio Community (optional)

Visual Studio Community Edition serves as an integrated development environment (IDE) for writing and editing code when working on Unity projects. [[Select the package "Microsoft Visual Studio Community"]] :

![install_webgl.png](./../../../media/download/install_visual_studio.png)

### Start the Unity installation

Once you have chosen your packages, [[select "Install"]] :

![install_progress.png](./../../../../media/download/install_unity_with_packages.png)

You can now see the download and installation progress in the Unity Hub left panel.

![install_progress.png](./../../../../media/download/install_progress.png)

## Congratulations

You have the Unity Editor installed on your computer ! You can now [download RPG Power Forge here](./download_rpg_power_forge.md).