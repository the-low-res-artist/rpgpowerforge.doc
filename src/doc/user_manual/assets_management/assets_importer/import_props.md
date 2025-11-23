# Import Props

This section covers the import of Props with RPG Power Forge !

```admonish success title="Oh yeah"
This section is up-to-date !
```

## Summary

## Window content

![import_props_window.png](../../../../../../media/user_manual/assets_management/import_props/import_props_window.png)

Import option|Description|Supported formats
--------|--------|--------
Sprite Sheet|Import an image file made up of numerous smaller graphics ("sprites") that are grouped into a tiled grid formation.|.png .bmp .jpg .jpeg
Sprite Directory|Import a folder containing one or multiple sprites, each separated in its own image file|directory and sub-directories

## Import procedure

### Sprite Sheet

Let's import this sample sprite sheet (an animated fire camp with a few trees and bushes) :

![import_props_spritesheet.png](../../../../../../media/user_resources/import_props_spritesheet.png)

```admonish tip title="User manual resources : import_props_spritesheet.png"
You can download all of our tutorial resources here : [download power_forge_resources.zip file](https://rpgpowerforge.com/media/power_forge_resources.zip)
```


#### Import the Sprite Sheet file
[[Select the "Sprite Sheet" button]] and choose the file to import in your file browser :

![import_props_window_spritesheet.png](../../../../../../media/user_manual/assets_management/import_props/import_props_window_spritesheet.png)

#### Sprite Editor window
The Sprite Sheet is imported into our Sprite Editor :

![import_props_general_view.png](../../../../../../media/user_manual/assets_management/import_props/import_props_general_view.png)


#### Slice the Sprite Sheet
A Sprite Sheet is usually composed of multiple Sprites arranged in a grid, like our current sample. We can slice the Sprite Sheet into individual Sprites with the Slice function :

Slice method|Description
--------|--------
Row & Column|Choose the number of [[rows]] and [[columns]] to Slice the Sprite Sheet into.
Pixel size|Choose the size (X for [[width]], Y for [[height]]) of the individual Sprite.

![import_props_slice.gif](../../../../../../media/user_manual/assets_management/import_props/import_props_slice.gif)

#### Merge Sprites (optional)

It is possible to merge Sprites together, especially if the Props is bigger than the Sprite size.

Merge method|Description
--------|--------
Manual|[[Select multiple Sprites with the SHIFT key, right-click > Merge]]. To undo, [[press CTRL + Z]].

![import_props_merge.gif](../../../../../../media/user_manual/assets_management/import_props/import_props_merge.gif)

#### Delete Sprites (optional)

It is possible to remove unnecessary Sprites (empty or not wanted). Deleted Sprites won't be imported in your RPG Power Forge project.

Delete method|Description
--------|--------
Automatic|[[Select the "Delete Empty Sprites" button]] to remove all of the empty Sprites at once. To undo, [[press CTRL + Z]].
Manual|[[Select the Sprite, right-click > Delete]]. Additionnally, you can select multiple Sprites with the SHIFT key. To undo, [[press CTRL + Z]].

![import_props_delete.gif](../../../../../media/user_manual/assets_management/import_props/import_props_delete.gif)

#### Transparency colors (optional)

You can define transparency colors for the Sprites. You can pick 2 different colors :

Transparency method|Description
--------|--------
Full Transparent Color| Useful if you want to remove a background color from your Sprite Sheet. The selected color will be completely transparent.
Semi Transparent Color| Useful for shadow, glass, tall-grass, etc. The selected color will be half-transparent.

In both cases, we recommend to use the **Color Picker** to select the desired color precisely. You can find [an example here](./import_animations.md).

### Validate the Sprite Sheet

You are now ready to go ! [[Select the "Apply" button]] in the bottom-right corner to go to the Props edition !


### Sprites Directory (additional import method)

Instead of a Sprite Sheet, you can import a directory full of individual Sprite files. Please refer to [this example here](./import_animations.md).


## Congratulation

You have successfully imported a Sprite Sheet, Slice it and make it a serie of Sprites. Well done ! You can now [create animations here](./../collections/create_animations.md).