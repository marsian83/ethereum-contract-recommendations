import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import re
from matplotlib import cm
import random

def load_data(file_path):
    """Load the experiment data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data['data']
    except json.JSONDecodeError:
        # Fix common JSON syntax errors like trailing commas
        print("JSON decode error found. Attempting to fix common issues...")
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Remove trailing commas in arrays/objects
        fixed_content = re.sub(r',\s*([}\]])', r'\1', content)
        
        # Try parsing the fixed content
        try:
            data = json.loads(fixed_content)
            print("Successfully fixed and loaded JSON")
            return data['data']
        except json.JSONDecodeError as e:
            print(f"Still couldn't parse JSON: {e}")
            # Alternative: create a C++ program to parse the file more robustly
            print("Attempting to load using vector format...")
            points = []
            # Simple parsing to extract coordinate triplets
            triplet_pattern = re.compile(r'\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]')
            matches = triplet_pattern.findall(content)
            for match in matches:
                x, y, z = map(int, match)
                points.append([x, y, z])
            
            print(f"Loaded {len(points)} points using regex parsing")
            return points

def visualize_3d_points(points):
    """Create a 3D scatter plot visualization of points with gradient coloring"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Extract x, y, z coordinates
    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])
    z = np.array([point[2] for point in points])
    
    # Calculate the centroid (actual center of the data points)
    center_x = np.mean(x)
    center_y = np.mean(y)
    center_z = np.mean(z)
    
    print(f"Calculated data centroid: ({center_x:.2f}, {center_y:.2f}, {center_z:.2f})")
    
    # Calculate distances from center
    distances = np.sqrt((x-center_x)**2 + (y-center_y)**2 + (z-center_z)**2)
    max_distance = np.max(distances)
    
    # Calculate relative distances (as percentage of max distance)
    relative_distances = distances / max_distance
    
    # Create two sets of points: 
    # 1. Core points (less than 70% distance from center)
    # 2. Outer points (70% or greater distance from center) - only show 50% of these
    
    core_indices = np.where(relative_distances < 0.7)[0]
    outer_indices = np.where(relative_distances >= 0.7)[0]
    
    # Randomly select 50% of the outer points
    selected_outer_indices = random.sample(list(outer_indices), k=len(outer_indices) // 3)
    
    print(f"Total points: {len(points)}")
    print(f"All contracts (inner radius): {len(core_indices)}")
    print(f"Most interacted L labelled (inner to outer radius): {len(outer_indices)}")
    # print(f"Selected outer points (50% of outer): {len(selected_outer_indices)}")
    
    # Plot core points with gradient coloring
    if len(core_indices) > 0:
        core_colors = distances[core_indices]
        scatter_core = ax.scatter(
            x[core_indices], y[core_indices], z[core_indices],
            c=core_colors, cmap=cm.viridis, marker='o', alpha=0.8, s=10
        )
        
    # Plot selected outer points in red
    if len(selected_outer_indices) > 0:
        scatter_outer = ax.scatter(
            x[selected_outer_indices], y[selected_outer_indices], z[selected_outer_indices],
            c='red', marker='o', alpha=0.8, s=10
        )
    
    # Add a color bar for the core points
    if len(core_indices) > 0:
        cbar = plt.colorbar(scatter_core, ax=ax, shrink=0.6, aspect=20)
        cbar.set_label(f'Distance from data centroid ({center_x:.2f}, {center_y:.2f}, {center_z:.2f})')
    
    # Set labels and title
    ax.set_xlabel('X Axis', fontsize=12)
    ax.set_ylabel('Y Axis', fontsize=12)
    ax.set_zlabel('Z Axis', fontsize=12)
    # ax.set_title('3D Visualization of Experiment Data Points', fontsize=14)
    
    # Set consistent axis limits to show the scale of the 1000x1000x1000 space
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    ax.set_zlim(0, 1000)
    
    # Calculate and display point statistics
    total_points = len(points)
    shown_points = len(core_indices) + len(selected_outer_indices)
    volume = 1000 * 1000 * 1000
    density = total_points / volume
    
    info_text = (
        f'Total points: {total_points} (Density: {density:.8f})\n'
        f'Shown points: {shown_points} ({shown_points/total_points*100:.1f}% of total)\n'
        f'Red points: {len(selected_outer_indices)} (≥70% distance from center)'
    )
    plt.figtext(0.02, 0.02, info_text)
    
    # Plot the centroid for reference
    ax.scatter([center_x], [center_y], [center_z], color='yellow', s=100, marker='*', edgecolor='black')
    
    # Add 3D grid for better depth perception
    ax.grid(True)
    
    # Add a legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=cm.viridis(0.5), 
               label='All contracts (inner radius)', markersize=8),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
               label='Labelled L (most interacted label) (inner to outer radius)', markersize=8),
        Line2D([0], [0], marker='*', color='w', markerfacecolor='yellow', 
               label='Centroid', markersize=12, markeredgecolor='black')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    return fig, ax

