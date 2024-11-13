import pandas as pd
import folium
from folium.plugins import MarkerCluster
from sklearn.cluster import KMeans
from geopy.distance import geodesic
import os

#This function just loads the csv file with all the datasets and gives
#back an error if the file is not found
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

#This function creates a map with the mean of the startLat and Lon to ceter
#the initial view of the map with a start zoom of 12 with necessary copyrights
def create_map(lat, lon):
    return folium.Map(
        location=[lat, lon],
        zoom_start=12,
        prefer_canvas=True,
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    )


# Function to calculate high-demand clusters without nearby taxi stands
def find_high_demand_clusters(taxi_data, taxi_stands, n_clusters=50, distance_threshold=500):
    pickup_coords = taxi_data[['StartLat', 'StartLon']].dropna()
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(pickup_coords)
    pickup_coords['Cluster'] = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_
    
    def distance_to_nearest_stand(cluster_center, taxi_stands):
        distances = taxi_stands.apply(lambda row: geodesic(cluster_center, (row['Latitude'], row['Longitude'])).meters, axis=1)
        return distances.min()
    
    high_demand_clusters = []
    for i, center in enumerate(cluster_centers):
        dist = distance_to_nearest_stand(center, taxi_stands)
        if dist > distance_threshold:  
            high_demand_clusters.append(i)
    
    return cluster_centers, high_demand_clusters

#This function just adds the datapoints into clusters using the MarkerCluster
#method. map_object is the map, data is the csv/excel file, max markers assures
#map isnt overhwhelmed by allowing only 1000 markers
def add_marker_cluster(map_object, data, max_markers=1000):
    marker_cluster = MarkerCluster().add_to(map_object)
    for index, row in data.head(max_markers).iterrows():
        folium.Marker(
            location=[row['StartLat'], row['StartLon']],
            popup=f"Start Time: {row['StartDateTime']}",
        ).add_to(marker_cluster)

def add_marker_cluster_stands(map_object, taxi, max_markers=1000):
    marker_cluster = MarkerCluster().add_to(map_object)
    for index, row in taxi.head(max_markers).iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Taxi Stand: {row['Taxi Rank Name - English']}",
            icon=folium.Icon(color='blue', icon='taxi', prefix='fa')  
        ).add_to(marker_cluster)
    
def add_high_demand_markers(map_object, cluster_centers, high_demand_clusters):
    high_demand_layer = folium.FeatureGroup(name='High-Demand Clusters')
    marker_cluster = MarkerCluster().add_to(high_demand_layer)
    
    for i in high_demand_clusters:
        centroid = cluster_centers[i]
        folium.Marker(
            location=[centroid[0], centroid[1]],
            popup=f"High-demand Cluster Centroid: ({centroid[0]:.4f}, {centroid[1]:.4f})",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(marker_cluster)

    high_demand_layer.add_to(map_object)
    return high_demand_layer

#This function just savres the map as a new html file
def save_map(map_object, file_name):
    map_object.save(file_name)
    if os.path.exists(file_name):
        print(f"Map saved to {file_name}")
    else:
        print("File was not created successfully")


# Main function to run the visualization
def main():
    taxi_data = load_data("anonymized-taxi-data.csv")
    taxi_stands = pd.read_excel("TaxiRanks.xlsx")  # Load existing taxi stands data
    
    if taxi_data is None or taxi_stands is None:
        return  # Exit if data can't be loaded

    center_lat = taxi_data['StartLat'].mean()
    center_lon = taxi_data['StartLon'].mean()
    map_object = create_map(center_lat, center_lon)

    # Feature groups for layer control
    pickup_layer = folium.FeatureGroup(name='Pickup Points')
    taxi_stand_layer = folium.FeatureGroup(name='Taxi Stands')
    
    add_marker_cluster(pickup_layer, taxi_data)
    add_marker_cluster_stands(taxi_stand_layer, taxi_stands)

    cluster_centers, high_demand_clusters = find_high_demand_clusters(taxi_data, taxi_stands)
    high_demand_layer = add_high_demand_markers(map_object, cluster_centers, high_demand_clusters)

    # Add all layers to the map
    pickup_layer.add_to(map_object)
    taxi_stand_layer.add_to(map_object)
    high_demand_layer.add_to(map_object)

    # Add layer control after all layers have been added to the map
    folium.LayerControl().add_to(map_object)

    output_file = 'taxi_start_times_map.html'
    save_map(map_object, output_file)

# Run the main function
if __name__ == "__main__":
    main()