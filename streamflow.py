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
    plt.savefig("provo_streamflow.png", dpi=150, bbox_inches="tight")
    plt.show()


def summarize(dates, flows, sites):
    # Excel check for gauge 10163000: MAX = 131.0 cfs; AVERAGE = 56.95236111111111 cfs
    print(f"{'Gauge':<12}{'Max (cfs)':>10}{'Date of max':>23}{'Min (cfs)':>12}{'Avg (cfs)':>12}")

    with open("streamflow_summary.csv", "w") as summary_file:
        summary_file.write("Gauge,Max (cfs),Date of max,Min (cfs),Avg (cfs)\n")

        for column, site in enumerate(sites):
            gauge_flows = flows[:, column]
            maximum = np.max(gauge_flows)
            maximum_index = np.argmax(gauge_flows)
            minimum = np.min(gauge_flows)
            average = np.mean(gauge_flows)
            date_of_max = dates[maximum_index]

            print(
                f"{site:<12}"
                f"{maximum:10.1f}"
                f"{date_of_max:>23}"
                f"{minimum:12.1f}"
                f"{average:12.1f}"
            )
            summary_file.write(
                f"{site},{maximum:.1f},{date_of_max},{minimum:.1f},{average:.15g}\n"
            )


# Main program
sites = ["10163000", "10155200", "10155500", "10154200", "10155000"]
dates, flows = load_streamflow("June-2021-Provo-River-Streamflow-Rates.csv")
summarize(dates, flows, sites)

threshold = float(input("Enter a flow threshold (cfs): "))

# Each 15-minute reading counts as 0.25 hours, so count readings above the
# threshold and multiply the count for each gauge by 0.25.
print("\nHours above threshold:")
for column, site in enumerate(sites):
    above_threshold = np.sum(flows[:, column] > threshold)
    hours_above = above_threshold * 0.25
    print(f"{site:<12}{hours_above:>8.2f} hours")

plot_streamflow(dates, flows, sites)
