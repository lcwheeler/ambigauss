API Design
==========

Base Model
----------

.. code-block:: python

  model = GaussianFitter(n_peaks=2)

  df = pd.DataFrame({
    'x' : [0, 1, 2],
    'y' : [0, 10, 50],
    'y2': [0, 5, 10]
  })

  model.fit(x=df.x, y=df.y)


  model.score()

  model.centers
  model.widths
  model.heights

  model.plot()



Gaussian spectrum
-----------------

.. code-block:: python

  # Import gaussian
  from ambigauss import GaussianSpectrum

  # Initialize a model.
  m = GaussianSpectrum(n_peaks=3)

  # Fit data.
  m.fit(x, y)

  # Plot data
  m.plot()

  # Print parameters
  m.print_parameters()


Voigt spectrum
--------------

.. code-block:: python

  # Import gaussian
  from ambigauss import VoigtSpectrum

  # Initialize a model.
  m = VoigtSpectrum(n_peaks=3)

  # Fit data.
  m.fit(x, y)

  # Plot data
  m.plot()

  # Print parameters
  m.print_parameters()
