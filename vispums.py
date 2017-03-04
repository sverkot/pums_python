# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#CPSC-51100, Statistical Programming, Spring 2017
#Name :
#Programming Assignment 6 – Visualizing ACS PUMS Data
header ='''
CPSC-51100, Statistical Programming, Spring 2017
Name :
Programming Assignment 6 – Visualizing ACS PUMS Data
'''
print header
def draw_pie(ax):
    hhl = df['HHL'].value_counts()
    languages = ['English only','Spanish','Other Indo-European','Asian and Pacific Island languages','Other']
    ax.pie(hhl,startangle=242)
    ax.set_title('Household Languages',fontsize=8)
    ax.legend(languages,prop={'size':6},loc='upper left')
    ax.axis('equal')

def draw_hist(ax):
    hincp = df['HINCP']
    hincp.plot(kind='kde',color='k',ls='dashed')
    logspace = np.logspace(1,7,num=100,base=10.0)
    ax.hist(hincp,bins=logspace,facecolor='g',alpha=0.5,histtype='bar', normed=True)
    ax.set_title('Distribution of Household Income',fontsize=8)
    ax.set_xlabel('Household Income($)- Log Scaled',fontsize=8)
    ax.set_ylabel('Density',fontsize=8)
    ax.set_xscale("log")
    ax.set_axisbelow(True)
    ax.grid(color='gray', linestyle='dotted')

def draw_bar(ax):
    grouped = df.groupby('VEH')['WGTP'].sum()/1000
    ax.bar(grouped.index,grouped.values,width=0.9,bottom=None,color='r',align='center')
    ax.set_title('Vehicles Available in Households',fontsize=8)
    ax.set_xlabel('# of Vehicles',fontsize=8)
    ax.set_ylabel('Thousands of Households',fontsize=8)
    ax3.set_xticks(grouped.index)

def draw_scatter(ax):
    taxp = df['TAXP']
    tax_amount = convert_taxp_to_numeric(taxp)
    valp = df['VALP']
    ax.set_ylim([0, 11000])
    ax.set_xlim([0, 1200000])
    #scatter plot with the converted values of property tazxes taxp against valp, property values,
    #MRGP as marker color, WGTP as marker size
    mappable = ax.scatter(valp,tax_amount,s=df.WGTP/2,c=df.MRGP/2,cmap='seismic',alpha=0.05,marker = 'o')
    cbar = fig.colorbar(mappable, ax=ax)
    cbar.ax.tick_params(labelsize=5)
    cbar.set_label('First Mortgage Payment (Monthly $)',fontsize=8)
    ax.set_title('Property Taxes vs Property Values',fontsize=8)
    ax.set_ylabel('Taxes($)',fontsize=8)
    ax.set_xlabel('Property Value($)',fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=4)

def new_range(start, stop, step):
    tax_amount = []
    num_elements = int((stop-start)/float(step))
    for i in range(num_elements+1):
        tax_amount.append(start + i*step)
    return tax_amount

#function to convert the taxp code to a numeric value equivalent to it's dollar amount.
def convert_taxp_to_numeric(values):
    step_by_50 = new_range(0,1000,50)
    step_by_50 = pd.Series(step_by_50)
    step_by_50.index+=2
    step_by_100 = new_range(1000,5000,100)
    step_by_100 = pd.Series(step_by_100)
    step_by_100.index+=22
    step_by_1000 = new_range(6000,10000,1000)
    step_by_1000 = pd.Series(step_by_1000)
    step_by_1000.index+=64
    result = []
    for i in values:
        if i == 2:
            result.append(1)
        elif 3 <= i <= 22:
            if i in step_by_50.index:
                result.append(step_by_50[i])
        elif 23 <= i <= 62:
            if i in step_by_100.index:
                result.append(step_by_100[i])
        elif i == 63:
            result.append(5500)
        elif 64 <= i <= 68:
            if i in step_by_1000.index:
                result.append(step_by_1000[i])
        else:
            result.append(np.NaN)
    return result

#Get the PUMS dataset
pums = pd.read_csv('/Users/sverkot/projects/python_files/week6_assignment/ss13hil.csv')
#pums = pd.read_csv('ss13hil.csv')
df = pd.DataFrame(pums)

fig = plt.figure(facecolor='white')

#create subplots and call the functions to draw the pie chart,histogram,
#bar chart and scatter plot
ax1 = fig.add_subplot(2,2,1)
ax1.tick_params(axis='both', which='major', labelsize=6)
ax1.tick_params(axis='both', which='minor', labelsize=6)
draw_pie(ax1)

ax2 = fig.add_subplot(2,2,2)
draw_hist(ax2)
ax2.tick_params(axis='both', which='major', labelsize=6)
ax2.tick_params(axis='both', which='minor', labelsize=6)

ax3 = fig.add_subplot(2,2,3)
draw_bar(ax3)
ax3.tick_params(axis='both', which='major', labelsize=6)
ax3.tick_params(axis='both', which='minor', labelsize=6)

ax4 = fig.add_subplot(2,2,4)
draw_scatter(ax4)
ax4.tick_params(axis='both', which='major', labelsize=6)
ax4.tick_params(axis='both', which='minor', labelsize=6)

fig.tight_layout()
plt.show()
plt.savefig('pums.png',dpi=400,bbox_inches='tight',facecolor='white')
