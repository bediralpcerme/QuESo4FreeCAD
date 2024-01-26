# QuESo4FreeCAD

## Description

One of the most significant challenges among engineering softwares is interoperability of CAD (Computer Aided Design) and CAE (Computer Aided Engineering) tools. Efficient and advanced engineering workflow requires close collaboration between CAD environment and FE (Finite Element) software. Integrated applications not only reduce the requirement of model conversion but also improve development process by making it accessible and convenient.
QuESo4FreeCAD is a plug-in developed for the FreeCAD on the purpose enabling of direct structural analysis that provides a Graphical User Interface (GUI) to the open-source softwares [QuESo](https://github.com/manuelmessmer/QuESo) and [Kratos Multiphysics](https://github.com/KratosMultiphysics/Kratos) based on embedded FE model. The plug-in allows user to perform the fundamental tasks for a structural analysis that are:

- Preprocessing
- Solving Process
- Postprocessing

without dealing with time-consuming works such as engaging with system console, setting up JSON files manually, exporting the STL files and so on. The only thing user needs to do is deciding the preprocessing as well as solver parameters, and applying boundary conditions. The plug-in takes care of the rest of the required tasks, and enables user to analyze the results of different modes, for example von Mises Stress, Z Displacement, XY Cauchy Stress etc.
QuESo4FreeCAD plug-in is written completely in Python due to the its flexibility over C++, which is not so suitable for developing GUI [^1]. If you want to learn how to use QuESo4FreeCAD plug-in or want to know about the detailed steps of how it is implemented, please check out the Wiki. Also, please do not hesitate to contact us if you have any questions about QuESo4FreeCAD.

<figure>
  <img
  src="https://github.com/manuelmessmer/QuESo4FreeCAD/blob/1901d9c8e6378db91515e1c5b13110cee9d42196/docs/QuESo4FreeCAD_Interface_Windows.png"
  alt="Interface of QuESo4FreeCAD in Windows">
  <figcaption>
    text-align=center;
    Figure: Interface of QuESo4FreeCAD in Windows.
  </figcaption>
</figure>

## Required Softwares To Be Installed

As QuESo4FreeCAD is a plug-in for FreeCAD, please make sure that you have [FreeCAD](https://www.freecad.org/) installed on your computer. Besides, the repository of QuESo4FreeCAD does not include QuESo and Kratos Multiphysics softwares. Because of that, please refer to [QuESo](https://github.com/manuelmessmer/QuESo) and [Kratos Multiphysics](https://github.com/KratosMultiphysics/Kratos) for the compilation instructions.

Besides, please note that the plug-in does not ask the user which type of direct sparse solver to use, but by default, it makes use of "Pardiso Solver", which has a dependency on [Intel® MKL library](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html), due to its robustsness and efficiency compared to regular "Sparse Solver" [^2]. Because of that, installing and enabling Intel® MKL library is strongly recommended, as otherwise, you will need to change the solver type manually in one of the JSON files (for more information, please see the Wiki). For more information about how to install and enable Intel® MKL library, please refer to [this](https://github.com/KratosMultiphysics/Kratos/blob/master/applications/LinearSolversApplication/README.md) page of Kratos Multiphysics.

## Special Thanks To

- [Manuel Meßmer](https://github.com/manuelmessmer) for the supervision of the project

[^1]: https://wiki.freecad.org/Workbench_creation
[^2]: https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html
