---
title: Scoring Tools documentation
viewport: 'width=device-width, initial-scale=0.9, maximum-scale=0.9'
...

<div class="document">

<div class="documentwrapper">

<div class="bodywrapper">

<div class="body" role="main">

<div id="module-scoringtools" class="section">

<span id="welcome-to-scoring-tools-documentation"></span>
Welcome to Scoring Tools’ documentation![¶](#module-scoringtools "Permalink to this headline"){.headerlink}
===========================================================================================================

This module is a interface for some functionality of the R-package
scoringRules. It is possible to calculate various scores for ensemble
predictions. Namely the Continuous Ranked Probability Score (CRPS), the
energy score and the variogram score.

 `scoringtools.`{.descclassname}`crps_sample`{.descname}<span class="sig-paren">(</span>*y*, *dat*<span class="sig-paren">)</span>[¶](#scoringtools.crps_sample "Permalink to this definition"){.headerlink}

:   Sample Continuous Ranked Probability Score (CRPS)

    This function calculates the CRPS for a given pair of
    observation (y) and ensemble prediction (dat). The observation y is
    considered to be univariate.

    Args:

    :   y (float): Univariate observation.

        dat (np.array): Ensemble prediction for value y of length m
        which is the number of ensemble members.

    Returns:
    :   float: Returns the variogram score of the
        forecast-observation pair.

<!-- -->

 `scoringtools.`{.descclassname}`crps_sample_vec`{.descname}<span class="sig-paren">(</span>*y\_vec*, *dat\_mat*<span class="sig-paren">)</span>[¶](#scoringtools.crps_sample_vec "Permalink to this definition"){.headerlink}

:   Sample Continuous Ranked Probability Score (CRPS); vectorized
    version

    This function calculates the CRPS for a given pair of a series of
    observations (y\_vec) and corresponding ensemble
    predictions (dat\_mat). The data in y\_vec is considered to be a
    series of univariate observations.

    Args:

    :   y\_vec (np.array): Series of multivariate observations of length
        n which is the number of observations.

        dat\_mat (np.array): Ensemble prediction for the values y\_vec
        containing m times n values where m is the number of
        ensemble members.

    Returns:
    :   float: Returns the CRPS of the forecast-observation series.

<!-- -->

 `scoringtools.`{.descclassname}`es_sample`{.descname}<span class="sig-paren">(</span>*y*, *dat*<span class="sig-paren">)</span>[¶](#scoringtools.es_sample "Permalink to this definition"){.headerlink}

:   Sample Energy Score

    This function calculates the energy score for a given pair of
    observation (y) and ensemble prediction (dat). The observation y is
    considered to be multivariate.

    Args:

    :   

        y (np.array): Multivariate observation of length d greater 
        :   than 1.

        dat (np.array): Ensemble prediction for value y containing d
        times m values, where m is the number of ensemble members.

    Returns:
    :   float: Returns the energy score of the
        forecast-observation pair.

<!-- -->

 `scoringtools.`{.descclassname}`es_sample_vec`{.descname}<span class="sig-paren">(</span>*y\_mat*, *dat\_mat*<span class="sig-paren">)</span>[¶](#scoringtools.es_sample_vec "Permalink to this definition"){.headerlink}

:   Sample Energy Score; vectorized version

    This function calculates the energy score for a given pair of a
    series of observations (y\_mat) and corresponding ensemble
    predictions (dat\_mat). The data in y\_mat is considered to be a
    series of multivariate observations.

    Args:

    :   y\_mat (np.array): Series of multivariate observations of
        dimension d times n. Where d is the dimension of the
        multivariate observation and n the number of observations.

        dat (np.array): Ensemble prediction for the values y\_mat
        containing d times m times n values where m is the number of
        ensemble members.

    Returns:
    :   float: Returns the energy score of the
        forecast-observation series.

<!-- -->

 `scoringtools.`{.descclassname}`vs_sample`{.descname}<span class="sig-paren">(</span>*y*, *dat*<span class="sig-paren">)</span>[¶](#scoringtools.vs_sample "Permalink to this definition"){.headerlink}

:   Sample Variogram Score

    This function calculates the variogram score for a given pair of
    observation (y) and ensemble prediction (dat). The observation y is
    considered to be multivariate.

    Args:

    :   

        y (np.array): Multivariate observation of length d greater 
        :   than 1.

        dat (np.array): Ensemble prediction for value y containing d
        times m values, where m is the number of ensemble members.

    Returns:
    :   float: Returns the variogram score of the
        forecast-observation pair.

<!-- -->

 `scoringtools.`{.descclassname}`vs_sample_vec`{.descname}<span class="sig-paren">(</span>*y\_mat*, *dat\_mat*<span class="sig-paren">)</span>[¶](#scoringtools.vs_sample_vec "Permalink to this definition"){.headerlink}

:   Sample Variogram Score; vectorized version

    This function calculates the Energy score for a given pair of a
    series of observations (y\_mat) and corresponding ensemble
    predictions (dat\_mat). The data in y\_mat is considered to be a
    series of multivariate observations.

    Args:

    :   y\_mat (np.array): Series of multivariate observations of
        dimension d times n. Where d is the dimension of the
        multivariate observation and n the number of observations.

        dat (np.array): Ensemble prediction for the values y\_mat
        containing d times m times n values where m is the number of
        ensemble members.

    Returns:
    :   float: Returns the variogram score of the
        forecast-observation series.

</div>

</div>

</div>

</div>

<div class="sphinxsidebar" role="navigation"
aria-label="main navigation">

<div class="sphinxsidebarwrapper">

[Scoring Tools](index.html#document-index) {#scoring-tools .logo}
==========================================

### Navigation

<div class="relations">

### Related Topics

-   [Documentation overview](index.html#document-index)

</div>

</div>

</div>

<div class="clearer">

</div>

</div>

<div class="footer">

©2017, Manuel Klar. | Powered by [Sphinx 1.6.3](http://sphinx-doc.org/)
& [Alabaster 0.7.10](https://github.com/bitprophet/alabaster)

</div>
