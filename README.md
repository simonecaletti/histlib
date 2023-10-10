# histlib
Usage

If you have a histogram file you might use the DataFile class to upload it with python. Here we give a tutorial to do with the interactice python interface after you download the histlib library.

> python
>
> import hist
>
> df10 = hist.DataFile("./gao_t10.dat")
> df19 = hist.DataFile("./gao_t19.dat")
> df20 = hist.DataFile(".gao_t20.dat")

Now we have uploaded 3 different data file. We can access to their information in two formats.
As a matrix using

> df10.get_array()

or as a dictionary

> dict10 = df10.get_dict()
> dict10["col0"]

and with the last line we print the "col0" (first column by default) of the df10 DataFrame.
Furthermore, since we have more than one DataFile for the same project, it might be convenient to collect all of them together using the Collection class.

> df_list = [df10, df19, df20]
> features = ["t10", "t19", "t20"]
> project = hist.Collection(df_list, features)
>
> myhistograms = project.get_dict()

Now we can access the histogram information in the following way

> project["t10"]["col0"]

exaclty as described before for dict10 but for all the Collection of DataFrame in a single shot.
Would be nice to make Collection nesting...
