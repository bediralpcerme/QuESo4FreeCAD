# QuESo4FreeCAD

One of the most significant challenges among engineering softwares is interoperability of CAD (Computer Aided Design) and CAE (Computer Aided Engineering) tools. Efficient and advanced engineering workflow requires close collaboration between CAD environment and FE (Finite Element) software. Integrated applications not only reduce the requirement of model conversion but also improve development process by making it accessible and convenient.
QuESo4FreeCAD is a plug-in developed for the FreeCAD on the purpose enabling of direct structural analysis that provides a Graphical User Interface (GUI) to the open-source softwares [QuESo](https://github.com/manuelmessmer/QuESo) and [Kratos Multiphysics](https://github.com/KratosMultiphysics/Kratos) based on embedded FE model. The plug-in allows user to perform the fundamental tasks for a structural analysis that are:

- Preprocessing
- Solving Process
- Postprocessing

without dealing with time-consuming works such as engaging with system console, setting up JSON files manually, exporting the STL files and so on. The only thing user needs to do is deciding the preprocessing as well as solver parameters, and applying boundary conditions. The plug-in takes care of the rest of the required tasks, and enables user to analyze the results of different modes, for example von Mises Stress, Z Displacement, XY Cauchy Stress etc.
QuESo4FreeCAD plug-in is written completely in Python due to the its flexibility over C++, which is not so suitable for developing GUI [^1]. If you want to learn how to use QuESo4FreeCAD plug-in or want to know about the detailed steps of how it is implemented, please check out the Wiki. Also, please do not hesitate to contact us if you have any questions about QuESo4FreeCAD.

<p align="center">
<img src="docs/QuESo4FreeCAD_Interface_Windows.png">
<figcaption> <strong>Fig. 1</strong>: Interface of QuESo4FreeCAD in Windows.</figcaption>
</p>

## Special Thanks To

- [Manuel Meßmer](https://github.com/manuelmessmer) for the supervision of the project

[^1]: https://wiki.freecad.org/Workbench_creation
