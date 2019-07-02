#!/user/bin/end pythin
import numpy as np
import os
import math
import matplotlib.pyplot as plt
from matplotlib import dates, rcParams
import pandas as pd

# Explicitly registering datetime converters due to future warning in pandas
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Number of data points used
PERIODS = 48
# Steps in y axis
STEPS = 5

def main():
    plotFileName = 'bandwidth.png'
    createPlot(plotFileName)
    os.startfile(plotFileName)

def createPlot(plotFileName):
    df = readData()
    # Insert function to find y limits, pass to makePlotFile
    lower, upper = findLims(df)
    makePlotFile(df, plotFileName, lower, upper)

def readData():
    df = pd.io.parsers.read_csv(
        'speedtest.log',
        names = "date time ping download upload".split(),
        header = None,
        sep = r'\s+',
        parse_dates = {'timestamp' :[0, 1]},
        na_values = ['TEST', 'FAILED'],
    )
    print(df)
    # Change to allow user to specify data
    return df[-PERIODS:] # return data for the last 48 periods

def findLims(last24):
    lower = math.floor(min(last24['download']))
    upper = math.ceil(max(last24['download']))
    return lower, upper

def makePlotFile(last24, filePlotName, lower, upper):
    rcParams['xtick.labelsize'] = 'xx-small'

    plt.plot(last24['timestamp'], last24['download'], 'b-')
    # Change title to reflect data presented
    plt.title('1108 Hopkind Rd Bandwidth Report (last 24 hours)')
    plt.ylabel('Bandwidth in MBps')
    # y axis ticks reflect upper and lowe data points
    # Steps set by user
    plt.yticks(np.arange(lower, upper + 1, step = STEPS))
    plt.ylim(float(lower), float(upper))

    plt.xlabel('Date/Time')
    plt.xticks(rotation = '45')

    plt.grid()

    currentAxes = plt.gca()
    currentFigure = plt.gcf()

    hfmt = dates.DateFormatter('%m/%d %H:%M')
    currentAxes.xaxis.set_major_formatter(hfmt)
    currentFigure.subplots_adjust(bottom = .25)

    loc = currentAxes.xaxis.get_major_locator()
    loc.maxticks[dates.HOURLY] = 24
    loc.maxticks[dates.MINUTELY] = 60

    currentFigure.savefig(filePlotName)

if __name__ == '__main__':
    main()