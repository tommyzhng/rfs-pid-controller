import numpy as np
import matplotlib.pyplot as plt
from time import time

class PID:
    def __init__(self):
        #PID gains

        self.Kp = 1.125
        self.Ki = 0
        self.Kd = 6.48

        #PID params
        self.error = 0
        self.derivative_error = 0
        self.last_error = 0
        self.integral_error = 0

        self.last_derivative = 0

        self.output = 0
        self.prev_output = self.output

        self.prev_time = 0
        self.current_time = 0
        self.time_step = 0

        #setpoint
        self.setpoint = 0

        #plotting
        self.positions = np.array([])
        self.descentRates = np.array([])
        self.times = np.array([])

    def compute(self, altitude, fpm, time):
        self.current_time = time
        self.time_step = self.current_time - self.prev_time

        if self.time_step == 0:
            return self.prev_output
        
        self.altitude = altitude
        self.fpm = fpm
        
        #calculate error
        self.error = self.setpoint - self.altitude
        self.error = (self.error / 1000)
        self.integral_error += (self.error * self.time_step)
        self.derivative_error = ((self.error - self.last_error) / self.time_step)

        if self.derivative_error == 0:
            self.derivative_error = self.last_derivative

        # Calculate PID terms
        proportional_term = self.Kp * self.error
        integral_term = self.Ki * self.integral_error
        derivative_term = self.Kd * self.derivative_error

        # Calculate control output
        self.output = proportional_term + integral_term + derivative_term
        self.output = min(max(self.output, -1), 1)


        #update variables
        self.last_error = self.error
        self.prev_time = self.current_time
        self.last_derivative = self.derivative_error
        
        self.positions = np.append(self.positions, altitude)
        self.descentRates = np.append(self.descentRates, fpm)
        self.times = np.append(self.times, self.current_time)

        self.prev_output = self.output
        
        #self.graph(self.times, self.positions, self.descentRates)
        
        print(f"P: {round(proportional_term, 3)}, I: {round(integral_term, 3)}, D: {round(derivative_term,3)}, Out: {round(self.output, 3)}")
        return self.output
        

    def graph(self, times, positions, descentRates):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig, ax1 = plt.subplots()
        color = 'red'

        ax1.set_xlabel('time (s)')
        ax1.set_ylabel('altitude', color=color)
        ax1.plot(times, positions, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()

        color = 'blue'
        ax2.set_ylabel('fpm', color=color)
        ax2.plot(times, descentRates, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        plt.show()

        

