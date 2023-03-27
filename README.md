# Modular-Pendulum

![Animate_ManimCE_v0 17 2](https://user-images.githubusercontent.com/89823585/227702606-5c100396-460c-40bd-b2d8-01b59b26dc19.gif)

The equations of motions are found using Kane's method via the Sympy library. The Integration is done using Scipy and the animation is done in ManimCE.

## Installation

All of the dependencies are provided in a conda environment:

```
conda env create -f environment.yml
```


## Usage

Run the Conda Environment:

```
conda activate modp
```

In `config.ini` you can find the customizable parameters.

To generate the animation exectute the following in the conda environment:

```
manim Animate.py Animate
```

By default, manim generates an mp4 at 1080p at 60fps, if you want to change this you can add parameters to the previous command, See the [ManimCE API](https://docs.manim.community/en/stable/guides/configuration.html) for more details.

## References and Further Reading

[1] *T. Kane  and D.  Levinson. (1985). "Dynamics, theory  and applications."*

[2] *Hussain, Zakia & Azlan, Norsinnira. (2016). "KANE's method for dynamic modeling."*

[3] *Stoneking. Eric. (2013). "Implementation of Kane's Method for a spacecraft Composed of Multiple Rigid Bodies."*

[4] *Charles. S. (2019). "The Lagrangian Mechanics and Pseudo-Periodicity of The Many-Body Planar Pendulum System."*
