import matplotlib.pyplot as plt 
import numpy as np

def plot(slices, delays, metrics):
    """Draws a diagram comparing the delay values and metric values."""
    x = np.arange(len(slices))
    colWidth = 0.4

    fig, ax = plt.subplots()

    ax.bar(x, delays, colWidth, label="Delays")
    ax.bar(x + colWidth, metrics, colWidth, label="Metric")

    ax.set_ylabel("Value")
    ax.set_xlabel("Time slice")
    ax.set_title("Compare delays to metric")
    ax.set_xticks(x + colWidth / 2)
    ax.set_xticklabels(slices)
    ax.legend()

    fig.tight_layout()

    plt.show()