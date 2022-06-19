import pandas as pd
from operator import itemgetter
from utils import check_hexacolor
from utils import euclidean_distance
from utils import get_cli_args
from monkey_model import Monkey
from monkey_visualize import scatter_plot


def read_monkeys_from_csv(csv_path, strict=False):
    """Create and process a pandas dataframe of monkeys."""
    monkeys_df = pd.read_csv(csv_path)                                          # import .csv as a pandas dataframe

    if strict:                                                                  # if strict mode is on
        if "" in monkeys_df:                                                    # check no value is missing
            raise ValueError("Values are missing in the dataframe.")
        elif monkeys_df.isnull().any().any():                                   # check no value is missing
            raise ValueError("Values are missing in the dataframe.")
        else:
            return monkeys_df
    else:                                                                       # if strict mode is off (default)

        monkeys_df.columns = ["species", "size", "weight", "fur_color"]         # rename columns
        monkeys_df = monkeys_df[["fur_color", "species", "size", "weight"]]     # reorder columns

        if list(monkeys_df) != ["fur_color", "species", "size", "weight"]:      # check what we hard-coded just above
            raise ValueError("Dataframe headers are incorrect.")

        monkeys_df["species"] = monkeys_df["species"].fillna("")                # replace NaN in species column by ""

        monkeys_df = monkeys_df.dropna()                                            # drop any row with NaN value
        monkeys_df = monkeys_df.drop(monkeys_df[monkeys_df["size"] <= 0].index)     # drop any row with size <= 0
        monkeys_df = monkeys_df.drop(monkeys_df[monkeys_df["weight"] <= 0].index)   # drop any row with weight <= 0
        # drop any row with invalid hexadecimal code
        monkeys_df = monkeys_df.drop(monkeys_df[monkeys_df["fur_color"].apply(check_hexacolor) != True].index)

        # create a column monkey with Monkey() class objects
        monkeys_df["monkey"] = monkeys_df.apply(lambda x: Monkey(x["fur_color"],
                                                                 x["size"],
                                                                 x["weight"],
                                                                 x["species"]), axis=1)
        # create a column fur_color_int with int values
        monkeys_df["fur_color_int"] = monkeys_df["fur_color"].apply(lambda x: x[1:])        # copy column + remove "#"
        monkeys_df["fur_color_int"] = monkeys_df["fur_color_int"].apply(lambda x: int(x, 16))   # convert str to int
        monkeys_df["bmi"] = monkeys_df["monkey"].apply(lambda x: x.compute_bmi())               # create a column bmi

        # create a new column in 0th position, named id, starting at 0
        monkeys_df.insert(0, "id", range(0, 0 + len(monkeys_df)))

        # create a column empty_str to classify the monkeys based on wether "species" was "" or not
        monkeys_df.loc[monkeys_df["species"] == "", "empty_str"] = "yes"    # if "" in species, fill yes in empty_str
        monkeys_df.loc[monkeys_df["species"] != "", "empty_str"] = "no"     # if "" not in species, fill no in empty_str

        return monkeys_df


def compute_knn(dataframe, k=5):
    """KNN classification algorithm to retrieve
    the species attribute of Monkey objects whenever it is missing."""

    print("KNN computation running...\nEstimated runtime: 1min 20sec.")

    for index1, row1 in dataframe.iterrows():           # for each unlabelled item
        if row1[8] == "yes":
            my_dict = {}                                # create a dict
            for index2, row2 in dataframe.iterrows():   # for each labelled item
                if row2[8] == "no":
                    # fill the dict with {labelled item: distance to unlabelled item} pairs
                    my_dict[row2[0]] = euclidean_distance(row1[7], row1[6], row2[7], row2[6])

            # list of k tuples (index of labelled item, distance to unlabelled item)
            # which are the closest to the unlabelled item
            k_closest = sorted(my_dict.items(), key=itemgetter(1))[:k]

            # retrieve from the dataframe the names of the k species listed in k_closest
            close_species = []
            for i in k_closest:
                close_species.append(dataframe.loc[dataframe["id"] == i[0], "species"].iloc[0])

            # compute the most frequent species name in close_species
            closest_species = max(set(close_species), key=close_species.count)

            # update the dataframe and replace the empty string by the closest species
            dataframe.loc[dataframe.id == row1[0], "species"] = closest_species

    return dataframe


def save_to_csv(dataframe, csv_filename):
    """Save the values of the columns species, fur_color, size, and weight to a CSV."""

    # drop unwanted columns
    dataframe = dataframe.drop(["id", "monkey", "fur_color_int", "bmi", "empty_str"], axis=1)

    # save the dataframe to a .csv
    dataframe.to_csv(csv_filename, index=False)


def main():
    args = get_cli_args()                                   # retrieve the CLI arguments

    if args.subparser == "knn":                             # if the first positional argument is knn

        processed_df = read_monkeys_from_csv(args.input)    # process the dataframe and store it in a variable
        knn_df = compute_knn(processed_df)                  # run the KNN algorithm and store the results in a variable
        save_to_csv(knn_df, args.output)                    # save the final dataframe to a CSV file

    if args.subparser == "visualize":                       # if the first positional argument is visualize

        df = read_monkeys_from_csv(args.input, strict=True)     # import a CSV with strict mode on
        x = df[args.columns[0]]                                 # set x as a dataframe column
        y = df[args.columns[1]]                                 # set y as a dataframe column
        labels = df["species"]                                  # set labels as the species column
        scatter_plot(x, y, labels)                              # create a scatter plot


if __name__ == "__main__":
    main()
