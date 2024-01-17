# Blender Unity Settings for Voxel models

A Blender add-on for Voxel 3D models.<br>
Description: streamlines optimising MagicaVoxel models to be used in Unity, can also create low level-of-detail version of models.<br>

> [!NOTE]
> The default parameters that my team found fit Unity best will be included in the attached images.

<details>
  <summary><h3>Content</h3></summary>

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Panels](#panels)
  - [Model Settings](#model-settings)
  - [Quick Export](#quick-export)
  - [Process Model](#process-model)
  - [Level Of Detail](#level-of-detail)
- [Usage](#usage)

</details>
<hr>

# Dependencies

The add-on relies on two existing add-ons and won't work without having them installed in advance:

1. VoxCleaner v1 by Farhan Shaikh - [Github repo](https://github.com/TheStrokeForge/Vox-Cleaner).
2. Texel Density Checker v3.3.1 by Ivan Vostrikov - [Addon page](https://mrven.gumroad.com/l/CEIOR).

It could work with different versions, but these are the ones that were tested.<br>

> [!TIP]
> You can read how to install Blender add-ons [here](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html) or find another guide online.

# Installation

1. Install the dependencies.
2. Download `UnitySettings_1_1.py` and add it to Blender.

# Panels

## Model Settings

<img align="right" src="https://github.com/ElenaChes/Blender-Unity-Settings-Voxel-models/assets/54331769/820a5141-33e1-4148-b79d-6e7b5fb78f81">

- `Model` - will define the size of the texture map.
- `Island Margin` - used while packing islands.
- `Set TD` - parameter that Texel Density Checker needs to change TD.
- `New Model` - quickly import a new Obj and remove anything extra from the scene.

## Quick Export

<img align="right" src="https://github.com/ElenaChes/Blender-Unity-Settings-Voxel-models/assets/54331769/b09bf240-ab54-456c-a8d1-d6b3d0dbc64e">

<img align="right" src="https://github.com/ElenaChes/Blender-Unity-Settings-Voxel-models/assets/54331769/36854ccf-7124-4b45-a9e8-5c14a38c3a6a">

- `Auto Export` (recommended) - whether processing will prompt to export the Texture and Obj(s) automatically. (couldn't get Blender to save without needing confirmation, might change in the future)
- `Texture Path` - location for the Texture to export to.
- `Flip Z axis` and `Scale` - will auto select these parameters when exporting.
- `Model Path` - location for the Obj to export to. (Will also be used for low LOD version if created)

> [!CAUTION]
> If `Auto Export` is unselected, the "path" inputs will be replaced with manual `Export` buttons. Remember to export both the Texture and Obj after you're done processing!

<img align="right" src="https://github.com/ElenaChes/Blender-Unity-Settings-Voxel-models/assets/54331769/3fcddf60-f5f3-4735-8b52-6a4aeaefe7c6">
<img align="right" src="https://github.com/ElenaChes/Blender-Unity-Settings-Voxel-models/assets/54331769/292dde53-5991-48d8-a19b-88d69fed1281">

> [!NOTE]
> If a low LOD model was processed, the Obj panel will update to reflect that.

## Process Model

<img align="right" src="https://github.com/ElenaChes/Blender-Unity-Settings-Voxel-models/assets/54331769/fb80080e-cd9c-4a2b-a0f1-3e094c6ae97f">

<img align="right" src="https://github.com/ElenaChes/Blender-Unity-Settings-Voxel-models/assets/54331769/fd19a843-5893-4632-8141-2cdb0f94247b">

- `Use smart process` (recommended) - whether to condence all processing steps into a single button click.
- `Smart Process` - runs 7 steps to process the MagicaVoxel (or other voxel art) model and optimise it for using in Unity.

> [!NOTE]
> If `Use smart process` is unselected you will be able to go step by step:
>
> - `Start Process` - removes all objects except selected.
> - `Prepare For UV` - uses VoxCleaner's `Prepare For UV`.
> - `Pack Islands` - cubes projections and packs islands.
> - `Update TD` - uses Texel Density Checker's `Set My TD`.
> - `Set To Pixels` - snaps islands on Texture to fit pixels.
> - `Bake Texture` - uses VoxCleaner's `Bake Texture`.
> - `Pretty Polygons` - traingulates the polygons so they're more effecient in Unity.

> [!TIP]
> There is generally no reason in regular usage to go step by step here and it's best to `Smart Process` instead.

## Level Of Detail

<img align="right" src="https://github.com/ElenaChes/Blender-Unity-Settings-Voxel-models/assets/54331769/5a30fd66-e722-4f7c-a1e1-63fc2ae8babe">

- `Decimate` - how much to reduce the face count of the mesh.
- `Process` - decimates the model and creates a low level-of-detail model instead.

> [!IMPORTANT]
> In order to create a low LOD version you need to process the model first.

# Usage

1. Select the `Unity Settings` tab (press `N` if it's not open)
2. Verify that all the settings fit your preferences.
3. Click `New Model` and import the model you wish to process, select the model once it's in the scene.
4. Select `Auto Export` and select a path for the Texture & Obj.
5. Select `Use smart process` and click `Smart Process`.
6. Confirm saving in the window that opens.
7. If also creating a low LOD verision click `Process` in the `Level of Detail` panel and confirm saving as well.

> [!NOTE]
> This is the recommended usage but you can choose to do the process manually if you wish to.
