from manim import *
import numpy as np

class ProjectilePhysics(): 
    def __init__(self, u:float, theta_deg: float, h0:float = 0.0, g:float=10):
        self.u= u
        self.theta = np.radians(theta_deg)
        self.h0 = h0
        self.g = g
        
        self.vx = self.u*np.cos(self.theta)
        self.vy = self.u*np.sin(self.theta)
        
        discriminant = self.vy**2 + (2 * self.g * self.h0)
        self.t_flight = (self.vy + np.sqrt(discriminant)) / self.g
        self.max_height = self.h0 + (self.vy**2) / (2 * self.g)
        self.range = self.vx * self.t_flight
        
    def get_t_flight(self):
        return self.t_flight
    
    def get_max_height(self):
        return self.max_height
    
    def get_range(self):
        return self.range
        
    def get_pos(self, t):
        """Returns (x, y) coordinates at time t."""
        sx = self.vx*t 
        sy = self.vy - 0.5*self.g*t**2
        return np.array([sx, sy, 0])
        
    def get_velocity(self, t):
        """Returns [vx, vy, 0] velocity components at time t."""
        vx= self.vx
        vy = self.vy - self.g*t
        return np.array([vx, vy, 0])
    
    
    
def dynamic_arrow(start, vector, color, scale, buff=0):
    end= start+vector*scale
    return Arrow(start=start, end=end, color=color, buff=buff)
 
 
class ProjectLessons(VMobject):
    def __init__(self, physics: ProjectilePhysics, axes: Axes, time_tracker: ValueTracker):
        super().__init__()
        self.physics = physics
        self.time_tracker = time_tracker
        self.axes = axes
        
        
        self.v_arrow= always_redraw(
            lambda: Arrow(
                start=self.get_origin_point(), end=self.axes.c2p(*(self.physics.get_pos(self.get_t()) + 
                        self.physics.get_velocity(self.get_t()))), 
                         buff=0, color=GREEN_C, stroke_width=4
                ))
        
        self.vx_arrow = always_redraw(lambda: Arrow(
            start=self.get_origin_point(),
            end=self.axes.c2p(*(self.physics.get_pos(self.get_t()) + 
                                np.array([self.physics.vx, 0, 0]) )),
            buff=0, color=BLUE_C, stroke_width=3
        ))
        
        self.vy_arrow = always_redraw(lambda: Arrow(
            start=self.get_origin_point(),
            end=self.axes.c2p(*(self.physics.get_pos(self.get_t()) + 
                                np.array([0, self.physics.get_velocity(self.get_t())[1], 0]) )),
            buff=0, color=RED_C, stroke_width=3
        ))
        
        
        self.add(self.v_arrow, self.vx_arrow, self.vy_arrow)

        
    
    
    def get_t(self):
        return self.time_tracker.get_value()
        
    
    def get_origin_point(self):
        return  self.axes.c2p(*self.physics.get_pos(self.get_t()))
       

  
 
 
class ProjectileIntro(Scene):
    def construct(self):
        physics = ProjectilePhysics(u=30, theta_deg=30)
    
        ax = Axes(
        x_range=[0, physics.get_range()+2, 5],
        y_range=[0, physics.get_max_height()+2, 2],
        x_length=15, 
        y_length=9,
        axis_config={"include_numbers": True}
        ).scale(0.5)
    
        labels = ax.get_axis_labels(x_label="x/m", y_label="h/m")
        self.add(ax, labels)
        
        flight_path = ax.plot_parametric_curve(
            lambda t: physics.get_pos(t),
            t_range=[0, physics.t_flight],
            color=GRAY_C, stroke_opacity=0.4
        )
        self.add(flight_path)
        
        time_clock = ValueTracker(0)
        projectile_dot = Dot(color=YELLOW_C, radius=0.12)
        projectile_dot.add_updater(lambda m: m.move_to(ax.c2p(*physics.get_pos(time_clock.get_value()))))
        
        arrows= ProjectLessons( physics, ax, time_clock)
        self.add(projectile_dot)
        
        
        t_pause = 0.8
        self.play(
            time_clock.animate.set_value(t_pause),
            run_time=2.0,
            rate_func=linear
        )
        self.wait(0.5)
    

