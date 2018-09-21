import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib import interactive


colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'limegreen',
          'red', 'navy', 'blue', 'magenta', 'crimson']
explode = (0.01, 0.01, 0.01, 0.01, 0.01)
labels = 'Not Parallelable', 'GPU Optimizable', 'CPU Optimizable', 'Vector Optimizable', 'Not Optimizable'
sizes = [0, 0, 0,0,0]
sizesOrignal = [15, 20, 45, 10,10]
fig = plt.figure()
ax = plt.subplot(2, 2, 1)

def updatePie(num):
    ax.clear()
    ax.axis('equal')
    ax.set_title('Loop Sections Breakdown')
    for sizeVal in range (0,5):
        if sizes[sizeVal]<sizesOrignal[sizeVal]:
            sizes[sizeVal] = sizes[sizeVal] +4
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)

ani = FuncAnimation(fig, updatePie, frames=range(100), repeat=False)
interactive(True)
plt.show()

objects = ('Section1', 'Section2', 'Section3', 'Section4', 'Section5', 'Section6')
y_pos = np.arange(len(objects))
performanceSet1 = [0,0,0,0,0,0]
originalPerformanceSet1 = [10,8,6,4,2,1]
performanceSet2 = [0,0,0,0,0,0]
originalPerformanceSet2 = [12,6,7,3,6,2]
axBar = plt.subplot(2, 2, 2)


def updateBar(i):
    axBar.clear()
    axBar.set_title('SubSections Execution Times')
    for sizeVal in range (0,6):
        if performanceSet1[sizeVal]<originalPerformanceSet1[sizeVal]:
            performanceSet1[sizeVal] = performanceSet1[sizeVal] +1
        if performanceSet2[sizeVal]<originalPerformanceSet2[sizeVal]:
            performanceSet2[sizeVal] = performanceSet2[sizeVal] +1

    axBar.set_xticks(y_pos)
    axBar.set_xticklabels(objects)
    axBar.set_ylabel('Execution Time')
    axBar.set_ylim(top=max(max(performanceSet1),max(performanceSet2))+1)
    axBar.bar(y_pos-0.4,performanceSet1,width=0.4,color='blue',align='center')
    axBar.bar(y_pos,performanceSet2,width=0.4,color='g',align='center')

anim=FuncAnimation(fig,updateBar,repeat=False,frames=range(100))
interactive(True)
plt.show()



axOverallBar=plt.subplot(2, 2, 3)
requiredLables= ('Optimized', 'Nonoptimized')
y_posOverall = np.arange(len(requiredLables))
overallperformanceSet1 = [0,0]
overalloriginalPerformanceSet1 = [10,14]

def updateOverallBar(i):

    axOverallBar.clear()
    axOverallBar.set_xlabel('Execution Time')
    axOverallBar.set_title('Overall Execution Time')
    for sizeVal in range (0,2):
        if overallperformanceSet1[sizeVal]<overalloriginalPerformanceSet1[sizeVal]:
            overallperformanceSet1[sizeVal] = overallperformanceSet1[sizeVal] +3
    axOverallBar.margins(y=0.4)
    axOverallBar.set_yticks(y_posOverall)
    axOverallBar.set_yticklabels(requiredLables)
    axOverallBar.set_xlim(right=max(overallperformanceSet1)+1)
    barhList = axOverallBar.barh(y_posOverall,overallperformanceSet1,height=0.3,color='green',align='center')
    barhList[1].set_color('b')

anim1=FuncAnimation(fig,updateOverallBar,repeat=False,frames=range(100))
interactive(True)
plt.show()


colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'limegreen',
          'red', 'navy', 'blue', 'magenta', 'crimson']
explodeOpt = (0.01, 0.01, 0.01)
labelsOpt = 'GPU Optimizations', 'CPU Optimizations', 'Vector Optimizations'
sizesOpt = [0, 0, 0]
sizesOrignalOpt = [15, 40, 45]
ax1 = plt.subplot(2, 2, 4)

def updateOptPie(num):
    ax1.clear()
    ax1.axis('equal')
    ax1.set_title('Optimization time Breakdown')
    for sizeVal in range (0,3):
        if sizesOpt[sizeVal]<sizesOrignalOpt[sizeVal]:
            sizesOpt[sizeVal] = sizesOpt[sizeVal] +4
    ax1.pie(sizesOpt, explode=explodeOpt, labels=labelsOpt, autopct='%1.1f%%',
            shadow=True, startangle=90)

aniPie = FuncAnimation(fig, updateOptPie, frames=range(100), repeat=False)
interactive(False)


mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
plt.show()
