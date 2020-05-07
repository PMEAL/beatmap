#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:26:18 2019

@author: ellsworthbell
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns
from beatmap import utils as util
from collections import namedtuple


def experimental_data_plot(df, file_name='dont_save'):
    """Creates a scatter plot of experimental data.

    Typical isotherm presentation where
    x-axis is relative pressure, y-axis is specific amount adsorbed.

    Parameters
    __________
    df : dataframe
        dataframe of imported experimental data

    file_name : str
        file name used to import .csv data, this function uses it to name the
        output .png file

    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """

    fig, (ax) = plt.subplots(1, 1, figsize=(13, 13))
    ax.plot(df.relp, df.n, c='grey', marker='o', linewidth=0)
    ax.set_xlim(-.05, 1.05)
    ax.set_title('Experimental Isotherm')
    ax.set_ylabel('n [mol/g]')
    ax.set_xlabel('P/Po')
    ax.grid(b=True, which='major', color='gray', linestyle='-')

    if file_name != 'do not save':
        fig.savefig('experimentaldata_%s.png' % (file_name[:-4]),
                    bbox_inches='tight')
        print('Experimental data plot saved as: experimentaldata_%s.png'
              % (file_name[:-4]))
    return()


def ssa_heatmap(df, bet_results, mask, file_name, gradient='Greens'):
    """Creates a heatmap of specific surface areas.

    Shading corresponds to specific surface area, normalized for the minimum
    and maximum spec sa values.

    Parameters
    __________
    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    bet_results : namedtuple
        bet_results is the named tuple returned from the bet function, containing all data
        required to check the validity of BET theory over all relative pressure intervals
        in this function the ssa element is used

    mask : array
        array of boolean values, returned from the rouq_mask function, used to mask
        invalid relative pressure ranges
    
    file_name : str
        file name used to import .csv data, this function uses it to name the
        output .png file

    gradient : string
        color gradient for heatmap

    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """

    if mask.all() == True:
        print('No valid relative pressure ranges. Specific surface area \
heatmap not created.')
        return

    #creating a masked array of ssa values
    ssa = np.ma.array(bet_results.ssa, mask=mask)

    # finding max and min sa to normalize heatmap colours
    ssamax, ssa_max_idx, ssamin, ssa_min_idx = util.max_min(ssa)
    hm_labels = round(df.relp * 100, 1)
    fig, ax = plt.subplots(1, 1, figsize=(13, 13))
    sns.heatmap(ssa, vmin=ssamin, vmax=ssamax, square=True, cmap=gradient,
                mask=(ssa == 0), xticklabels=hm_labels, yticklabels=hm_labels,
                linewidths=1, linecolor='w',
                cbar_kws={'shrink': .78, 'aspect': len(df.relp)})
    ax.invert_yaxis()
    ax.set_title('BET Specific Surface Area [m^2/g]')
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.xlabel('Start Relative Pressure')
    plt.yticks(rotation=45, horizontalalignment='right')
    plt.ylabel('End Relative Pressure')

    if file_name != 'do not save':
        fig.savefig('ssa_heatmap_%s.png' % (file_name[:-4]),
                    bbox_inches='tight')
        print('Specific surface area heatmap saved as: ssa_heatmap_%s.png'
              % (file_name[:-4]))
    return


def err_heatmap(df, bet_results, mask, file_name, gradient='Greys'):
    """Creates a heatmap of error values.

    Shading corresponds to theta, normalized for the minimum and maximum theta
    values, 0 = white
    Can be used to explore correlation between error in BET analysis and
    BET specific surface area

    Parameters
    __________
    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    bet_results : namedtuple
        bet_results is the named tuple returned from the bet function, containing all data
        required to check the validity of BET theory over all relative pressure intervals
        in this function the error element is used

    mask : array
        array of boolean values, returned from the rouq_mask function, used to mask
        invalid relative pressure ranges
    
    file_name : str
        file name used to import .csv data, this function uses it to name the
        output .png file

    gradient : string
        color gradient for heatmap

    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """

    if mask.all() == True:
        print('No valid relative pressure ranges. Error heat map not created.')
        return

    err = np.ma.array(bet_results.err, mask=mask)

    #creating a masked array of ssa values
    err = np.ma.array(bet_results.err, mask=mask)

    errormax, error_max_idx, errormin, error_min_idx = util.max_min(err)

    hm_labels = round(df.relp * 100, 1)
    fig, (ax) = plt.subplots(1, 1, figsize=(13, 13))
    sns.heatmap(err, vmin=0, vmax=errormax, square=True, cmap=gradient,
                mask=(err == 0), xticklabels=hm_labels, yticklabels=hm_labels,
                linewidths=1, linecolor='w',
                cbar_kws={'shrink': .78, 'aspect': len(df.relp)})
    ax.invert_yaxis()
    ax.set_title('BET Error Between Experimental and Theoretical Isotherms')
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.xlabel('Start Relative Pressure')
    plt.yticks(rotation=45, horizontalalignment='right')
    plt.ylabel('End Relative Pressure')

    if file_name != 'do not save':
        fig.savefig('error_heatmap_%s.png' % (file_name[:-4]),
                    bbox_inches='tight')
        print('Error heatmap saved as: error_heatmap_%s.png' %
              (file_name[:-4]))
    return


