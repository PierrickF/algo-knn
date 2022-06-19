import pandas as pd
import matplotlib.pyplot as plt


def scatter_plot(x, y, labels):
    """Produces a matplotlib scatter plot."""

    assert len(x) == len(y) == len(labels), "The arguments should have the same length."    # check columns length

    df = pd.concat([x, y, labels], axis=1)                                                  # recreate a pandas df

    groups = df.groupby("species")                                                          # group by species

    for name, group in groups:                                                              # plot each datapoint
        plt.plot(group.iloc[:, 0], group.iloc[:, 1], marker="o", linestyle="", label=name)
    plt.legend()                                                                            # create a legend

    # plt.savefig("data/scatter_plot.jpg")

    plt.show()                                                                              # display scatter plot
