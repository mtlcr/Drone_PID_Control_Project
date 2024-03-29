
from DroneListener import DroneListener
import matplotlib.pyplot as plt
from tkinter import *  
from PIL import ImageTk, Image  
import time
import math

class TKinterVisualizer(DroneListener):
        
    def initialize(self, target_elevation, target_x, simulation_length, path:list() = []):
        self.root = Tk()  
        self.root.geometry("+0+0")
        self.canvas = Canvas(self.root, bg="green", width = 800, height = 500)  
        self.canvas.pack()
        self.bg_img = Image.open("Forest_with_mountains2.jpg") #"../images/blurry_trees_bg2.gif")
        self.tk_bg_img = ImageTk.PhotoImage(self.bg_img)
        
        # The following line sometimes gives an error in IPython console.
        # It happens if there was a previous run that resulted in an error and
        # caused some lingering reference that is invalid. The solution is to 
        # fix whatever was causing the error in the previous run, then restart the
        # kernel before running again.
        self.background = self.canvas.create_image(0, 0, anchor=NW, image=self.tk_bg_img) 
        self.text = StringVar()
        self.text.set('Keep Window Open...')

        self.button = Button(self.root,
                            textvariable=self.text,
                            command = self.wait_for_user)
        self.button.pack()
        self.button.place(x=350, y=100)
        self.button["state"] = "disabled"
        self.wait = False
        
        counter = 0 
        
        
        self.drone_info = StringVar()
        self.label = Label(self.root, 
                           fg="black", 
                           #bg="gray",
                           justify = "left",
                           borderwidth=2, 
                           relief="groove",
                           textvariable=self.drone_info)
        self.label.pack()
        self.label.place(x=600, y=100)
                
        if len(path) > 0:
            prev_y = 490-path[0][1]*10
            prev_x = 100+path[0][0]*10
            
            for i in range(1,len(path)):
                y = 490-path[i][1]*10
                x = 100+path[i][0]*10
                
                height = (y - prev_y)
                y1 = prev_y
                
                start_x_pad = 0
                end_x_pad = 0
                if height < 0: 
                    y1 = y
                    height = abs(height)
                    end_x_pad = 30
                elif height > 0:
                    start_x_pad = -30

                
                width = (x - prev_x)
                
                self.rect = self.canvas.create_rectangle(
                                        prev_x + start_x_pad, 
                                        y1, 
                                        prev_x + width + end_x_pad,
                                        y1 + height + 30, 
                                        width=1,
                                        fill='brown',
                                        outline='saddle brown')
                
                prev_y = y
                prev_x = x
        
        self.time_step = 0
    
    def update(self, x, y, roll_angle, thrust, roll, rpm_left, rpm_right, pid_params):
        self.time_step += 1     
        img = Image.open("dualrotor4.png")
        self.tkimage = ImageTk.PhotoImage(img.rotate(max(min(roll_angle*10*180/math.pi,89/math.pi),-89/math.pi)))
        self.canvas.create_image(100+x*10, 500-y*10, anchor=S, image=self.tkimage) 
        #canvas.move(drone, x, y)
        
        t_p = round(pid_params['pid_thrust']['tau_p'],2)
        t_d = round(pid_params['pid_thrust']['tau_d'],2)
        t_i = round(pid_params['pid_thrust']['tau_i'],4)
        t_params = "P:{}, D:{}, I:{}".format(t_p, t_d, t_i) 
        r_p = round(pid_params['pid_roll']['tau_p'],2)
        r_d = round(pid_params['pid_roll']['tau_d'],2)
        r_i = round(pid_params['pid_roll']['tau_i'],4)
        r_params = "P:{}, D:{}, I:{}".format(r_p, r_d, r_i)
        
        
        self.drone_info.set("Time Step: {} \nThrust: {} \nRoll: {} \nLeft RPM: {} \nRight RPM: {} \nPID Thrust: {} \nPID Roll: {}".format(
                                self.time_step,
                                round(thrust,2), 
                                round(roll_angle,2), 
                                round(rpm_left,2), 
                                round(rpm_right,2),
                                t_params,
                                r_params)
                            )
        
        self.root.update()
        if self.time_step % 100 == 0:
            self.root.after(1)
        
    
    def wait_for_user(self):
        self.wait = True
        self.text.set('Use the X button on top to close this Window')
        
    def destroy(self):
        if not self.wait:
            self.root.destroy()
    
    def end_simulation(self, args: dict = dict()):
        self.button["state"] = "normal"
        self.root.update()
        self.root.after(2000, self.destroy)
        
        self.root.mainloop()
        
        
        
    
    



