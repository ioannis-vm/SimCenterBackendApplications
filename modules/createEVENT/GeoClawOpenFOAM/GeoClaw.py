#!/usr/bin/env python
# LICENSING INFORMATION
####################################################################
"""LICENSE INFORMATION:

Copyright (c) 2020-2030, The Regents of the University of California (Regents).

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
        list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the authors and should not be interpreted as representing official policies, either expressed or implied, of the FreeBSD Project.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

"""  # noqa: D400
####################################################################
# AUTHOR INFORMATION
####################################################################
# 2020 - 2021: Ajay B Harish (ajaybh@berkeley.edu)

####################################################################
# Import all necessary modules
####################################################################
# Standard python modules
import os

import numpy as np

# Other custom modules
from hydroUtils import hydroUtils


####################################################################
# OpenFOAM7 solver class
####################################################################
class GeoClaw:
    """This class includes the methods related to
    coupling GeoClaw and OpenFOAM in HydroUQ

    Methods
    -------
            decomptext: Get all the text for the decomposeParDict

    """  # noqa: D205, D400, D404

    #############################################################
    def creategeom(self, data, path):
        """Creates the geometry for bathymetry

        Arguments:
        ---------
                data: all the JSON data

        """  # noqa: D400, D401
        # Create a utilities object
        hydroutil = hydroUtils()

        # Get information about the interface
        swcfdfile = ', '.join(
            hydroutil.extract_element_from_json(data, ['Events', 'SWCFDInteFile'])
        )
        swcfdfilepath = os.path.join(path, swcfdfile)  # noqa: PTH118
        swcfdpoints = np.genfromtxt(
            swcfdfilepath, delimiter=',', dtype=(float, float)
        )

        # Add extremum to the constants file
        maxvalues = np.max(swcfdpoints, axis=0)
        minvalues = np.min(swcfdpoints, axis=0)

        # Points of interest
        bottompts = self.getbathy(maxvalues, minvalues, data)  # noqa: F841

        return 0  # noqa: DOC201, RUF100
