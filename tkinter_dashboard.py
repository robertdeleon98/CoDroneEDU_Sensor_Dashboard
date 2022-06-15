import datetime as dt
import sys
import tkinter as tk
from tkinter import ttk
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from codrone_edu.drone import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data_list = [0] * 11

drone = Drone()
drone.pair()


class DroneDashboard:
    def __init__(self):
        self.temperature = data_list[0]
        self.battery = data_list[1]
        self.pressure = data_list[2]
        self.rollAngle = data_list[3]
        self.yawAngle = data_list[4]
        self.pitchAngle = data_list[5]
        self.accX = data_list[6]
        self.accY = data_list[7]
        self.accZ = data_list[8]
        self.frontRange = data_list[9]
        self.bottomRange = data_list[10]

        self.max_elements = 20

    def run(self):
        # === tkinter interface ===
        # create main window
        self.root = tk.Tk()
        self.root.title("CDE Sensor Dashboard")
        self.root.state('zoomed')

        # create main container
        self.mainframe = ttk.Frame(self.root, padding="5 5 5 50")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # styling configs
        ttk.Style().configure("TLabel", font=('Helvetica', 14))
        ttk.Style().configure("title.TLabel", font=('Helvetica', 18))

        # Create figures for plotting
        self.fig_temp = plt.figure()  # temperature
        self.ax_temp = self.fig_temp.add_subplot(1, 1, 1)
        self.fig_pres = plt.figure()  # pressure
        self.ax_pres = self.fig_pres.add_subplot(1, 1, 1)
        self.fig_batt = plt.figure()  # battery
        self.ax_batt = self.fig_batt.add_subplot(1, 1, 1)
        self.fig_angles = plt.figure()  # angles
        self.ax_angles = plt.axes(projection='3d')

        # Empty lists for storing sensor data to plot later
        xs1 = []
        xs2 = []
        xs3 = []
        temp = []
        pres = []
        batt = []

        self.start = [0, 0, 0]

        # Create a Tk Canvas widget out of our matplotlib figures
        canvas_temp = FigureCanvasTkAgg(self.fig_temp, master=self.mainframe)
        canvas_temp_plot = canvas_temp.get_tk_widget()
        canvas_temp_plot.grid(row=1, column=0, rowspan=3, columnspan=4, sticky=tk.W + tk.E + tk.N + tk.S)

        canvas_pres = FigureCanvasTkAgg(self.fig_pres, master=self.mainframe)
        canvas_pres_plot = canvas_pres.get_tk_widget()
        canvas_pres_plot.grid(row=1, column=4, rowspan=3, columnspan=4, sticky=tk.W + tk.E + tk.N + tk.S)

        canvas_batt = FigureCanvasTkAgg(self.fig_batt, master=self.mainframe)
        canvas_batt_plot = canvas_batt.get_tk_widget()
        canvas_batt_plot.grid(row=5, column=0, rowspan=3, columnspan=4, sticky=tk.W + tk.E + tk.N + tk.S)

        canvas_angle = FigureCanvasTkAgg(self.fig_angles, master=self.mainframe)
        canvas_angle_plot = canvas_angle.get_tk_widget()
        canvas_angle_plot.grid(row=5, column=4, rowspan=3, columnspan=4, sticky=tk.W + tk.E + tk.N + tk.S)

        # add tkinter widgets to display sensor values as text
        self.temp_label = ttk.Label(self.mainframe, text="Temperature:").grid(row=1, column=10, columnspan=1)
        self.pres_label = ttk.Label(self.mainframe, text="Pressue:").grid(row=1, column=12, columnspan=1)
        self.batt_label = ttk.Label(self.mainframe, text="Battery:").grid(row=1, column=14, columnspan=1)
        self.accX_label = ttk.Label(self.mainframe, text="X Acceleration:").grid(row=2, column=10, columnspan=1)
        self.accY_label = ttk.Label(self.mainframe, text="Y Acceleration:").grid(row=2, column=12, columnspan=1)
        self.accZ_label = ttk.Label(self.mainframe, text="Z Acceleration:").grid(row=2, column=14, columnspan=1)
        self.frange_label = ttk.Label(self.mainframe, text="Front Range:").grid(row=3, column=10, columnspan=1)
        self.brange_label = ttk.Label(self.mainframe, text="Bottom Range:").grid(row=3, column=12, columnspan=1)
        self.placeholder = tk.Label(self.mainframe, text=" ")

        # add tkinter labels for graphs
        self.temp_graph_title = ttk.Label(self.mainframe, text="Temperature", style="title.TLabel").grid(row=0, column=1, columnspan=2)
        self.pres_graph_title = ttk.Label(self.mainframe, text="Pressure", style="title.TLabel").grid(row=0, column=5, columnspan=2)
        self.batt_graph_title = ttk.Label(self.mainframe, text="Battery", style="title.TLabel").grid(row=4, column=1, columnspan=2)
        self.angle_graph_title = ttk.Label(self.mainframe, text="Roll/Pitch/Yaw", style="title.TLabel").grid(row=4, column=5, columnspan=2)

        # Add a standard 5 pixel padding to all widgets
        for w in self.mainframe.winfo_children():
            w.grid(padx=5, pady=5)

        # self.sensor_poll()
        # update_sensor_data()
        self.update_table()

        # Set up plot to call animate() function periodically
        self.ani_temp = animation.FuncAnimation(self.fig_temp, self.animate_temp, fargs=(xs1, temp), interval=250)
        self.ani_pres = animation.FuncAnimation(self.fig_pres, self.animate_pres, fargs=(xs2, pres), interval=250)
        self.ani_batt = animation.FuncAnimation(self.fig_batt, self.animate_batt, fargs=(xs3, batt), interval=250)
        self.ani_angle = animation.FuncAnimation(self.fig_angles, self.animate_xyz, interval=250)

        self.root.mainloop()

    # update sensor variables at regular intervals
    def sensor_poll(self):
        self.temperature = self.drone.get_drone_temp()
        self.battery = self.drone.get_battery()
        self.pressure = round(self.drone.get_pressure() / 1000, 3)
        self.rollAngle = self.drone.get_x_angle()
        self.pitchAngle = self.drone.get_y_angle()
        self.yawAngle = self.drone.get_z_angle()
        self.accX = self.drone.get_x_accel()
        self.accY = self.drone.get_y_accel()
        self.accZ = self.drone.get_z_accel()
        self.frontRange = self.drone.get_front_range()
        self.bottomRange = self.drone.get_bottom_range()

        self.placeholder.after(250, self.sensor_poll)

    def animate_temp(self, i, xs1, temp):
        # try:
        #     new_temp = round(drone.get_drone_temp(), 2)
        # except:
        #     pass

        # Add x and y1 to lists
        xs1.append(dt.datetime.now().strftime('%S'))
        temp.append(self.temperature)

        # Limit x and y1 lists to 20 items
        xs1 = xs1[-self.max_elements:]
        temp = temp[-self.max_elements:]

        # Draw x and y1 lists
        self.ax_temp.clear()
        self.ax_temp.plot(xs1, temp, 'r')

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)

    def animate_pres(self, i, xs2, pres):
        # try:
        #     new_pres = round(drone.get_pressure() / 1000)
        # except:
        #     pass

        # Add x and y1 to lists
        xs2.append(dt.datetime.now().strftime('%S'))
        pres.append(self.pressure)

        # Limit x and y1 lists to 20 items
        xs2 = xs2[-self.max_elements:]
        pres = pres[-self.max_elements:]

        # Draw x and y1 lists
        self.ax_pres.clear()
        self.ax_pres.plot(xs2, pres, 'b')

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)

    def animate_batt(self, i, xs3, batt):
        # try:
        #     new_batt = drone.get_battery()
        # except:
        #     pass

        # Add x and y1 to lists
        xs3.append(dt.datetime.now().strftime('%S'))
        batt.append(self.battery)

        # Limit x and y1 lists to 20 items
        xs3 = xs3[-self.max_elements:]
        batt = batt[-self.max_elements:]

        # Draw x and y1 lists
        self.ax_batt.clear()
        self.ax_batt.plot(xs3, batt, 'g')

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)

    def animate_xyz(self, i):
        # try:
        #     roll = drone.get_x_angle()
        #     pitch = drone.get_y_angle()
        #     yaw = drone.get_z_angle()
        # except:
        #     pass

        self.ax_angles.clear()
        self.ax_angles.set_xlim([-180, 180])
        self.ax_angles.set_ylim([-180, 180])
        self.ax_angles.set_zlim([-180, 180])

        self.ax_angles.quiver(self.start[0], self.start[1], self.start[0], self.rollAngle, 0, 0, color='r')
        self.ax_angles.quiver(self.start[0], self.start[1], self.start[0], 0, self.pitchAngle, 0, color='g')
        self.ax_angles.quiver(self.start[0], self.start[1], self.start[0], 0, 0, self.yawAngle, color='b')

    def update_table(self):
        temp_val_label = ttk.Label(self.mainframe, text=" ")
        pres_val_label = ttk.Label(self.mainframe, text=" ")
        batt_val_label = ttk.Label(self.mainframe, text=" ")
        accX_val_label = ttk.Label(self.mainframe, text=" ")
        accY_val_label = ttk.Label(self.mainframe, text=" ")
        accZ_val_label = ttk.Label(self.mainframe, text=" ")
        frange_val_label = ttk.Label(self.mainframe, text=" ")
        brange_val_label = ttk.Label(self.mainframe, text=" ")

        temp_val_label['text'] = str(self.temperature)
        pres_val_label['text'] = str(self.pressure)
        batt_val_label['text'] = str(self.battery)
        accX_val_label['text'] = str(self.accX)
        accY_val_label['text'] = str(self.accY)
        accZ_val_label['text'] = str(self.accZ)
        frange_val_label['text'] = str(self.frontRange)
        brange_val_label['text'] = str(self.bottomRange)

        temp_val_label.grid(row=1, column=11, columnspan=1)
        pres_val_label.grid(row=1, column=13, columnspan=1)
        batt_val_label.grid(row=1, column=15, columnspan=1)
        accX_val_label.grid(row=2, column=11, columnspan=1)
        accY_val_label.grid(row=2, column=13, columnspan=1)
        accZ_val_label.grid(row=2, column=15, columnspan=1)
        frange_val_label.grid(row=3, column=11, columnspan=1)
        brange_val_label.grid(row=3, column=13, columnspan=1)

        # self.placeholder.after(250, self.update_table)


