import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
from codrone_edu.drone import *

data_list = [0] * 11

drone = Drone()
drone.pair()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget3 = pg.PlotWidget()
        self.graphWidget4 = pg.PlotWidget()
        self.graphWidget5 = pg.PlotWidget()
        self.graphWidget6 = pg.PlotWidget()
        self.graphWidget7 = pg.PlotWidget()
        self.graphWidget8 = pg.PlotWidget()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.graphWidget1, 0, 0)
        layout.addWidget(self.graphWidget2, 0, 1)
        layout.addWidget(self.graphWidget3, 0, 2)
        layout.addWidget(self.graphWidget4, 1, 0)
        layout.addWidget(self.graphWidget5, 1, 2)
        layout.addWidget(self.graphWidget6, 2, 0)
        layout.addWidget(self.graphWidget7, 2, 1)
        layout.addWidget(self.graphWidget8, 2, 2)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.x = list(range(100))  # 100 time points
        self.y1 = [0 for _ in range(100)]  # 100 data points
        self.y2 = [0 for _ in range(100)]  # 100 data points
        self.y3 = [0 for _ in range(100)]  # 100 data points
        self.y4 = [0 for _ in range(100)]  # 100 data points
        self.y5 = [0 for _ in range(100)]  # 100 data points
        self.y6 = [0 for _ in range(100)]  # 100 data points
        self.y7 = [0 for _ in range(100)]  # 100 data points
        self.y8 = [0 for _ in range(100)]  # 100 data points

        self.graphWidget1.setBackground('w')
        self.graphWidget2.setBackground('w')
        self.graphWidget3.setBackground('w')
        self.graphWidget4.setBackground('w')
        self.graphWidget5.setBackground('w')
        self.graphWidget6.setBackground('w')
        self.graphWidget7.setBackground('w')
        self.graphWidget8.setBackground('w')

        self.graphWidget1.setTitle("Temperature (C)")
        self.graphWidget2.setTitle("Battery (%)")
        self.graphWidget3.setTitle("Pressure (kPa)")
        self.graphWidget4.setTitle("Bottom Range Distance (cm)")
        self.graphWidget5.setTitle("Front Range Distance (cm)")
        self.graphWidget6.setTitle("Roll")
        self.graphWidget7.setTitle("Pitch")
        self.graphWidget8.setTitle("Yaw")

        pen1 = pg.mkPen(color=(255, 0, 0))
        pen2 = pg.mkPen(color=(255, 127, 0))
        pen3 = pg.mkPen(color=(0, 0, 255))
        pen4 = pg.mkPen(color=(0, 0, 0))
        pen5 = pg.mkPen(color=(0, 255, 0))
        self.data_line1 = self.graphWidget1.plot(self.x, self.y1, pen=pen1)
        self.data_line2 = self.graphWidget2.plot(self.x, self.y2, pen=pen2)
        self.data_line3 = self.graphWidget3.plot(self.x, self.y3, pen=pen3)
        self.data_line4 = self.graphWidget4.plot(self.x, self.y4, pen=pen4)
        self.data_line5 = self.graphWidget5.plot(self.x, self.y5, pen=pen4)
        self.data_line6 = self.graphWidget6.plot(self.x, self.y6, pen=pen1)
        self.data_line7 = self.graphWidget7.plot(self.x, self.y7, pen=pen5)
        self.data_line8 = self.graphWidget8.plot(self.x, self.y8, pen=pen3)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y1 element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y1 = self.y1[1:]  # Remove the first
        self.y1.append(data_list[0])  # Add a new random value.

        self.y2 = self.y2[1:]  # Remove the first
        self.y2.append(data_list[1])  # Add a new random value.

        self.y3 = self.y3[1:]  # Remove the first
        self.y3.append(data_list[2] / 1000)  # Add a new random value.

        self.y4 = self.y4[1:]  # Remove the first
        self.y4.append(data_list[9])  # Add a new random value.

        self.y5 = self.y5[1:]  # Remove the first
        self.y5.append(data_list[10])  # Add a new random value.

        self.y6 = self.y6[1:]  # Remove the first
        self.y6.append(data_list[3])  # Add a new random value.

        self.y7 = self.y7[1:]  # Remove the first
        self.y7.append(data_list[4])  # Add a new random value.

        self.y8 = self.y8[1:]  # Remove the first
        self.y8.append(data_list[5])  # Add a new random value.

        self.data_line1.setData(self.x, self.y1)  # Update the data.
        self.data_line2.setData(self.x, self.y2)  # Update the data.
        self.data_line3.setData(self.x, self.y3)  # Update the data.
        self.data_line4.setData(self.x, self.y4)  # Update the data.
        self.data_line5.setData(self.x, self.y5)  # Update the data.
        self.data_line6.setData(self.x, self.y6)  # Update the data.
        self.data_line7.setData(self.x, self.y7)  # Update the data.
        self.data_line8.setData(self.x, self.y8)  # Update the data.


def thread_function():
    # INSERT FLIGHT CODE HERE. MAKE SURE TO INCLUDE update_sensor_data() BETWEEN EACH LINE TO UPDATE DASHBOARD
    update_sensor_data()
    drone.takeoff()

    update_sensor_data()
    # drone.set_yaw(30)
    # drone.move(3)
    drone.hover(5)

    update_sensor_data()
    drone.land()

    update_sensor_data()

    drone.close()
    sys.exit()


def update_sensor_data():
    data_list[0] = drone.get_drone_temp()
    data_list[1] = drone.get_battery()
    data_list[2] = drone.get_pressure()
    data_list[3] = drone.get_x_angle()
    data_list[4] = drone.get_y_angle()
    data_list[5] = drone.get_z_angle()
    data_list[6] = drone.get_x_accel()
    data_list[7] = drone.get_y_accel()
    data_list[8] = drone.get_z_accel()
    data_list[9] = drone.get_front_range()
    data_list[10] = drone.get_bottom_range()


# ================================================================================
# creating thread
t1 = threading.Thread(target=thread_function)
# starting thread 1
t1.start()

# initialize PyQt Dashboard
app = QtWidgets.QApplication([])
w = MainWindow()
w.show()

app.exec_()


