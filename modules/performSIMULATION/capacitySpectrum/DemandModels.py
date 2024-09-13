#  # noqa: N999, D100
# Copyright (c) 2018 Leland Stanford Junior University
# Copyright (c) 2018 The Regents of the University of California
#
# This file is part of the SimCenter Backend Applications
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# You should have received a copy of the BSD 3-Clause License along with
# this file. If not, see <http://www.opensource.org/licenses/>.
#
# Contributors:
# Jinyan Zhao
# 
# References:
# 1. Cao, T., & Petersen, M. D. (2006). Uncertainty of earthquake losses due to 
# model uncertainty of input ground motions in the Los Angeles area. Bulletin of 
# the Seismological Society of America, 96(2), 365-376.
# 2. Steelman, J., & Hajjar, J. F. (2008). Systemic validation of consequence-based
# risk management for seismic regional losses.
# 3. Newmark, N. M., & Hall, W. J. (1982). Earthquake spectra and design. 
# Engineering monographs on earthquake criteria.
# 4. FEMA (2022), HAZUS – Multi-hazard Loss Estimation Methodology 5.0, 
# Earthquake Model Technical Manual, Federal Emergency Management Agency, Washington D.C.



import os
import sys
import time

import numpy as np
import pandas as pd

class demand_model_base:
    """
    A class to represent the base of demand models.
    
    Attributes:
    ----------
    T : numpy.ndarray
        Periods in the demand spectrum.
    dem_sd_05 : numpy.ndarray
        Spectrum displacement in the demand spectrum at 5% damping. In the unit of (inch)
    dem_sa_05 : numpy.ndarray
        Spectrum acceleration in the demand spectrum at 5% damping. In the unit of (g)
    
    Methods:
    -------
    """
    def __init__(self, T, dem_sd_05, dem_sa_05):
        self.T         = T
        self.dem_sd_05 = dem_sd_05
        self.dem_sa_05 = dem_sa_05

