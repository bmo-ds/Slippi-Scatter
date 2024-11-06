"""
Slippi Scatter

Takes a slippi file as an input and outputs an animated scatterplot in GIF, showing the players as
bubbles which take damage over time.

author: bmo-ds@github.com
date: June 2023

!!
Latest Python update breaks py-slippi package, the '__repr__' function in util.py needs to be fixed
with patch here: https://github.com/hohav/py-slippi/pull/49/files
!!
"""
import os
import glob
import numpy as np
import pandas as pd
from slippi import Game
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')


class SlippiScatter:
    def __init__(self, game=None, gif_title=None, temp_images_dir="Temp_images", figure_size=(8, 8), verbose=False):
        """Initializes class and set game, directories, plot size"""
        # Set directories and dataframe placeholder
        self.temp_images_dir = temp_images_dir  # where images will be temporarily stored
        self.df = None
        self.game = game
        self.gif_title = gif_title

        # Matplotlib settings
        self.figure_size = figure_size

        # Print to console
        self.verbose = verbose

    def create_gif(self):
        """Fetch frames, stitch together and save to GIF"""
        if self.verbose:
            print("Creating GIF...\n")
        frames = []
        images = glob.glob(f"{self.temp_images_dir}/*.png")
        for i in sorted(images, key=os.path.getmtime):
            new_frame = Image.open(i)
            frames.append(new_frame)

        if self.verbose:
            print("Saving to GIF...please wait \n")
        # Save to GIF (this can take some time depending on pc & game length
        frames[0].save(f"Output/{self.gif_title}.gif", format="GIF", append_images=frames[1:],
                       save_all=True, duration=30, loop=0)

        if self.verbose:
            print("Closing frames...\n")

        # Close the operation
        for frame in frames:
            frame.close()

        # Remove temp images
        self.remove_temp_files()

        if self.verbose:
            print("Process complete!\n")

    def create_images(self):
        """Go frame by frame and generate a scatter chart and drop into folder"""
        if self.verbose:
            print("Creating plots...\n")

        for row in self.df.index:
            if row % 2 != 0:  # skip every other frame or these files get big
                continue

            plt.figure(figsize=self.figure_size)

            p1_damage = (self.df.P1_damage.iloc[row]) ** 2 * np.e  # we want the damage bubbles to grow exp
            p2_damage = (self.df.P2_damage.iloc[row]) ** 2 * np.e  # we want the damage bubbles to grow exp

            plt.xlim(-180, 180)
            plt.ylim(-180, 180)

            plt.axhline(y=0, color="black", alpha=0.35)
            plt.axvline(x=0, color="black", alpha=0.35)

            # Get x, y
            x1, y1 = self.df.P1_x.iloc[row], self.df.P1_y.iloc[row]
            x2, y2 = self.df.P2_x.iloc[row], self.df.P2_y.iloc[row]

            x = [x1, x2]
            y = [y1, y2]

            # Plot connecting line
            plt.plot(x, y, linewidth=3.5, color='#7dfaa9', alpha=0.7, zorder=1)
            # Plot x, y
            plt.scatter(x1, y1, s=150, marker='o', c='#f689db', zorder=4)
            plt.scatter(x2, y2, s=150, marker='o', c='#4d7ff8', zorder=5)
            # Plot damage bubble
            plt.scatter(x1, y1, s=p1_damage, marker='o', c='#7de2fb', alpha=0.35, zorder=2)
            plt.scatter(x2, y2, s=p2_damage, marker='o', c='#f689db', alpha=0.35, zorder=3)
            # Set title
            plt.title(f"Frame {row}")
            plt.tight_layout()
            # Save to temp dir
            plt.savefig(f"{self.temp_images_dir}/{row}.png")
            plt.close()

        if self.verbose:
            print("Plotting complete...\n")

    def generate_dataframe(self):
        """Creates a dataframe with the x, y and damage % data"""
        if self.verbose:
            print("Creating dataframe...\n")
        # Create empty lists
        p1_xy = []
        p2_xy = []
        p1_damage = []
        p2_damage = []

        # Append data to lists
        for i, frame in enumerate(self.game.frames):
            # print(frame.ports)
            p1_xy.append(str(frame.ports[2].leader.pre.position))  # player 1 is index[2] but has changed in the past
            p2_xy.append(str(frame.ports[3].leader.pre.position))  # player 2 is index[3] but has changed in the past
            p1_damage.append(float(frame.ports[2].leader.pre.damage))
            p2_damage.append(float(frame.ports[3].leader.pre.damage))

        # Set into Dataframe
        df = pd.DataFrame(list(zip(p1_xy, p2_xy)), columns=["P1", "P2"])
        df.P1 = df.P1.apply(lambda x: x.replace('(', '').replace(')', ''))  # clean up brackets
        df.P2 = df.P2.apply(lambda x: x.replace('(', '').replace(')', ''))

        # Set position and damage data
        df["P1_x"] = df.P1.apply(lambda x: float(x.split(', ')[0]))
        df["P1_y"] = df.P1.apply(lambda x: float(x.split(', ')[1]))
        df["P2_x"] = df.P2.apply(lambda x: float(x.split(', ')[0]))
        df["P2_y"] = df.P2.apply(lambda x: float(x.split(', ')[1]))
        df["P1_damage"] = p1_damage
        df["P2_damage"] = p2_damage

        self.df = df

        if self.verbose:
            print(self.df.describe())
            print("Dataframe complete...\n")

    def remove_temp_files(self):
        """Clear the temp images directory after gif created"""
        files = glob.glob('Temp_images/*')
        for f in files:
            os.remove(f)

    def run_analysis(self, game="", verbose=False):
        """Main function to create and save gif"""
        if verbose:
            self.verbose = True

        # Check if game is set, else create game
        if not self.game:
            self.game = Game(game)

        # Create dataframe, images, save to gif
        self.generate_dataframe()
        self.create_images()
        self.create_gif()

    def set_game(self, slippi_file):
        """Sets the current game"""
        if self.verbose:
            print(f"Setting game: {slippi_file} \n")
        self.game = Game(slippi_file)


# Example
# Initialize class, run analysis
slsc = SlippiScatter(gif_title="zain_jmook_g4_Shine2022_GFs")
slsc.run_analysis(game="Slippi_Input/Stream-Game_20220828T225101.slp", verbose=True)