def visualize_2d_points(points):
    """Create a 2D scatter plot visualization of points using only X and Y coordinates"""
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111)
    
    # Extract x, y coordinates
    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])
    
    # Calculate the centroid (actual center of the X,Y data points)
    center_x = np.mean(x)
    center_y = np.mean(y)
    
    print(f"Calculated 2D data centroid: ({center_x:.2f}, {center_y:.2f})")
    
    # Calculate distances from center
    distances = np.sqrt((x-center_x)**2 + (y-center_y)**2)
    max_distance = np.max(distances)
    
    # Calculate relative distances (as percentage of max distance)
    relative_distances = distances / max_distance
    
    # Create two sets of points: 
    # 1. Core points (less than 70% distance from center)
    # 2. Outer points (70% or greater distance from center) - only show 50% of these
    
    core_indices = np.where(relative_distances < 0.7)[0]
    outer_indices = np.where(relative_distances >= 0.7)[0]
    
    # Randomly select 50% of the outer points
    selected_outer_indices = random.sample(list(outer_indices), k=len(outer_indices) // 2)
    
    print(f"2D Analysis - Total points: {len(points)}")
    print(f"2D Core points (<70% distance): {len(core_indices)}")
    print(f"2D Outer points (≥70% distance): {len(outer_indices)}")
    print(f"2D Selected outer points (50% of outer): {len(selected_outer_indices)}")
    
    # Plot core points with gradient coloring
    if len(core_indices) > 0:
        core_colors = distances[core_indices]
        scatter_core = ax.scatter(
            x[core_indices], y[core_indices],
            c=core_colors, cmap=cm.viridis, marker='o', alpha=0.8, s=20
        )
        
    # Plot selected outer points in red
    if len(selected_outer_indices) > 0:
        scatter_outer = ax.scatter(
            x[selected_outer_indices], y[selected_outer_indices],
            c='red', marker='o', alpha=0.8, s=20
        )
    
    # Add a color bar for the core points
    if len(core_indices) > 0:
        cbar = plt.colorbar(scatter_core, ax=ax, shrink=0.6, aspect=20)
        cbar.set_label(f'Distance from data centroid ({center_x:.2f}, {center_y:.2f})')
    
    # Set labels and title
    ax.set_xlabel('X Axis (0-5000)', fontsize=12)
    ax.set_ylabel('Y Axis (0-5000)', fontsize=12)
    ax.set_title('2D Visualization of Experiment Data Points (X-Y Plane)', fontsize=14)
    
    # Set consistent axis limits to show the scale as 5000x5000 space
    ax.set_xlim(0, 5000)
    ax.set_ylim(0, 5000)
    
    # Calculate and display point statistics
    total_points = len(points)
    shown_points = len(core_indices) + len(selected_outer_indices)
    area = 5000 * 5000
    density = total_points / area
    
    info_text = (
        f'Total points: {total_points} (2D Density: {density:.8f})\n'
        f'Shown points: {shown_points} ({shown_points/total_points*100:.1f}% of total)\n'
        f'Red points: {len(selected_outer_indices)} (≥70% distance from center)'
    )
    plt.figtext(0.02, 0.02, info_text)
    
    # Plot the centroid for reference
    ax.scatter([center_x], [center_y], color='yellow', s=200, marker='*', edgecolor='black')
    
    # Add grid for better readability
    ax.grid(True)
    
    # Add a legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=cm.viridis(0.5), 
               label='Core Points (<70% dist)', markersize=10),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
               label='Outer Points (≥70% dist)', markersize=10),
        Line2D([0], [0], marker='*', color='w', markerfacecolor='yellow', 
               label='Centroid', markersize=15, markeredgecolor='black')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    return fig, ax

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Load the data
    points = load_data('experiment.json')
    print(f"Loaded {len(points)} points from experiment.json")
    
    # Calculate bounds of the data
    x_min = min(point[0] for point in points)
    x_max = max(point[0] for point in points)
    y_min = min(point[1] for point in points)
    y_max = max(point[1] for point in points)
    z_min = min(point[2] for point in points)
    z_max = max(point[2] for point in points)
    
    print(f"Data bounds: X: {x_min}-{x_max}, Y: {y_min}-{y_max}, Z: {z_min}-{z_max}")
    
    # Create both visualizations
    fig_3d, ax_3d = visualize_3d_points(points)
    fig_2d, ax_2d = visualize_2d_points(points)
    
    # Show the visualizations
    plt.tight_layout()
    plt.show()