class HAZUS(demand_model_base):
    """
    A class to represent the design spectrum from HAZUS V5 (2022), section 4.1.3.2
    
    Attributes:
    ----------
    Tvd : float
        Tvd as HAZUS Eq. 4-4.
        Default value is 10 s as suggested by HAZUS (Below Eq. 4-4).
    Tav : float
        Tav as Cao and Peterson 2006. Figure A1.
    T : numpy.ndarray
        Periods in the demand spectrum.
    dem_sd_05 : numpy.ndarray
        Spectrum displacement in the demand spectrum at 5% damping. In the unit of (inch)
    dem_sa_05 : numpy.ndarray
        Spectrum acceleration in the demand spectrum at 5% damping. In the unit of (g)
    
    Methods:
    -------
    """
    def __init__(self, Mw = 7.0):
        self.Tvd = np.power(10, (Mw - 5)/2)
        self.T  = [0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 
                                   0.25, 0.3, 0.4, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 7.5, 10]
        self.Mw = Mw
    
    def set_IMs(self, sa_03, sa_10):
        self.sa_03 = sa_03
        self.sa_10 = sa_10
        self.Tav = sa_10/sa_03
        self.g = 386
        # insert tvd and tav in self.T
        self.T.append(self.Tvd)
        self.T.append(self.Tav)
        self.T = np.sort(self.T)
        self.dem_sd_05 = np.zeros_like(self.T)
        self.dem_sa_05 = np.zeros_like(self.T)
        ## Eq A1a to Eq A2c in Cao and Peterson 2006
        for i, t in enumerate(self.T):
            if t <= self.Tav:
                self.dem_sa_05[i] = sa_03
                self.dem_sd_05[i] = self.g/(4 * np.pi**2) * t**2 * self.dem_sa_05[i] # Eq. A2
            elif t <= self.Tvd:
                self.dem_sa_05[i] = sa_10/t
                self.dem_sd_05[i] = self.g/(4 * np.pi**2) * t**2 * self.dem_sa_05[i] # Eq. A2
            else:
                self.dem_sa_05[i] = sa_10 * self.Tvd / t**2 # Ea. A1a
                self.dem_sd_05[i] = self.g/(4 * np.pi**2) * t**2 * self.dem_sa_05[i]  

    def get_sa(self, T):
        # return np.interp(T, self.T, self.dem_sa_05)
        if T <= self.Tav:
            return self.sa_03
        elif T <= self.Tvd:
            return self.sa_10/T
        else:
            return self.sa_10 * self.Tvd / T**2
    
    def get_sd(self, T):
        # return np.interp(T, self.T, self.dem_sd_05)
        # return np.interp(T, self.T, self.dem_sa_05)
        if T <= self.Tav:
            return self.get_sd_from_sa(self.sa_03, T)
        elif T <= self.Tvd:
            return self.get_sd_from_sa(self.sa_10/T, T)
        else:
            return self.get_sd_from_sa(self.sa_10 * self.Tvd / T**2, T)
        
    def get_sd_from_sa(self, sa, T):
        return self.g/(4 * np.pi**2) * T**2 * sa
    
    def set_Tavb(self, damping_model, tol = 0.05, max_iter = 100):
        x_prev = 5 # Start with 5% damping
        for i in range(max_iter):
            beta = x_prev
            ra = 2.12/(3.21-0.68*np.log(beta))
            Tavb = self.Tav * (2.12/(3.21-0.68*np.log(beta)))/(1.65/(2.31-0.41*np.log(beta)))
            sa = self.get_sa(Tavb) / ra
            sd = self.get_sd_from_sa(sa, Tavb)
            beta_eff = damping_model.get_beta(sd, sa)
            x_next = beta_eff
            if np.abs(x_next - x_prev) < tol:
                self.Tavb = self.Tav * (2.12/(3.21-0.68*np.log(beta_eff)))/(1.65/(2.31-0.41*np.log(beta_eff)))
                break
            x_prev = x_next
        if (getattr(self, 'Tavb', None) is None or (3.21-0.68*np.log(beta_eff)) < 0
            or 2.12/(3.21-0.68*np.log(beta)) < 1):
            # raise a warning
            # print('WARNING: in HAZUS demand model, the Tavb is not converged.')
            self.Tavb = self.Tav 


    def set_beta_tvd(self, damping_model, tol = 0.05, max_iter = 100):
        x_prev = 5 # Start with 5% damping
        max_iter = 100
        tol = 0.05
        for i in range(max_iter):
            beta = x_prev
            Tvd = self.Tvd
            rd = 1.65/(2.31-0.41*np.log(beta))
            sa = self.get_sa(Tvd)/rd
            sd = self.get_sd_from_sa(sa, Tvd)
            beta_eff = damping_model.get_beta(sd, sa)
            x_next = beta_eff
            if np.abs(x_next - x_prev) < tol:
                self.beta_tvd = x_next
                break
            x_prev = x_next
        if (getattr(self, 'beta_tvd', None) is None or (2.31-0.41*np.log(self.beta_tvd)) < 0
            or 1.65/(2.31-0.41*np.log(self.beta_tvd)) < 1):
            # raise a warning
            # print('WARNING: in HAZUS demand model, the beta_tvd is not converged.')
            self.beta_tvd = -1 # This will be overwritten in get_reduced_demand.


    def get_reduced_demand(self, beta_eff):
        if getattr(self, 'Tavb', None) is None:
            raise ValueError('The Tavb is not set yet.')
        if getattr(self, 'beta_tvd', None) is None:
            raise ValueError('The beta_tvd is not set yet.')
        RA = 2.12/(3.21-0.68*np.log(beta_eff))
        Rv = 1.65/(2.31-0.41*np.log(beta_eff))
        if self.beta_tvd < 0:
            RD = 1.39/(1.82 - 0.27 * np.log(beta_eff)) # EQ A9 in Cao and Peterson 2006
        else:
            RD = (1.65/(2.31-0.41*np.log(self.beta_tvd)))
        dem_sa = np.zeros_like(np.array(self.T))
        dem_sd = np.zeros_like(np.array(self.T))
        for i, t in enumerate(self.T):
            if t <= self.Tavb:
                dem_sa[i] = self.get_sa(t) / RA
                dem_sd[i] = self.get_sd_from_sa(dem_sa[i], t)
            elif t <= self.Tvd:
                dem_sa[i] = self.get_sa(t) / Rv
                dem_sd[i] = self.get_sd_from_sa(dem_sa[i], t)
            else:
                dem_sa[i] = self.get_sa(t) / RD
                dem_sd[i] = self.get_sd_from_sa(dem_sa[i], t)
        return dem_sd, dem_sa
        
    
    def set_ruduction_factor(self, beta_eff):
        if getattr(self, 'Tavb', None) is None:
            raise ValueError('The Tavb is not set yet.')
        self.RA = 2.12/(3.21-0.68*np.log(beta_eff))
        self.Rv = 1.65/(2.31-0.41*np.log(beta_eff))
        self.RD = (1.65/(2.31-0.41*np.log(beta_eff)))    
        
    # def __init__(self, sa_03, sa_10, Mw = 7.0):
    #     self.Tvd = np.power(10, (Mw - 5)/2)
    #     self.Tav = sa_10/sa_03
    #     g = 386 
    #     # self.T is defined as typical GMPEs
    #     self.T  = [0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 
    #                                0.25, 0.3, 0.4, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 7.5, 10]
    #     # insert tvd and tav in self.T
    #     self.T.append(self.Tvd)
    #     self.T.append(self.Tav)
    #     self.T = np.sort(self.T)
    #     self.dem_sd_05 = np.zeros_like(self.T)
    #     self.dem_sa_05 = np.zeros_like(self.T)
    #     ## Eq A1a to Eq A2c in Cao and Peterson 2006
    #     for i, t in enumerate(self.T):
    #         if t <= self.Tav:
    #             self.dem_sa_05[i] = sa_03
    #             self.dem_sd_05[i] = g/(4 * np.pi**2) * t**2 * self.dem_sa_05[i] # Eq. A2
    #         elif t <= self.Tvd:
    #             self.dem_sa_05[i] = sa_10/t
    #             self.dem_sd_05[i] = g/(4 * np.pi**2) * t**2 * self.dem_sa_05[i] # Eq. A2
    #         else:
    #             self.dem_sa_05[i] = sa_10 * self.Tvd / t**2 # Ea. A1a
    #             self.dem_sd_05[i] = g/(4 * np.pi**2) * t**2 * self.dem_sa_05[i] 
    #     self.Mw = Mw
    
    def name(self):
        return 'HAZUS'
    
    @staticmethod
    def check_IM(IM_header):
        if 'SA_0.3' not in IM_header:
            raise ValueError('The IM header should contain SA_0.3')
        if 'SA_1.0' not in IM_header:
            raise ValueError('The IM header of should contain SA_1.0')

