import matplotlib.pyplot as plt
import pandas as pd

def visualize():
    mbti_profiles = pd.read_csv('mbti.csv', names=['Name','MBTI Profile','1','2','3','4'])
    fig,axs = plt.subplots(2,2)
    data,mbti,freq = [],[],[]

    for i in range(1,5):
        data.append(mbti_profiles[str(i)].value_counts())
        mbti.append(mbti_profiles[str(i)].value_counts().index)
        freq.append(mbti_profiles[str(i)].value_counts().values)

    for i,d in enumerate(data):
        if i <2:
            x = 0
            y = 0
        else:
            x = -2
            y = 1
        
        axs[x+i,y].bar(mbti[i],freq[i])
    plt.show()