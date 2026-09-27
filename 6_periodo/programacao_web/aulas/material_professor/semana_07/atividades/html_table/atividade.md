Challenge: Structuring a planet data table

In this challenge, we provide data on the planets in our solar system. Your job is to structure it into an accessible HTML table.

Starting Point

Create a new folder in an appropriate location on your computer called planet-data-table (or open an online editor and take the required steps to create a new project).

Save the following HTML listing inside a file inside your folder called index.html (or paste it into your online editor's HTML pane).

<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>Planet data table</title>
    <link href="style.css" rel="stylesheet" type="text/css" />
  </head>
  <body>
    <h1>Planet data table</h1>
  </body>
</html>

Save the following CSS listing inside a file inside your folder called style.css (or paste it into your online editor's CSS pane)

html {
font-family: sans-serif;
}

table {
border-collapse: collapse;
border: 2px solid rgb(200 200 200);
letter-spacing: 1px;
font-size: 0.8rem;
}

td,
th {
border: 1px solid rgb(190 190 190);
padding: 10px 20px;
}

th {
background-color: rgb(235 235 235);
}

td {
text-align: center;
}

tr:nth-child(even) td {
background-color: rgb(250 250 250);
}

tr:nth-child(odd) td {
background-color: rgb(245 245 245);
}

caption {
padding: 10px;
}

.column-border {
border: 2px solid black;
}


Keep the following data handy; you'll need to turn this into an HTML data table inside your HTML

Rows

Terrestrial planets

Mercury 0.330 4,879 5427 3.7 4222.6 57.9 167 0 Closest to the Sun
Venus 4.87 12,104 5243 8.9 2802.0 108.2 464 0
Earth 5.97 12,756 5514 9.8 24.0 149.6 15 1 Our world
Mars 0.642 6,792 3933 3.7 24.7 227.9 -65 2 The red planet

Jovian planets

Gas giants

Jupiter 1898 142,984 1326 23.1 9.9 778.6 -110 67 The largest planet
Saturn 568 120,536 687 9.0 10.7 1433.5 -140 62

Ice giants

Uranus 86.8 51,118 1271 8.7 17.2 2872.5 -195 27
Neptune 102 49,528 1638 11.0 16.1 4495.1 -200 14

Dwarf planets*

Pluto 0.0146 2,370 2095 0.7 153.3 5906.4 -225 5 Declassified as a planet in 2006, but this <a href="http://www.usatoday.com/story/tech/2014/10/02/pluto-planet-solar-system/16578959/">remains controversial</a>.

Columns

Name
Mass (10<sup>24</sup>kg)
Diameter (km)
Density (kg/m<sup>3</sup>)
Gravity (m/s<sup>2</sup>)
Length of day (hours)
Distance from Sun (10<sup>6</sup>km)
Mean temperature (°C)
Number of moons
Notes

Caption

Data about the planets of our solar system (Planetary facts taken from <a href="http://nssdc.gsfc.nasa.gov/planetary/factsheet/">Nasa's Planetary Fact Sheet - Metric</a>).

Project Brief

You are working at a school; currently, your students are studying the planets of our solar system, and you want to provide them with an easy-to-follow set of data to look up facts and figures about the planets. An HTML data table would be ideal — you need to take the raw data you have available and turn it into a table, following the steps below.

All the data you need is contained in the data listing provided above. If you have trouble visualizing the data, take a look at the live example below, or try drawing a diagram.

    Start the table off by giving it an outer container, a table header, and a table body. You don't need a table footer for this example.
    Add the provided caption to your table.
    Add a row to the table header containing all the column headers.
    Create all the content rows inside the table body, remembering to make all the row headings into headings semantically.
    Ensure all the content is placed into the right cells — in the raw data, each row of planet data is shown next to its associated planet.
    Add attributes to make the row and column headers unambiguously associated with the rows, columns, or row groups that they act as headings for.
    Add a black border just around the column that contains all the planet name row headers. Do this using a suitable <colgroup>/<col> structure and the .column-border class style provided in the CSS.

Hins and tips


    The first cell of the header row needs to be blank, and span two columns.
    The group row headings (e.g., Jovian planets) that sit to the left of the planet name row headings (e.g., Saturn) are a little tricky to sort out — you need to make sure each one spans the correct number of rows and columns.
    One way of associating headers with their rows/columns is a lot easier than the other way.

Example

The table should look like the following after being marked up correctly. If you get stuck, check out the solution below the live example.

