# Blender Unity Settings for Voxel models.

A Blender add-on for Voxel 3D models.<br>
Description: streamlines optimising MagicaVoxel models to be used in Unity, can also create low level-of-detail version of models.<br>
> The default parameters that my team found fit Unity best will be included in the attached image.

# Dependencies

The add-on relies on two existing add-ons and won't work without having them installed in advance:
1. VoxCleaner v1 by Farhan Shaikh - [Github repo](https://github.com/TheStrokeForge/Vox-Cleaner).
2. Texel Density Checker v3.3.1 by Ivan Vostrikov - [Addon page](https://mrven.gumroad.com/l/CEIOR).

It could work with different versions, but these are the ones that were tested.<br>
> You can read how to install Blender add-ons [here](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html) or find another guide online.

# Installation

1. Install the dependencies.
2. Download `UnitySettings_1_1.py` and add it to Blender.

# Panels
<img align="right" src="https://github.com/ElenaChes/Node-Js-Express-MVC-Web-App/assets/54331769/12dcbccd-a079-4113-938f-9ded5fd425f5">

## Model Settings
- `Model` - will define the size of the texture map.
- `Island Margin` - used while packing islands.
- `Set TD` - parameter that Texel Density Checker needs to change TD.
- `New Model` - quickly import a new Obj and remove anything extra from the scene.

## Quick Export
- `Auto Export` (recommended) - whether processing will prompt to export the Texture and Obj(s) automatically. (couldn't get Blender to save without needing confirmation, might change in the future)
- `Texture Path` - location for the Texture to export to.
- `Flip Z axis` and `Scale` - will auto select these parameters when exporting.
- `Model Path` - location for the Obj to export to. (Will also be used for low LOD version if created)

Notes:
- If `Auto Export` is unselected, the "path" inputs will be replaced with manual `Export` buttons. Remember to export both the Texture and Obj after you're done processing!
- If a low LOD model was processed, the Obj panel will update to reflect that.

## Process Model
- `Use smart process` (recommended) - whether to condence all processing steps into a single button click.
- `Smart Process` - runs 7 steps to process the MagicaVoxel (or other voxel art) model and optimise it for using in Unity.

Notes:
- If `Use smart process` is unselected you will be able to go step by step:
  - `Start Process` - removes all objects except selected.
  - `Prepare For UV` - uses VoxCleaner's `Prepare For UV`.
  - `Pack Islands` - cubes projections and packs islands.
  - `Update TD` - uses Texel Density Checker's `Set My TD`.
  - `Set To Pixels` - snaps islands on Texture to fit pixels.
  - `Bake Texture` - uses VoxCleaner's `Bake Texture`.
  - `Pretty Polygons` - traingulates the polygons so they're more effecient in Unity.
> There is generally no real reason to go step by step here and it's best to `Smart Process` instead.

## Level Of Detail
- `Decimate` - how much to reduce the face count of the mesh.
- `Process` - decimates the model and creates a low level-of-detail model instead.

# Usage
 
1. Select the `Unity Settings` tab (press `N` if it's not open)
2. Verify that all the settings fit your preferences.
3. Click `New Model` and import the model you wish to process, select the model once it's in the scene.
4. Select `Auto Export` and select a path for the Texture & Obj.
6. Select `Use smart process` and click `Smart Process`.
7. Confirm saving in the window that opens.
8. If also creating a low LOD verision click `Process` in the `Level of Detail` panel and confirm saving as well.
> This is the recommended usage but you can choose to do the process manually if you wish to.

     
   
   
