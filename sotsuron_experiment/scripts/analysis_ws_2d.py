from pprint import pprint
import matplotlib.pyplot as plt

from analysis_management import *
from analysis_initial_processor import *

path_management,csv_labels,color_dict=management_initial()

plt.rcParams["figure.figsize"] = (10,8)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
fig, ax = plt.subplots() 
# pprint(path_management["ras_2d_csv_dir_path_unique"])

path_management["png_dir_path"]=path_management["png_dir_path"]+"/"+"2d_denoise"
os.makedirs(path_management["png_dir_path"],exist_ok=True)

result_chart=[]

for i, trialpath in enumerate(path_management["ras_2d_csv_dir_path_unique"]):
    data=initial_processor(trialpath,denoise=True)
    # save denoise csv
    # data.to_csv(path_management["denoise_2d_csv_dir_path"]+"/"+os.path.basename(trialpath)[:-4]+"_denoise.csv")
    data_np=data.to_numpy()
    frameout_accum_head=np.array([])
    frameout_accum_foot=np.array([])
    frameout_accum_left=np.array([])
    frameout_accum_right=np.array([])
    time_partialout_head=0
    time_partialout_foot=0
    time_partialout_left=0
    time_partialout_right=0
    time_totalout=0
    for i in range(data_np.shape[1]):
        if i%3==0:
            continue
        if i%3==1: #x
            plt.scatter(data_np[:,0],data_np[:,i],c="r",s=1)
            under_idx=np.argwhere(data_np[:,i]<10)
            over_idx=np.argwhere(data_np[:,i]>1910)
            plt.scatter(data_np[under_idx.flatten(),0],data_np[under_idx.flatten(),i],c="g",s=4)
            frameout_accum_left=np.append(frameout_accum_left,under_idx)
            frameout_accum_right=np.append(frameout_accum_right,over_idx)
        if i%3==2: #y
            plt.scatter(data_np[:,0],data_np[:,i],c="b",s=1)
            under_idx=np.argwhere(data_np[:,i]<10)
            over_idx=np.argwhere(data_np[:,i]>1070)
            frameout_accum_head=np.append(frameout_accum_head,under_idx)
            frameout_accum_foot=np.append(frameout_accum_foot,over_idx)
        
        # 部分欠損
        plt.scatter(data_np[under_idx.flatten(),0],data_np[under_idx.flatten(),i],c="k",s=2)
        plt.scatter(data_np[over_idx.flatten(),0],data_np[over_idx.flatten(),i],c="k",s=2)
        
        partial_frameout=np.unique(np.concatenate([under_idx.flatten(),over_idx.flatten()]))
        start=0
        end=0
        for i,frameidx in enumerate(partial_frameout):
            # print(start,end)
            if frameidx-1 not in partial_frameout:
                start=frameidx
            elif frameidx-1 in partial_frameout and frameidx+1 in partial_frameout:
                pass
            elif frameidx-1 in partial_frameout and frameidx+1 not in partial_frameout:
                end=frameidx
                ax.fill_between([data_np[start,0],data_np[end,0]],[0,0],[2000,2000],facecolor='y',alpha=0.5)
                start=frameidx
    frameout_accum_head=np.unique(frameout_accum_head)
    frameout_accum_foot=np.unique(frameout_accum_foot)
    frameout_accum_left=np.unique(frameout_accum_left)
    frameout_accum_right=np.unique(frameout_accum_right)
    
    if i%3==0: # x(left,right)
        start=0
        end=0
        for i,frameidx in enumerate(frameout_accum_left):
            # print(start,end)
            if frameidx-1 not in frameout_accum_left:
                start=frameidx
            elif frameidx-1 in frameout_accum_left and frameidx+1 in frameout_accum_left:
                pass
            elif frameidx-1 in frameout_accum_left and frameidx+1 not in frameout_accum_left:
                end=frameidx
                time_partialout_left+=(data_np[int(end),0]-data_np[int(start),0])
                start=frameidx
        start=0
        end=0
        for i,frameidx in enumerate(frameout_accum_right):
            # print(start,end)
            if frameidx-1 not in frameout_accum_right:
                start=frameidx
            elif frameidx-1 in frameout_accum_right and frameidx+1 in frameout_accum_right:
                pass
            elif frameidx-1 in frameout_accum_right and frameidx+1 not in frameout_accum_right:
                end=frameidx
                time_partialout_right+=(data_np[int(end),0]-data_np[int(start),0])
                start=frameidx
    if i%3==1: # x(head,foot)
        start=0
        end=0
        for i,frameidx in enumerate(frameout_accum_head):
            # print(start,end)
            if frameidx-1 not in frameout_accum_head:
                start=frameidx
            elif frameidx-1 in frameout_accum_head and frameidx+1 in frameout_accum_head:
                pass
            elif frameidx-1 in frameout_accum_head and frameidx+1 not in frameout_accum_head:
                end=frameidx
                time_partialout_head+=(data_np[int(end),0]-data_np[int(start),0])
                start=frameidx
        start=0
        end=0
        for i,frameidx in enumerate(frameout_accum_foot):
            # print(start,end)
            if frameidx-1 not in frameout_accum_right:
                start=frameidx
            elif frameidx-1 in frameout_accum_right and frameidx+1 in frameout_accum_right:
                pass
            elif frameidx-1 in frameout_accum_right and frameidx+1 not in frameout_accum_right:
                end=frameidx
                time_partialout_right+=(data_np[int(end),0]-data_np[int(start),0])
                start=frameidx        
    # frameout_accum=np.unique(frameout_accum)
    all_idx=np.arange(data_np.shape[0])
    # 完全欠損
    allout_idx=np.array([])
    for i, frameidx in enumerate(all_idx[:-1]):
        frameidx=int(frameidx)
        if (data_np[int(all_idx[i+1]),0]-data_np[frameidx,0]>3) & (data_np[-1,0]-data_np[int(all_idx[i+1]),0]>2):
            ax.fill_between([data_np[frameidx,0],data_np[int(all_idx[i+1]),0]],[0,0],[2000,2000],facecolor='r',alpha=0.5)
            allout_idx=np.append(allout_idx,[i])
            time_totalout+=data_np[int(all_idx[i+1]),0]-data_np[frameidx,0]

    # カルテ作成
    result_list=[
        os.path.basename(trialpath)[:2],
        os.path.basename(trialpath)[3:5],
        os.path.basename(trialpath)[6:8],
        data_np.shape[0],
        len(frameout_accum_head),
        len(frameout_accum_foot),
        len(frameout_accum_left),
        len(frameout_accum_right),
        len(allout_idx),
        time_partialout_head,
        time_partialout_foot,
        time_partialout_left,
        time_partialout_right,
        time_totalout,
        trialpath
    ]
    result_chart.append(result_list)
    result_df=pd.DataFrame(result_chart,columns=csv_labels["result_chart"])
    result_df.to_csv(path_management["result_csv_path"], index=False)
    print(result_df)
    
    plt.xlabel("timestamp [s]")
    plt.ylabel("position in image [px] x=red, y=blue frameout=black")
    plt.ylim([0,2000])
    plt.title(os.path.basename(trialpath))
    plt.legend()
    plt.savefig(path_management["png_dir_path"]+"/"+os.path.basename(trialpath)[:8]+"_denoise.png")
    plt.pause(0.01)
    plt.cla()
json_saver(path_management,csv_labels,color_dict)