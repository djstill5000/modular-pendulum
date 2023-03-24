# Kane Pendulum

Creates animated pendulums!

The equations of motions are found using Kane's method via the Sympy library. The Integration is done using Scipy and the animation is done in ManimCE.

## Installation

All of the dependencies are provided in a conda environment:

```
conda env create -f environment.yml
```


## Usage

Run the Conda Environment:

```
conda activate kane-p
```

In `Kane-Integrate.py` you can find the customizable parameters.

To generate the animation exectute the following in the conda environment:

```
manim Animate.py Animate
```

By default, manim generates an mp4 at 1080p at 60fps, if you want to change this you can add parameters to the previous command, See the [ManimCE API](https://docs.manim.community/en/stable/guides/configuration.html) for more details.

## References and Further Reading

[1] T. Kane  and D.  Levinson, Dynamics, theory  and applications. New York: McGraw-Hill, 1985. 

[2] Hussain, Zakia & Azlan, Norsinnira. (2016). KANE's method for dynamic modeling. 174-179. 10.1109/I2CACIS.2016.7885310.

[3] Stoneking. Eric, "Implementation of Kane's Method for a spacecraft Composed of Multiple Rigid Bodies", AIAA-2013-4649

[4] Charles. S, "The Lagrangian Mechanics and Pseudo-Periodicity of The Many-Body Planar Pendulum System", doi:  
10.48550/arXiv.1911.04364
