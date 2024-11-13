# Dynamic Taxi Stand Allotment

## Project Overview

This project was developed for the "UAE Gen AI Hackathon 2024," organized by Alibaba Cloud and the Roads and Transport Authority (RTA) in Dubai, held at the University of Birmingham, Dubai. The hackathon's objective was to leverage Generative AI to enhance the taxi services provided by the RTA. Our team proposed a solution named "Dynamic Taxi Stand Allotment" to address issues around the availability of taxis in high-demand areas.

## Problem Statement

Dubai's taxi services experience fluctuations in demand across different regions. While some areas have a high density of taxi stands, others with high demand lack nearby stands, leading to inefficiencies in taxi distribution and customer wait times. Our goal was to identify high-demand areas that currently lack taxi stands and propose new stand locations to improve service accessibility.

## Solution Approach

Our solution uses KMeans clustering and geolocation analysis to recommend new taxi stand locations:

1. **Data Gathering**: 
   - We were provided with data on taxi ranks across Dubai (`TaxiRanks.xlsx`) and anonymized data for the starting points of various taxi trips in Dubai (`anonymized-taxi-data.csv`), including latitude and longitude coordinates.

2. **Clustering**:
   - Using a KMeans clustering model, we grouped taxi trip start locations into 50 clusters, representing different areas of demand across Dubai. This step was executed in the Jupyter notebook `clustering.ipynb`.

3. **Distance Calculation and Demand Labeling**:
   - With GeoPy, we calculated the distance between the centroid of each cluster and the nearest taxi rank.
   - We then labeled clusters as either:
     - "High demand with no taxi rank nearby" or 
     - "Low demand with a taxi rank nearby".

4. **Mapping and Visualization**:
   - Using the Folium library, we mapped the existing taxi ranks, the cluster centroids, and the start locations of random trips. The resulting map highlights potential areas for new taxi stands in high-demand regions.
   - This mapping was done in `mapping.py`.

5. **Proposed New Taxi Stand Locations**:
   - The centroids of clusters labeled as "high demand" represent our recommended locations for new taxi stands. These could potentially optimize taxi availability and reduce wait times for customers.

## Files in the Repository

- **TaxiRanks.xlsx**: Dataset containing the locations of current taxi ranks in Dubai.
- **anonymized-taxi-data.csv**: Dataset of anonymized start locations for taxi trips in Dubai.
- **clustering.ipynb**: Jupyter notebook where we applied KMeans clustering to identify high and low-demand areas.
- **mapping.py**: Python script using Folium to generate an interactive map of taxi ranks, trip start locations, and recommended new taxi stand locations.

## Tools and Libraries Used

- **Python**: For data processing and modeling.
- **KMeans (from sklearn)**: Used to cluster the taxi trip start locations.
- **GeoPy**: For calculating distances between cluster centroids and taxi ranks.
- **Folium**: For mapping and visualization of demand areas and proposed taxi stands.

## Installation

To use the **OptionsPricing** web application locally, follow the instructions below:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PrinceAJ17/Taxi-Stand-Allotment.git
   cd Taxi-Stand-Allotment

2. **Run the application:**

   To start the web application, run the following command:

   ```bash
   python mapping.py
   ```
   Open taxi_start_times_map.html on your web browser.

## Conclusion

Our solution provides RTA with insights into where new taxi stands could be beneficial based on demand patterns in Dubai. By optimizing the placement of taxi stands, this solution aims to enhance service efficiency and customer satisfaction for Dubai's taxi riders.

