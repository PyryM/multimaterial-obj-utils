# multimaterial-obj-utils

A number of tools (Autdesk 123d catch / remake / recap) like to produce .obj meshes where different faces use 
different materials, in order to split large textures among multiple texture maps. This often causes problems with obj loaders,
for example when trying to use such meshes with three.js or aframe.io.

This is a set of utilities to turn such meshes into simple single-material meshes.

## Tools

### splitobj.py
This script splits an obj into separate objs, one for each material used in the source.

Usage: `python splitobj.py src.obj dest_prefix`

If the materials are named e.g., "glass" and "stone", it will produce files "dest_prefix_glass.obj" and "dest_prefix_stone.obj".
It does not modify the .mtl files at all, so all the resulting meshes will share the original .mtls.
