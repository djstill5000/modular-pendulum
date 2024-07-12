# Modular-Pendulum

Python script used to create n-body pendulum simulations in any media format supported by the Manim library (mp4, gif, etc).
The equations of motions are found using Kane's method via the Sympy library. The Integration is done using Scipy and the animation is done in ManimCE.

![Animate_ManimCE_v0 17 2](https://github.com/user-attachments/assets/05f2abfe-c85d-4807-9fd6-9041225e8847)

## Installation

All of the dependencies are provided in a conda environment, ensure that you have the conda-forge channel enabled, and conda channel_priority set to flexible
before trying to install the environment or it may not generate correctly. You may also have to the libmamba solver enabled in your conda config.

```
conda env create -f environment.yml
```

## Usage

Run the Conda Environment:

```
conda activate modp
```

In `config.ini` you can find the customizable parameters.

To generate the animation exectute the following in the `modp` conda environment:

```
manim Animate.py Animate
```

By default, manim generates an mp4 at 1080p at 60fps, if you want to change this you can add parameters to the previous command, See the [ManimCE API](https://docs.manim.community/en/stable/guides/configuration.html) for more details.

## References and Further Reading

[1] *T. Kane  and D.  Levinson. (1985). "Dynamics, theory  and applications."*

[2] *Hussain, Zakia & Azlan, Norsinnira. (2016). "KANE's method for dynamic modeling."*

[3] *Stoneking. Eric. (2013). "Implementation of Kane's Method for a spacecraft Composed of Multiple Rigid Bodies."*

[4] *Charles. S. (2019). "The Lagrangian Mechanics and Pseudo-Periodicity of The Many-Body Planar Pendulum System."*
