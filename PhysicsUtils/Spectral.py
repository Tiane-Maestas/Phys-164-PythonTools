"""This module is a collection of every tool I've made for processing 'Spectral' data."""
import numpy as np
import matplotlib.pyplot as plt
import copy as cp

def Test():
    print("Here")

class SpectralPlotter:

    def __init__(self, data_file, **options) -> None:
        """Initialize Spectral data as pixel # and intensity from a given 'data_file'."""
        options = SpectralPlotter.process_optional_params(options)
        self.buffer = options[0]
        self.title = options[1]

        pix, int = np.genfromtxt(data_file, usecols = [0, 1], unpack = True, invalid_raise = False)
        pix = pix[~np.isnan(pix)] # Remove nan
        int = int[~np.isnan(int)] # Remove nan

        self.pixel_data = np.array(pix)
        self.intensity_data = np.array(int)

    def get_a_centroid_domin(self, max_value = None):
        """This will give a domain around the max intensity and the avearge location of the centroid."""
        # First get index of max_value
        if max_value == None:
            max_value = max(self.intensity_data)

        max_location_index = np.where(self.intensity_data == max_value)[0][0]
        working_domain = [max_location_index - self.buffer, max_location_index + self.buffer]
        
        # Use centroid Equation
        average_location = np.sum(self.pixel_data[working_domain[0]:working_domain[1]] * self.intensity_data[working_domain[0]:working_domain[1]]) / np.sum(self.intensity_data[working_domain[0]:working_domain[1]])

        return [working_domain[0], working_domain[1], average_location]
    
    def order_centroid_locations(self, n):
        """This will return y sorted from max to min with n centroid locations."""
        tmp = cp.deepcopy(self.intensity_data)
        self.max_intensity_ordered = np.array([])
        
        for i in range(n):
            self.max_intensity_ordered = np.append(self.max_intensity_ordered, max(tmp))
            init = np.where(tmp == max(tmp))[0][0] - self.buffer
            fini = np.where(tmp == max(tmp))[0][0] + self.buffer
            tmp = np.delete(tmp, range(init, fini))

        return self.max_intensity_ordered
    
    def plot_centroids(self, n=3):
        """This will plot the top 'n' centroids. It returns a list of each centroid average location (Pixel #)."""
        fig, ax = plt.subplots(n, figsize=(10, 10)) # Make plots for each centroid + combined plot.
        
        self.order_centroid_locations(n) # Get all n centroid locations.
        
        self.centroid_locations = np.array([]) # Pixel #s of centroids.

        for i in range(n):
            current_domain = self.get_a_centroid_domin(max_value=self.max_intensity_ordered[i])
            self.centroid_locations = np.append(self.centroid_locations, current_domain[2])
            
            # Plot individual centroids zoomed in.
            ax[i].plot(self.pixel_data, self.intensity_data)
            ax[i].set_xlim(self.pixel_data[current_domain[0]], self.pixel_data[current_domain[1]])
            ax[i].axvline(current_domain[2], color='red')
            ax[i].set_xlabel('Pixel # (' + str(current_domain[2]) + ')')
            ax[i].set_ylabel('Intensity')
            ax[i].set_title(self.title + " " + str(i + 1))


        plt.tight_layout() # This makes proper spacing.
        
        return self.centroid_locations
    
    def plot_spectrum(self):
        """This will plot the entire spectrum."""
        fig, ax = plt.subplots(1, figsize=(10, 5))
        # Plot the whole spectrum.
        ax.plot(self.pixel_data, self.intensity_data)
        # Make a line at each peek represented here.
        for location in self.centroid_locations:
            ax.axvline(location, color='red')
        ax.set_xlabel('Pixel #')
        ax.set_ylabel('Intensity')
        ax.set_title('Total Spectrum of ' + self.title)
    
    def show(self):
        plt.show()

    @staticmethod
    def process_optional_params(options):
        """This will return a list of all the optional paramater values. [buffer, title]"""
        return_list = [10, ""]
        for key, value in options.items(): # Process optional paramaters.
            if key == "buffer":
                return_list[0] = value
            elif key == "title":
                return_list[1] = value
        return return_list