def bet_combo_plot(df, bet_results, mask, file_name):
    """Creates two BET plots, for the minimum and maxium error data sets.

    Only datapoints in the minimum and maximum error data sets are plotted
    Line is fit using scipy.stats.linregress
    Equation for best fit line and corresponding R value are annotated on plots
    Image is 2 by 1, two BET plots arranged horizontally in one image

    Parameters
    __________

    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    bet_results : namedtuple
        bet_results is the named tuple returned from the bet function, containing all data
        required to check the validity of BET theory over all relative pressure intervals
        in this function the error element is used

    mask : array
        array of boolean values, returned from the rouq_mask function, used to mask
        invalid relative pressure ranges

    file_name : str
        file name used to import .csv data, this function uses it to name the
        output .png file

    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """

    if mask.all() == True:
        print('No valid relative pressure ranges. BET combo plot not created.')
        return

    err = np.ma.array(bet_results.err, mask=mask)
    c = np.ma.array(bet_results.c, mask=mask)

    err_max, err_max_idx, err_min, err_min_idx = util.max_min(err)

    min_start = int(err_min_idx[1])
    min_stop = int(err_min_idx[0])
    max_start = int(err_max_idx[1])
    max_stop = int(err_max_idx[0])

    slope, intercept, r_value, p_value, std_err =\
        sp.stats.linregress(df.relp[min_start: min_stop + 1],
                            df.bet[min_start:min_stop + 1])

    min_liney = np.zeros(2)
    min_liney[0] = slope * (df.relp[min_start] - .01) + intercept
    min_liney[1] = slope * (df.relp[min_stop] + .01) + intercept
    min_linex = np.zeros(2)
    min_linex[0] = df.relp[min_start] - .01
    min_linex[1] = df.relp[min_stop] + .01

    figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    ax1.set_title('BET Plot - Data Points for Minimum Error C')
    ax1.set_xlim(min_linex[0]-.01, min_linex[1]+.01)
    ax1.set_ylabel('1/[n(1-Po/P)]')
    ax1.set_ylim(min_liney[0]*.9, min_liney[1]*1.1)
    ax1.set_xlabel('P/Po')
    ax1.grid(b=True, which='major', color='gray', linestyle='-')
    ax1.plot(df.relp[min_start:min_stop + 1], df.bet[min_start:min_stop + 1],
             label='Experimental Data', c='grey', marker='o', linewidth=0)
    ax1.plot(min_linex, min_liney, color='black', label='Linear Regression')
    ax1.legend(loc='upper left', framealpha=1)
    ax1.annotate('Linear Regression: \nm = %.3f \nb = %.3f \nR = %.3f'
                 % (slope, intercept, r_value),
                 bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                 textcoords='axes fraction', xytext=(.775, .018),
                 xy=(df.relp[min_stop], df.bet[min_start]), size=11)

    slope, intercept, r_value, p_value, std_err = \
        sp.stats.linregress(df.relp[max_start: max_stop + 1],
                            df.bet[max_start: max_stop + 1])
    max_liney = np.zeros(2)
    max_liney[0] = slope * (df.relp[max_start] - .01) + intercept
    max_liney[1] = slope * (df.relp[max_stop] + .01) + intercept
    max_linex = np.zeros(2)
    max_linex[0] = df.relp[max_start] - .01
    max_linex[1] = df.relp[max_stop] + .01

    ax2.set_title('BET Plot - Data Points for Maximum Error C')
    ax2.set_xlim(max_linex[0]-.01, max_linex[1]+.01)
    ax2.set_xlabel('P/Po')
    ax2.set_ylabel('1/[n(1-Po/P)]')
    ax2.set_ylim(max_liney[0]*.9, max_liney[1]*1.1)
    ax2.grid(b=True, which='major', color='gray', linestyle='-')
    ax2.plot(df.relp[max_start:max_stop + 1], df.bet[max_start:max_stop + 1],
             label='Experimental Data', c='grey', marker='o', linewidth=0)
    ax2.plot(max_linex, max_liney, color='black', label='Linear Regression')
    ax2.annotate('Linear Regression: \nm = %.3f \nb = %.3f \nR = %.3f'
                 % (slope, intercept, r_value),
                 bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                 textcoords='axes fraction', xytext=(.775, .018),
                 xy=(df.relp[max_stop], df.bet[max_start + 1]), size=11)

    if file_name != 'do not save':
        figure.savefig('betplot_%s.png' % (file_name[:-4]),
                       bbox_inches='tight')
        print('BET plot saved as: betplot_%s.png' % (file_name[:-4]))
    return