def thread_function():
    dashboard.run()


def update_sensor_data():
    dashboard.temperature = data_list[0] = drone.get_drone_temp()
    dashboard.battery = data_list[1] = drone.get_battery()
    dashboard.pressure = data_list[2] = drone.get_pressure()
    dashboard.rollAngle = data_list[3] = drone.get_x_angle()
    dashboard.pitchAngle = data_list[4] = drone.get_y_angle()
    dashboard.yawAngle = data_list[5] = drone.get_z_angle()
    dashboard.accX = data_list[6] = drone.get_x_accel()
    dashboard.accY = data_list[7] = drone.get_y_accel()
    dashboard.accZ = data_list[8] = drone.get_z_accel()
    dashboard.frontRange = data_list[9] = drone.get_front_range()
    dashboard.bottomRange = data_list[10] = drone.get_bottom_range()


# ================================================================================
# initialize sensor data
dashboard = DroneDashboard()
update_sensor_data()

# creating thread
t1 = threading.Thread(target=thread_function)
# starting thread 1
t1.start()

# INSERT FLIGHT CODE HERE. MAKE SURE TO INCLUDE update_sensor_data() BETWEEN EACH LINE TO UPDATE DASHBOARD
update_sensor_data()
drone.takeoff()

update_sensor_data()
drone.set_yaw(30)
drone.move(3)

update_sensor_data()
drone.land()

update_sensor_data()

drone.close()
sys.exit()

