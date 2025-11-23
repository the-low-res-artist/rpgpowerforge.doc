# Import Animations

This section covers the import of Animations with RPG Power Forge !

```admonish success title="Oh yeah"
This section is up-to-date !
```

## Summary

## Window location

```admonish example title="Window location"
Detailled location are in [Assets Importer page here](./assets_importer.md#feature-location).
```

## Window content
![import_animation_window.png](../../../../../../media/user_manual/assets_management/import_animation/import_animation_window.png)

Import option|Description|Supported formats
--------|--------|--------
Sprite Sheet|Import an image file made up of numerous smaller graphics ("sprites") that are grouped into a tiled grid formation.|.png .bmp .jpg .jpeg
Sprite Directory|Import a folder containing one or multiple sprites, each separated in its own image file|directory and sub-directories
Aseprite File| Import an Aseprite file that already contain animation information|.ase .aseprite

## Import procedure

### Sprite Sheet

Let's import this sample Sprite Sheet (a character walking in 4 directions) :

![import_animation_spritesheet.png](../../../../../../media/user_resources/import_animation_spritesheet.png)

```admonish tip title="User manual resources"
You can download all of our tutorial resources here : [download power_forge_resources.zip file](https://rpgpowerforge.com/media/power_forge_resources.zip)
```

#### Import the Sprite Sheet file
[[Select the "Sprite Sheet" button]] and choose the file to import in your file browser :

![import_animation_window_sprite_sheet.png](../../../../../../media/user_manual/assets_management/import_animation/import_animation_window_sprite_sheet.png)

#### Sprite Editor window
The Sprite Sheet is imported into our Sprite Editor :

![import_animation_general_view.png](../../../../../../media/user_manual/assets_management/import_animation/import_animation_general_view.png)


#### Slice the Sprite Sheet
A Sprite Sheet is usually composed of multiple Sprites arranged in a grid, like our current sample. We can slice the Sprite Sheet into individual Sprites with the Slice function :

Slice method|Description
--------|--------
Row & Column|Choose the number of [[rows]] and [[columns]] to Slice the Sprite Sheet into.
Pixel size|Choose the size (X for [[width]], Y for [[height]]) of the individual Sprite.

![import_animation_slice.gif](../../../../../../media/user_manual/assets_management/import_animation/import_animation_slice.gif)

#### Delete Sprites (optional)

It is possible to remove unnecessary Sprites (empty or not wanted). Deleted Sprites won't be imported in your RPG Power Forge project.

Delete method|Description
--------|--------
Automatic|[[Select the "Delete Empty Sprites" button]] to remove all of the empty Sprites at once. To undo, [[press CTRL + Z]].
Manual|[[Select the Sprite, right-click > Delete]]. Additionnally, you can select multiple Sprites with the SHIFT key. To undo, [[press CTRL + Z]].

![import_animation_general_view_delete_sprites.gif](../../../../../../media/user_manual/assets_management/import_animation/import_animation_general_view_delete_sprites.gif)

#### Transparency colors (optional)

You can define transparency colors for the Sprites. You can pick 2 different colors :

Transparency method|Description
--------|--------
Full Transparent Color| Useful if you want to remove a background color from your Sprite Sheet. The selected color will be completely transparent.
Semi Transparent Color| Useful for shadow, glass, tall-grass, etc. The selected color will be half-transparent.

In both cases, we recommend to use the **Color Picker** to select the desired color precisely :

![import_animation_transparency.gif](../../../../../../media/user_manual/assets_management/import_animation/import_animation_transparency.gif)


### Validate the Sprite Sheet

You are now ready to go ! [[Select the "Apply" button]] in the bottom-right corner to go to the Animation creation !

![import_animation_general_view_apply.png](../../../../../../media/user_manual/assets_management/import_animation/import_animation_general_view_apply.png)


### Sprites Directory (additional import method)

Instead of a Sprite Sheet, you can import a directory full of individual Sprites. Here is an example :

![import_animation_sprite_directory_hierarchy.png](../../../../../../media/user_manual/assets_management/import_animation/import_animation_sprite_directory_hierarchy.png)

```admonish tip title="User manual resources"
You can download all of our tutorial resources here : [download power_forge_resources.zip file](https://rpgpowerforge.com/media/power_forge_resources.zip)
```

When importing "import_sprites_directory", RPG Power Forge will automatically :
* Browse your directory and sub-directories.
* Find all of the Sprites (images files).
* Name each Sprite according to its location ("idle/up/0.png" will be named "IdleUp0")
* Import each Sprite in the Animation Collection (1 line per sub-directory).

Once Imported, [[Use the feature "Template > One Animation per line"]] to create all of your animations at once. More about [Animation creation here](./../collections/create_animations.md).

![import_animation_sprite_directory_process.gif](../../../../../../media/user_manual/assets_management/import_animation/import_animation_sprite_directory_process.gif)


### Aseprite File (additional import method)

It is possible to also import and Aseprite file (.aseprite or .ase). The animations will be extracted automatically and you will be redirected to the create Animations Collection window.


## Congratulation

You have successfully imported a Sprite Sheet, Slice it and make it a serie of Sprites. Well done ! You can now [create animations here](./../collections/create_animations.md).