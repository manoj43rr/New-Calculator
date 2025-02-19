import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.header("Incentive Calculator")

video_file = open("bean.mp4", "rb")
video_bytes = video_file.read()

options = ["Annual Calculator", "Non Annual Calculator"]

val = st.radio("choose the type of calculator: ", options, index=None)

if val is not None:
    if val == options[0]:
        inputFile = st.file_uploader("Please Upload the file with renewal Data", type=["xlsx", "xls", "csv"])

        if inputFile is not None:

            if inputFile.name.endswith(".csv"):
                data = pd.read_csv(inputFile)
            else:
                data = pd.read_excel(inputFile, engine="openpyxl")


            persons = data[data.columns[2]].unique().tolist()

            assignedAmounts = []
            targetAchieved = []
            achievedAmounts = []

            for i in persons:
                tempDf = data[data[data.columns[2]] == i].copy()  # Ensure proper filtering
                assignedAmounts.append(tempDf[tempDf.columns[0]].sum())

                tempDf_pass = tempDf[tempDf[tempDf.columns[3]] == "Active"].copy()
                targetAchieved.append(tempDf_pass[tempDf_pass.columns[1]].count())
                achievedAmounts.append(tempDf_pass[tempDf_pass.columns[0]].sum())

            percAchieved = []
            for i in range(len(persons)):
                if assignedAmounts[i] == 0:
                    percAchieved.append(0.0)
                else:
                    percAchieved.append(round((achievedAmounts[i] / assignedAmounts[i]) * 100.00, 3))

            incentiveLogic1 = []
            for i in range(len(persons)):
                if percAchieved[i] >= 70.0:
                    incentive = assignedAmounts[i] * (percAchieved[i] / 100) * ((((percAchieved[i] / 100) - 0.7) / 10) + 0.005)
                    incentiveLogic1.append(round(incentive))
                else:
                    incentiveLogic1.append(0)

            incentiveData = pd.read_excel("AnnualIncentiveData.xlsx")
            incentiveLogic2 = []

            for i in range(len(persons)):
                if percAchieved[i] >= 70.0:
                    row = incentiveData[(incentiveData["start_range"] <= round(percAchieved[i])) & 
                                        (round(percAchieved[i]) <= incentiveData["end_range"])]
                    
                    if not row.empty:
                        incentive = assignedAmounts[i] * (percAchieved[i] / 100) * row[row.columns[2]].iloc[0]
                        incentiveLogic2.append(round(incentive))
                    else:
                        incentiveLogic2.append(0.0)
                else:
                    incentiveLogic2.append(0.0)

            finalData = pd.DataFrame({
                "Individuals" : persons,
                "Assigned Amount" : assignedAmounts,
                "Percentage of renwals Done": percAchieved,
                "incentiveLogic1" : incentiveLogic1,
                "incentiveLogic2" : incentiveLogic2,
            })

            st.dataframe(finalData)

            fig, ax = plt.subplots()
            x = np.arange(len(finalData["Individuals"]))
            width = 0.4

            ax.bar(x - width / 2, finalData["incentiveLogic1"], width, label="Incentive Logic 1", color='blue')
            ax.bar(x + width / 2, finalData["incentiveLogic2"], width, label="Incentive Logic 2", color='orange')

            ax.set_xlabel("Individuals")
            ax.set_ylabel("Incentives")
            ax.set_title("Comparison of Incentive Logic")
            ax.set_xticks(x)
            ax.set_xticklabels(finalData["Individuals"], rotation=45)
            ax.legend()

            st.pyplot(fig)
            st.balloons()
        else:
            st.warning("Something Wrong", icon="⚠️")
    
    elif val == options[1]:
        inputFile = st.file_uploader("Please Upload the file with renewal Data", type=["xlsx", "xls", "csv"])

        if inputFile is not None:

            if inputFile.name.endswith(".csv"):
                data = pd.read_csv(inputFile)
            else:
                data = pd.read_excel(inputFile, engine="openpyxl")


            persons = data[data.columns[2]].unique().tolist()

            assignedAmounts = []
            targetAchieved = []
            achievedAmounts = []

            for i in persons:
                tempDf = data[data[data.columns[2]] == i].copy()  # Ensure proper filtering
                assignedAmounts.append(tempDf[tempDf.columns[0]].sum())

                tempDf_pass = tempDf[tempDf[tempDf.columns[3]] == "Active"].copy()
                targetAchieved.append(tempDf_pass[tempDf_pass.columns[1]].count())
                achievedAmounts.append(tempDf_pass[tempDf_pass.columns[0]].sum())

            percAchieved = []
            for i in range(len(persons)):
                if assignedAmounts[i] == 0:
                    percAchieved.append(0.0)
                else:
                    percAchieved.append(round((achievedAmounts[i] / assignedAmounts[i]) * 100.00, 3))

            incentiveLogic1 = []
            for i in range(len(persons)):
                if percAchieved[i] >= 85.0:
                    incentive = assignedAmounts[i] * (percAchieved[i] / 100) * ((((percAchieved[i] / 100) - 0.85) / 10) + 0.015)
                    incentiveLogic1.append(round(incentive))
                else:
                    incentiveLogic1.append(0)

            incentiveData = pd.read_excel("nonAnnualIncentiveData.xlsx")
            incentiveLogic2 = []

            for i in range(len(persons)):
                if percAchieved[i] >= 85.0:
                    row = incentiveData[(incentiveData["start_range"] <= percAchieved[i]) & 
                                        (percAchieved[i] <= incentiveData["end_range"])]
                    
                    if not row.empty:
                        incentive = assignedAmounts[i] * (percAchieved[i] / 100) * row[row.columns[2]].iloc[0]
                        incentiveLogic2.append(round(incentive))
                    else:
                        incentiveLogic2.append(0.0)
                else:
                    incentiveLogic2.append(0.0)

            finalData = pd.DataFrame({
                "Individuals" : persons,
                "Assigned Amount" : assignedAmounts,
                "Percentage of renwals Done": percAchieved,
                "incentiveLogic1" : incentiveLogic1,
                "incentiveLogic2" : incentiveLogic2,
            })

            st.dataframe(finalData)

            fig, ax = plt.subplots()
            x = np.arange(len(finalData["Individuals"]))
            width = 0.4

            ax.bar(x - width / 2, finalData["incentiveLogic1"], width, label="Incentive Logic 1", color='blue')
            ax.bar(x + width / 2, finalData["incentiveLogic2"], width, label="Incentive Logic 2", color='orange')

            ax.set_xlabel("Individuals")
            ax.set_ylabel("Incentives")
            ax.set_title("Comparison of Incentive Logic")
            ax.set_xticks(x)
            ax.set_xticklabels(finalData["Individuals"], rotation=45)
            ax.legend()

            st.pyplot(fig)
            st.balloons()
        else:
            st.warning("Something Wrong", icon="⚠️")
else:    
    st.video(video_bytes, autoplay=True, muted=True, loop=True)
