import sympy as sp
import sympy.physics.mechanics as me
import numpy as np
import scipy
from sympy import Dummy


#Parameter Configuration:
n = 2                                                         #Number of Masses
b = 0.3                                                       #Air Resistance
theta = 120                                                   #Initial Angle (0-360)
omega = 0                                                     #Initial Angular Velocity
gravity = 5                                                   #Gravity



#Create Constants
m = sp.symbols('m:{0}'.format(n))                             #Masses
l = sp.symbols('l:{0}'.format(n))                             #Lengths
g = sp.symbols('g')                                           #Gravity

#Introduce Generalized Coordinates                  
q = me.dynamicsymbols('q:{0}'.format(n))                      #Generalized Coordinates in Configuration Space
qd = me.dynamicsymbols('q:{0}'.format(n), level = 1)          #Vector of the Time Derivatives of the Generalized Coordinates 
u = me.dynamicsymbols('u:{0}'.format(n))                      #Generalized Speeds in Configuration Space
                        
N = me.ReferenceFrame('N')                                    #Inertial Reference Frame
O = me.Point('O')                                             #Coordinate Location of Origin
O.set_vel(N, 0)                                               #Sets the Velocity Vector of Point 'O' Relative to Frame 'N'

#Kanes Method
def get_equations():
    
    ref_frames, kde, particle_locs, particles, gravities, forces, drags = ([] for i in range(7))

    for i in range(n):
        
        #Create Particle Objects
        if i == 0:
            ref_frames.append(N.orientnew('mass_ref_frame{0}'.format(i), 'Axis', (q[i], N.z)))
            particle_loc = O.locatenew('P{0}'.format(i), (-l[i] * ref_frames[i].y))
            particle_object = me.Particle('p{0}'.format(i), particle_loc, m[i])
        else:
            ref_frames.append(ref_frames[i-1].orientnew('mass_ref_frame{0}'.format(i), 'Axis', (q[i], N.z)))
            particle_loc = particle_locs[i-1].locatenew('P{0}'.format(i), (-l[i] * ref_frames[i].y))
            particle_object = me.Particle('p'.format(i), particle_loc, m[i])
        particle_locs.append(particle_loc)
        particles.append(particle_object)
        
        #Create Kinetic Differential Equations
        for j in range(i):                
            qd[0] += qd[j+1]
        kde.append(u[i]- qd[0])
        
        #Add Action Forces
        drags.append(-b*u[i]*N.y - b*u[i]*N.x - b*u[i]*N.z)
        gravities.append(-g*m[i]*N.y)
        forces.append((particle_locs[i], gravities[i] + drags[i]))
           
    #Calculate Fr + Fr* = 0
    KM = me.KanesMethod(N, q, u, kd_eqs=kde) # Kane's method instance
    fr, fstar = KM.kanes_equations(particles, forces) # "Evaluate the sum"

    return(KM,-fstar,fr)


#Symbolic to Numerical and Integrate
def numerical_integration(KM, fstar, fr, times, lengths = None, masses = 1):
    
    
    y0 = np.deg2rad(np.concatenate([np.broadcast_to(theta, n),
                                    np.broadcast_to(omega, n)]))

    
    if lengths is None:
        lengths = np.ones(n) / n
    lengths = np.broadcast_to(lengths, n)
    masses = np.broadcast_to(masses, n)
    
        
    parameters = [g] + list(l) + list(m)
    parameter_vals = [gravity] + list(lengths) + list(masses)    
    
    unknowns = [Dummy() for i in q + u]
    unknown_dict = dict(zip(q + u, unknowns))
    kds = KM.kindiffdict()
    
    mm_sym = KM.mass_matrix_full.subs(kds).subs(unknown_dict)
    fo_sym = KM.forcing_full.subs(kds).subs(unknown_dict)
    
    mm_func = sp.lambdify(unknowns + parameters, mm_sym)
    fo_func = sp.lambdify(unknowns + parameters, fo_sym)
    
    def gradient(y, t, args):
        vals = np.concatenate((y, args))
        sol = np.linalg.solve(mm_func(*vals), fo_func(*vals))
        return np.array(sol).T[0]
    
    return scipy.integrate.odeint(gradient, y0, times, args=(parameter_vals,))


#Convert Generalized Coordinates to Cartesian Coordinates
def get_xy_coords(integrated_func, lengths=None):
    """Get (x, y) coordinates from generalized coordinates p"""
    integrated_func = np.atleast_2d(integrated_func)
    n = integrated_func.shape[1] // 2
    if lengths is None:
        lengths = np.ones(n) / n
    zeros = np.zeros(integrated_func.shape[0])[:, None]
    x = np.hstack([zeros, lengths * np.sin(integrated_func[:, :n])])
    y = np.hstack([zeros, -lengths * np.cos(integrated_func[:, :n])])
    return np.cumsum(x, 1), np.cumsum(y, 1)


t = np.arange(0, 10+0.006944444444, 0.006944444444)

KM,EOM_i,EOM_f = get_equations()
integrated_func = numerical_integration(KM,EOM_i,EOM_f,t)
x, y = get_xy_coords(integrated_func)
