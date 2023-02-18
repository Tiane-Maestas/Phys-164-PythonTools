from PhysicsUtils import Spectral

He_file = "TestData\He_1.txt"

he_spectra = Spectral.SpectralPlotter(He_file, title="Helium")
he_spectra.plot_centroids()
he_spectra.plot_spectrum()
he_spectra.show()
