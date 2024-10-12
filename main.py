from manim import *
from scipy.integrate import solve_ivp
import numpy as np

class BungeeJump(Scene):
    def construct(self):
        
        # numerical integration args
        time_range      = [0,50]   # s 
        height_start    = 80       # mass
        velocity_start  = 0        # ms^-1

        # constants for ODE
        g = -9.81   # gravity on earth  / ms^-2 
        k = 50      # spring constant   / Nm^-1
        l = 30      # length of bungee  / m
        mass = 80   # mass of person    / kg
        step = 0.05


        def bungee_step(t,values) -> list :
            """bungee_step 

            Paramaters
            ----------
            t : float
                for time dependent ODE's
            values : list
                contains the variables in the ODE systemass 

            Returns
            -------
            list
                contains the time derivatives respective to how they were passed into the function
            """
            y,v = values
            
            dydt = v
            
            # it doesn't make sense to calculate drag if the person is on the floor
            # while the rope reverbs. (super super rough ground collision implementation)
            if y == 0 or y < 0 :                
                dvdt = g + k*(height_start-y-l)/mass                                                             
                
            # maintain a sign of velocity for the sake of direction,    
            # it always opposes direction of travel.
            elif y < height_start - l :                                                                    
                dvdt = g + k*(height_start-y-l)/mass + (-v-abs(v)*v)/mass                                      

            # this is before the rope has begun to stretch, so no hookes law.
            else :                                                                                  
                dvdt = g + (-v-abs(v)*v)/mass                                                        
            
            return [dydt,dvdt]

        solution = solve_ivp(bungee_step, time_range, [height_start, velocity_start], max_step = step)

        times            = solution.t
        height,velocity  = solution.y
    
        # Latex
        equations = MathTex(r"""\\
            \frac{dy}{dt}&=v    \\
            \frac{d\vec{v}}{dt}&=\vec{g}+\frac{k\cdot(80-y_i-l)}{m}+\frac{(-\vec{v_i}-|\vec{v_i}|\vec{v_i})}{m}
            """,font_size=30)
    
        # Axes
        axes = Axes(
            x_range=(0,50,5),
            y_range=(0,100,10),
            x_length=10,
            y_length=6.5,
        )
        axes.add_coordinates()
        x_label = axes.get_x_axis_label('Time (s)')
        y_label = axes.get_y_axis_label('Height (m)')
        
        # Graphs
        graph_position = axes.plot_line_graph(times,height,add_vertex_dots=False,line_color=BLUE)
        graph_velocity = axes.plot_line_graph(times,velocity,add_vertex_dots=False,line_color=RED)
        
        # Drawing 
        self.add(axes,x_label,y_label)
        
        equations.to_corner(UR)
        self.add(equations)
        
        self.play(Write(graph_position),run_time=50)