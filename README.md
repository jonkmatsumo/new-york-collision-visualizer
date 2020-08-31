# New York Collision Visualizer #

#### To view the live demo deployed on Heroku, click [here](https://nyc-visualizer.herokuapp.com/). ####

The following is an interactive data science web application built using the Streamlit library in Python. The results are based on a public dataset on Motor Vehicle Collisions 
from the [City of New York](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95). By navigating through the various menus, one can sort these
collisions by location and date of time - and the results are dynamically generated in real time.

The following screens explain how to navigate the interface:

![Sample Map 1](/assets/sample_display_nyc.PNG).

Initially, 5000 entries from the dataset (provided in .csv format) are loaded. This amount can be changed as necessary, but increasing the amount of entries will significantly increase the time required to generate the dataset. This is cached so that this data only needs to be loaded only one time each time the user changes the amount.
The second sidebar allows the user to select how many people were injured in an accident, and the site displays the results.

![Sample Map 2](/assets/sample_display_nyc_2.PNG).

This map is similar to the first except it groups the numbers by time of day instead of people injured.

![Sample Map 3](/assets/sample_display_nyc_3.PNG).

The final display shows the information in the maps in a more concise graph form. Additionally, the user can see the specific streets that have the highest frequency of injuriesby navigating the menu at the bottom.

To run this application, either check out the [live demo](https://nyc-visualizer.herokuapp.com/) deployed on Heroku or download the repository and run the following in the Terminal:
> streamlit run app.py.

Note that this application makes use of the following libraries: Numpy, Pandas, Plotly, Pydeck, and Streamlit. For more information, check *requirements.txt*. 