class HAZUS_lin_chang_2003(HAZUS):
    """
    A class to represent the design spectrum from HAZUS V5 (2022), and the
    damping deduction relationship from Lin and Chang 2003.
    """
    def __init__(self, Mw = 7.0):
        super().__init__(Mw)
    def name(self):
        return "HAZUS_lin_chang_2003"
    def get_dmf(self, beta_eff, T):
        alpha = 1.303+0.436*np.log(beta_eff)
        R     = 1-alpha*T**0.3/(T+1)**0.65
        return R
    def get_reduced_demand(self, beta_eff):
        if getattr(self, 'Tavb', None) is None:
            raise ValueError('The Tavb is not set yet.')
        if getattr(self, 'beta_tvd', None) is None:
            raise ValueError('The beta_tvd is not set yet.')
        dem_sa = np.zeros_like(np.array(self.T))
        dem_sd = np.zeros_like(np.array(self.T))
        for i, t in enumerate(self.T):
            R = self.get_dmf(beta_eff, t)
            if t <= self.Tavb:
                dem_sa[i] = self.get_sa(t) / R
                dem_sd[i] = self.get_sd_from_sa(dem_sa[i], t)
            elif t <= self.Tvd:
                dem_sa[i] = self.get_sa(t) / R
                dem_sd[i] = self.get_sd_from_sa(dem_sa[i], t)
            else:
                dem_sa[i] = self.get_sa(t) / R
                dem_sd[i] = self.get_sd_from_sa(dem_sa[i], t)
        return dem_sd, dem_sa

class ASCE_7_10(demand_model_base):
    """
    A class to represent the design spectrum from ASCE_7_10.
    
    Attributes:
    ----------
    Tvd : float
        Tvd as HAZUS Eq. 4-4.
    Tav : float
        Tav as Cao and Peterson 2006. Figure A1.
    T : numpy.ndarray
        Periods in the demand spectrum.
    dem_sd_05 : numpy.ndarray
        Spectrum displacement in the demand spectrum at 5% damping. In the unit of (inch)
    dem_sa_05 : numpy.ndarray
        Spectrum acceleration in the demand spectrum at 5% damping. In the unit of (g)
    
    Methods:
    -------
    """
    
    def __init__(self, T, dem_sd_05, dem_sa_05):
        self.T         = T
        self.dem_sd_05 = dem_sd_05
        self.dem_sa_05 = dem_sa_05

