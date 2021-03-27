import os
import csv
import pandas as pd
from operator import mul


entries = os.listdir('database/DataPaper/')
doc_name = "database/DataPaper/"
all_filenames = []
for ent in entries:
    for (dirpath, dirnames, filenames) in os.walk(doc_name + ent + "/"):
        all_filenames.extend([doc_name + ent + "/" + name for name in filenames])


PSQI = []
age, gender, weight, height, BMI  = [], [], [], [], []
cortisol_before, cortisol_after = [], []
melatonin_before, melatonin_after = [], []
latency_efficiency, total_minutes_in_bed, total_sleep_time = [], [], []
RR = []
daily_stress = []
activity_medium, activity_heavy = [], []
activity_small_screen_usage, activity_large_screen_usage = [], []
activity_smoking, activity_alcohol_assumption = [], []
actigraph_X_mean, actigraph_Y_mean, actigraph_Z_mean = [], [], []
steps_mean = []


def convert_to_minutes(my_time):
    factors = (60, 1)
    t2 = sum(map(mul, map(int, my_time.split(':')), factors))
    return(t2)  


for fln in all_filenames:

    if fln[-13:] == "user_info.csv":
        data = pd.read_csv(fln)
        age.append(data["Age"][0])
        weight.append(data["Weight"][0])
        height.append(data["Height"][0])
        gender.append(data["Gender"][0])

    if fln[-10:] == "saliva.csv":
        data = pd.read_csv(fln)
        cortisol_before.append(data["Cortisol NORM"][0])
        cortisol_after.append(data["Cortisol NORM"][1])
        melatonin_before.append(data["Melatonin NORM"][0])
        melatonin_after.append(data["Melatonin NORM"][1])

    if fln[-9:] == "sleep.csv":
        data = pd.read_csv(fln)
        latency_efficiency.append(data["Efficiency"][0])
        total_minutes_in_bed.append(data["Total Minutes in Bed"][0])
        total_sleep_time.append(data["Total Sleep Time (TST)"][0])

    if fln[-6:] == "RR.csv":
        data = pd.read_csv(fln)
        ibi_s = data["ibi_s"]
        mean_RR = sum(ibi_s)/len(ibi_s)
        RR.append(mean_RR)

    if fln[-17:] == "questionnaire.csv":
        data = pd.read_csv(fln)
        PSQI.append(data["Pittsburgh"][0])
        daily_stress.append(data["Daily_stress"][0])

    if fln[-12:] == "Activity.csv":
        data = pd.read_csv(fln)
        activity = data["Activity"].tolist()
        start = data["Start"].tolist()
        end = data["End"].tolist()
        start_in_m = [convert_to_minutes(i) for i in start]
        end_in_m = [convert_to_minutes(i) for i in end]
        duration = [end_in_m[i] - start_in_m[i] for i in range(len(start))]
        
        actvt = {"Activity": activity,
                "Duration": duration}
        actvt_df = pd.DataFrame(actvt, 
                                columns = ["Activity", "Duration"])
        by = actvt_df.groupby('Activity', as_index=False).agg({"Duration": "sum"})
        a, d = by["Activity"].tolist(), by["Duration"].tolist()
        lst = [0] * 8
        indcs = [1, 5, 6, 8, 9, 10, 11, 12]
        for j in range(len(indcs)):
            try:
                h = a.index(indcs[j])
                lst[j] = d[h]
            except:
                continue

        activity_medium.append(lst[1])
        activity_heavy.append(lst[2])
        activity_small_screen_usage.append(lst[3])
        activity_large_screen_usage.append(lst[4])
        activity_smoking.append(lst[6])
        activity_alcohol_assumption.append(lst[7])

    if fln[-13:] == "Actigraph.csv":
        data = pd.read_csv(fln)
        actigraph_X = data["Axis1"].tolist()
        actigraph_Y = data["Axis2"].tolist()
        actigraph_Z = data["Axis3"].tolist()
        steps = data["Steps"].tolist()
        actigraph_X_mean.append(sum(actigraph_X)/len(actigraph_X))
        actigraph_Y_mean.append(sum(actigraph_Y)/len(actigraph_Y))
        actigraph_Z_mean.append(sum(actigraph_Z)/len(actigraph_Z))
        steps_mean.append(sum(steps)/len(steps))
        

column_names = ["User", "PSQI", "Age", "Gender", "Weight", "Height", "BMI",
                "Cortisol_before", "Cortisol_after", "Melatonin_before", "Melatonin_after", 
                "Latency_Efficiency", "Total_minutes_in_bed", "Total_sleep_time",
                "RR", "Daily_stress",
                "Activity_medium", "Activity_heavy", "Activity_small_screen_usage", "Activity_large_screen_usage",
                "Activity_smoking", "Activity_alcohol_assumption",
                "Actigraph_X_mean", "Actigraph_Y_mean", "Actigraph_Z_mean",
                "Steps_mean"]


for i in range(len(weight)):
    ind = weight[i]/(height[i]**2)*10000
    BMI.append(ind)


d = {"User" : entries, 
     "PSQI" : PSQI, 
     "Age": age,
     "Gender" : gender,
     "Weight" : weight,
     "Height" : height,
     "BMI" : BMI, 
     "Cortisol_before" : cortisol_before, 
     "Cortisol_after" : cortisol_after, 
     "Melatonin_before" : melatonin_before, 
     "Melatonin_after" : melatonin_after,      
     "Latency_Efficiency" : latency_efficiency, 
     "Total_minutes_in_bed" : total_minutes_in_bed, 
     "Total_sleep_time" : total_sleep_time,            
     "RR" : RR, 
     "Daily_stress" : daily_stress,
     "Activity_medium" : activity_medium, 
     "Activity_heavy" : activity_heavy, 
     "Activity_small_screen_usage" : activity_small_screen_usage, 
     "Activity_large_screen_usage" : activity_large_screen_usage,
     "Activity_smoking" : activity_smoking, 
     "Activity_alcohol_assumption" : activity_alcohol_assumption,
     "Actigraph_X_mean" : actigraph_X_mean, 
     "Actigraph_Y_mean" : actigraph_Y_mean, 
     "Actigraph_Z_mean" : actigraph_Z_mean,
     "Steps_mean" : steps_mean}


df = pd.DataFrame(d, columns = column_names)
df.to_csv('Data.csv')
print("Saved")
