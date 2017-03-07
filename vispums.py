# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Pie chart containing the number of household records for different values of the HHL (household language) attribute.
def draw_pie(ax):
    hhl = df['HHL'].value_counts()
    languages = ['English only','Spanish','Other Indo-European','Asian and Pacific Island languages','Other']
    ax.pie(hhl,startangle=242)
    ax.set_title('Household Languages',fontsize=8)
    ax.legend(languages,prop={'size':6},bbox_to_anchor=(0,0.95),loc='upper left',bbox_transform=fig.transFigure)
    ax.axis('equal')

#Histogram of HINCP (household income) with KDE plot superimposed.
def draw_hist(ax):
    hincp = df['HINCP']
    hincp.plot(kind='kde',color='k',ls='dashed')
    #log scale on the x-axis with log-spaced bins
    logspace = np.logspace(1,7,num=100,base=10.0)
    ax.hist(hincp,bins=logspace,facecolor='g',alpha=0.5,histtype='bar', normed=True)
    ax.set_title('Distribution of Household Income',fontsize=8)
    ax.set_xlabel('Household Income($)- Log Scaled',fontsize=8)
    ax.set_ylabel('Density',fontsize=8)
    ax.set_xscale("log")
    ax.set_axisbelow(True)
    ax.grid(color='gray', linestyle='dotted')
#Bar chart of Thousands of Households for each VEH (vehicles available) value
def draw_bar(ax):
    #use the WGTP value to count how many households are represented by each household record and divide the sum by 1000
    grouped = df.groupby('VEH')['WGTP'].sum()/1000
    ax.bar(grouped.index,grouped.values,width=0.9,bottom=None,color='r',align='center')
    ax.set_title('Vehicles Available in Households',fontsize=8)
    ax.set_xlabel('# of Vehicles',fontsize=8)
    ax.set_ylabel('Thousands of Households',fontsize=8)
    ax.set_xticks(grouped.index)
#Scatter plot of TAXP (property taxes) vs. VALP (property value)
def draw_scatter(ax):
    taxp = df['TAXP']
    tax_amount = convert_taxp(taxp)
    valp = df['VALP']
    ax.set_ylim([0, 11000])
    ax.set_xlim([0, 1200000])
    #scatter plot with the converted values of property tazxes taxp against valp, property values,
    #MRGP as marker color, WGTP as marker size
    mappable = ax.scatter(valp,tax_amount,s=df.WGTP/2,c=df.MRGP,cmap='seismic',alpha=0.15,marker = 'o')
    cbar = fig.colorbar(mappable, ax=ax)
    cbar.ax.tick_params(labelsize=5)
    cbar.set_label('First Mortgage Payment (Monthly $)',fontsize=8)
    ax.set_title('Property Taxes vs Property Values',fontsize=8)
    ax.set_ylabel('Taxes($)',fontsize=8)
    ax.set_xlabel('Property Value($)',fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=4)

#create a dictionary to map taxp values to tax amount in $
def get_taxp_mapping_dict():
    taxp_dict = {}
    taxp_dict[1] = np.NaN
    taxp_dict[2] = 1
    taxp_dict[63]=5500
    counter = 50
    for key in range (3,23):
        taxp_dict[key]=counter
        counter += 50
    for key in range (23,63):
        taxp_dict[key] = counter+50
        counter += 100
    counter = counter - 50
    for key in range (64,69):
        taxp_dict[key] = counter+1000
        counter += 1000
    return taxp_dict

#function to convert the taxp code to a numeric value equivalent to it's dollar amount.
def convert_taxp(taxp):
    tax_amount = []
    taxp_dict = get_taxp_mapping_dict()
    for i in taxp:
        if taxp_dict.has_key(i):
            tax_amount.append(taxp_dict[i])
        else:
            tax_amount.append(np.NaN)
    return tax_amount

#Get the PUMS dataset
pums = pd.read_csv('ss13hil.csv')
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
#save the figure
plt.savefig('pums.png',dpi=400,bbox_inches='tight',facecolor='white')
