import matplotlib.pyplot as plt
import numpy as np


def load_streamflow(filename):
    """Read the streamflow CSV. Return the dates and a 2D array of flows (cfs),
    one column per gauge."""
    data = np.loadtxt(filename, delimiter=',', dtype=str, skiprows=1)
    dates = data[:, 0]
    flows = data[:, 1:].astype(float)
    return dates, flows


def plot_streamflow(dates, flows, sites):
    """Plot the flow at each gauge with the Matplotlib homework formatting."""
    colors = ['tab:purple', 'tab:gray', 'tab:green', 'tab:olive', 'tab:red']

    plt.figure(figsize=(9, 5))

    for column, (site, color) in enumerate(zip(sites, colors)):
        plt.plot(dates, flows[:, column], color=color, label=site)

    plt.title('Provo River Streamflow Data (2021)')
    plt.xlabel('Date')
    plt.ylabel('Flowrate (cfs)')
    plt.legend(title='Site Numbers', loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xticks(dates[::5])
    plt.show()


# Main program
sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]
dates, flows = load_streamflow("June-2021-Provo-River-Streamflow-Rates.csv")
plot_streamflow(dates, flows, sites)
