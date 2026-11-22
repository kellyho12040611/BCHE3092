What did the AI agent do?

The AI agent generated the initial Python Streamlit code. It successfully understood my requirements for the Bradford Assay and correctly implemented the linear regression math using `scipy.stats.linregress`. It also did a great job formatting the graph with matplotlib.

What worked well:
The math was accurate. When I tested it with the standard curve data, the R-squared value was 0.9998, which shows a very strong linear fit. The app have successfully calculated the unknown protein concentration (5.204 µg/mL) when I inputted the absorbance of 0.3900.

What did not work (and how I fixed it):
The main problem was technical. Initially, I tried to build this in R Shiny, but installing the R packages in the Codespaces terminal kept failing with errors. I decided to use to Python Streamlit instead.