import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import imageio

# Load your CSV file
df = pd.read_csv('out_data/jack.csv')

# Sort by frame_number
df.sort_values('frame_number', inplace=True)


def plot_point_cloud(frame_df):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot points with color based on SNR
    sc = ax.scatter(frame_df['x'], frame_df['y'], frame_df['z'], c=frame_df['snr'], cmap='viridis')
    
    # Set axis limits to ensure consistency across frames
    ax.set_xlim(df['x'].min(), df['x'].max())
    ax.set_ylim(df['y'].min(), df['y'].max())
    ax.set_zlim(df['z'].min(), df['z'].max())
    
    # Add colorbar
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label('SNR')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.view_init(elev=90, azim=0)

    return fig, ax

output_directory = 'frames'
os.makedirs(output_directory, exist_ok=True)

frames = []
for frame_number, frame_df in df.groupby('frame_number'):
    fig, ax = plot_point_cloud(frame_df)
    plt.savefig(f'{output_directory}/frame_{frame_number:04d}.png')
    plt.close()
    frames.append(f'{output_directory}/frame_{frame_number:04d}.png')


output_gif = 'point_cloud_animation.gif'
imageio.mimsave(output_gif, [imageio.imread(frame) for frame in frames], duration=5)