def bet_iso_combo_plot(df, bet_results, mask, file_name):
    """Creates an image to visually compare the "best" and "worst" values of C.

    Image is 4 by 4, with two "decomposed isotherm" plots on the top row
    and two BET plots on the bottom row.
    The x axis scale is kept constant on all plots
    so that data points map nicely.
    Only datapoints in the minimum and maximum error data sets are plotted
    Line is fit using scipy.stats.linregress
    Equation for best fit line and corresponding R value are annotated on plots
    See documentation for more information on this plot.

    Parameters
    __________

    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    bet_results : namedtuple
        bet_results is the named tuple returned from the bet function, containing all data
        required to check the validity of BET theory over all relative pressure intervals
        in this function the error element is used

    mask : array
        array of boolean values, returned from the rouq_mask function, used to mask
        invalid relative pressure ranges

    file_name : str
        file name used to import .csv data, this function uses it to name the
        output .png file

    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """

    if mask.all() == True:
        print('No valid relative pressure ranges. BET isotherm \
combo plot not created.')
        return

    ssa = np.ma.array(bet_results.ssa, mask=mask)
    nm = np.ma.array(bet_results.nm, mask=mask)
    c = np.ma.array(bet_results.c, mask=mask)
    err = np.ma.array(bet_results.err, mask=mask)

    err_max, err_max_idx, err_min, err_min_idx = util.max_min(err)
    c_max_err = c[err_max_idx[0], err_max_idx[1]]
    c_min_err = c[err_min_idx[0], err_min_idx[1]]

    nnm_min = nm[err_min_idx[0], err_min_idx[1]]
    nnm_max = nm[err_max_idx[0], err_max_idx[1]]
    ppo = np.arange(-.1, .9001, .001)
    nnm1 = 1 / (1 - ppo)
    nnm2_min = 1 / (1 + (c_min_err - 1) * ppo)
    nnm2_max = 1 / (1 + (c_max_err - 1) * ppo)
    synth_min = nnm1 - nnm2_min
    synth_max = nnm1 - nnm2_max
    expnnm_min = df.n / nnm_min
    err_min_i = int(err_min_idx[0] + 1)
    err_min_j = int(err_min_idx[1])
    expnnm_min_used = expnnm_min[err_min_j:err_min_i]
    ppo_expnnm_min_used = df.relp[err_min_j:err_min_i]
    expnnm_max = df.n / nnm_max
    err_max_i = int(err_max_idx[0] + 1)
    err_max_j = int(err_max_idx[1])
    expnnm_max_used = expnnm_max[err_max_j:err_max_i]
    ppo_expnnm_max_used = df.relp[err_max_j:err_max_i]

    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2,
                                               figsize=(20, 20))

    ax1.set_title('Isotherm as a composition of two equations, a and b - \
Minimum Error C')
    ax1.set_ylim(-1, synth_min[-2]+1)
    ax1.set_xlim(-.05, 1.05)
    ax1.set_ylabel('n/nm')
    ax1.set_xlabel('P/Po')
    ax1.grid(b=True, which='major', color='gray', linestyle='-')
    ax1.plot(ppo, nnm1, linestyle='--', linewidth=1, c='b',
             label='a = 1/(1-P/Po)')
    ax1.plot(ppo, nnm2_min, linestyle='--', linewidth=1, c='r',
             label='b = 1/(1+(c-1)(P/Po))')
    ax1.plot(ppo, synth_min, linestyle='-', linewidth=1, c='y',
             label='Theoretical isotherm', marker='')
    ax1.plot(ppo_expnnm_min_used, expnnm_min_used, c='grey',
             label='Experimental isotherm - used data',
             marker='o', linewidth=0)
    ax1.plot(df.relp, expnnm_min, c='grey', fillstyle='none',
             label='Experimental isotherm', marker='o', linewidth=0)
    ax1.plot([-.05, 1.05], [1, 1], c='grey', linestyle='-',
             linewidth=1, marker='')
    ax1.legend(loc='upper left', framealpha=1)

    ax2.set_title('Isotherm as a composition of two equations, a and b - \
Maximum Error C')
    ax2.set_ylabel('n/nm')
    ax2.set_xlabel('P/Po')
    ax2.set_ylim(-1, synth_max[-2] + 1)
    ax2.set_xlim(-.05, 1.05)
    ax2.grid(b=True, which='major', color='gray', linestyle='-')
    ax2.plot(ppo, nnm1, linestyle='--', linewidth=1, c='b',
             label='a = 1/(1-P/Po)')
    ax2.plot(ppo, nnm2_max, linestyle='--', linewidth=1, c='r',
             label='b = 1/(1+(c-1)(P/Po))')
    ax2.plot(ppo, synth_max, linestyle='-', linewidth=1, c='y',
             label='Theoretical isotherm', marker='')
    ax2.plot(ppo_expnnm_max_used, expnnm_max_used, c='grey',
             label='Experimental isotherm - used data',
             marker='o', linewidth=0)
    ax2.plot(df.relp, expnnm_max, c='grey', fillstyle='none',
             label='Experimental isotherm', marker='o', linewidth=0)
    ax2.plot([-.05, 1.05], [1, 1], c='grey', linestyle='-',
             linewidth=1, marker='')

    min_start = int(err_min_idx[1])
    min_stop = int(err_min_idx[0])
    max_start = int(err_max_idx[1])
    max_stop = int(err_max_idx[0])

    slope, intercept, r_value, p_value, std_err = \
        sp.stats.linregress(df.relp[min_start: min_stop + 1],
                            df.bet[min_start: min_stop + 1])
    min_liney = np.zeros(2)
    min_liney[0] = slope * (df.relp[min_start] - .01) + intercept
    min_liney[1] = slope * (df.relp[min_stop] + .01) + intercept
    min_linex = np.zeros(2)
    min_linex[0] = df.relp[min_start] - .01
    min_linex[1] = df.relp[min_stop] + .01
    ax3.set_title('BET Plot - Data Points for Minimum Error C')
    ax3.set_xlim(-.05, 1.05)
    ax3.set_ylim(min_liney[0]*.9, min_liney[1]*1.1)
    ax3.set_ylabel('1/[n(1-Po/P)]')
    ax3.set_xlabel('P/Po')
    ax3.grid(b=True, which='major', color='gray', linestyle='-')
    ax3.plot(df.relp[min_start:min_stop + 1], df.bet[min_start:min_stop + 1],
             label='Experimental Data', c='grey', marker='o', linewidth=0)
    ax3.plot(min_linex, min_liney, color='black', label='Linear Regression')
    ax3.legend(loc='upper left', framealpha=1)
    ax3.annotate('Linear Regression: \nm = %.3f \nb = %.3f \nR = %.3f'
                 % (slope, intercept, r_value),
                 bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                 textcoords='axes fraction', xytext=(.775, .018),
                 xy=(df.relp[min_stop], df.bet[min_start]), size=11)

    slope, intercept, r_value, p_value, std_err =\
        sp.stats.linregress(df.relp[max_start:max_stop + 1],
                            df.bet[max_start:max_stop + 1])
    max_liney = np.zeros(2)
    max_liney[0] = slope * (df.relp[max_start] - .01) + intercept
    max_liney[1] = slope * (df.relp[max_stop] + .01) + intercept
    max_linex = np.zeros(2)
    max_linex[0] = df.relp[max_start] - .01
    max_linex[1] = df.relp[max_stop] + .01

    ax4.set_title('BET Plot - Data Points for Maximum Error C')
    ax4.set_ylabel('1/[n(1-Po/P)]')
    ax4.set_xlabel('P/Po')
    ax4.set_xlim(-.05, 1.05)
    ax4.set_ylim(max_liney[0]*.9, max_liney[1]*1.1)
    ax4.grid(b=True, which='major', color='gray', linestyle='-')
    ax4.plot(df.relp[max_start:max_stop + 1], df.bet[max_start:max_stop + 1],
             label='Experimental Data', c='grey', marker='o', linewidth=0)
    ax4.plot(max_linex, max_liney, color='black', label='Linear Regression')
    ax4.annotate('Linear Regression: \nm = %.3f \nb = %.3f \nR = %.3f'
                 % (slope, intercept, r_value),
                 bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                 textcoords='axes fraction', xytext=(.775, .018),
                 xy=(df.relp[min_stop], df.bet[min_start]), size=11)

    if file_name != 'do not save':
        f.savefig('isothermcomp_%s.png' % (file_name[:-4]),
                  bbox_inches='tight')
        print('Isotherm decomposition plot saved as: isothermcomp_%s.png'
              % (file_name[:-4]))
    return
