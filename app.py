import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

st.title('Health Monitoring Dashboard')

# Load data
health_data = pd.read_csv('healthmonitoring.csv')

# calculate medians
median_body_temp = health_data['BodyTemperature'].median()
median_oxygen_sat = health_data['OxygenSaturation'].median()

# fill missing values
health_data['BodyTemperature'].fillna(median_body_temp, inplace=True)
health_data['OxygenSaturation'].fillna(median_oxygen_sat, inplace=True)

# Create a dropdown for analysis selection
analysis_option = st.selectbox("Select an analysis option", ["Summary Statistics", "Gender Distribution", "Correlation Matrix", "Heart Rate by Activity Level", "Blood Pressure Distribution", "Health Metrics by Gender"])

if analysis_option == "Summary Statistics":
    st.write("## Summary Statistics")
    st.write(health_data.drop('PatientID',axis = 1).describe())
    # Plotting distributions of numerical features
    fig, axes = plt.subplots(3, 2, figsize=(14, 18))
    sns.histplot(health_data['Age'], bins=20, kde=True, ax=axes[0, 0])
    axes[0, 0].set_title('Age Distribution')

    sns.histplot(health_data['HeartRate'], bins=20, kde=True, ax=axes[0, 1])
    axes[0, 1].set_title('Heart Rate Distribution')

    sns.histplot(health_data['RespiratoryRate'], bins=20, kde=True, ax=axes[1, 0])
    axes[1, 0].set_title('Respiratory Rate Distribution')

    sns.histplot(health_data['BodyTemperature'], bins=20, kde=True, ax=axes[1, 1])
    axes[1, 1].set_title('Body Temperature Distribution')

    sns.histplot(health_data['OxygenSaturation'], bins=10, kde=True, ax=axes[2, 0])
    axes[2, 0].set_title('Oxygen Saturation Distribution')

    fig.delaxes(axes[2, 1])  # remove unused subplot

    plt.tight_layout()
    st.pyplot(fig)

elif analysis_option == "Gender Distribution":
    st.write("## Gender Distribution")
    gender_counts = health_data['Gender'].value_counts()
    st.write(gender_counts)

    # Calculate percentage distribution
    gender_percentage = gender_counts / gender_counts.sum() * 100
    st.write("Percentage Distribution:")
    st.write(gender_percentage)
    st.write('Males comprising a slight majority at 51.2%.')

    # Plotting the pie chart
    fig, axes = plt.subplots(1, 1, figsize=(6, 6))
    gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff'])
    plt.ylabel('')
    plt.title('Gender Distribution')
    st.pyplot(fig)


elif analysis_option == "Correlation Matrix":
    st.write("## Correlation Matrix")
    correlation_matrix = health_data[['Age', 'HeartRate', 'RespiratoryRate', 'BodyTemperature', 'OxygenSaturation']].corr()
    st.write(correlation_matrix)
    st.write('The correlation matrix shows no strong correlations between the variables, as all the values are close to zero.')

    # Plotting the correlation matrix heatmap
    fig, axes = plt.subplots(1, 1, figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=axes)
    plt.title('Correlation Matrix')
    st.pyplot(fig)


elif analysis_option == "Heart Rate by Activity Level":
    st.write("## Heart Rate by Activity Level")

    # Plotting the box plot using seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='ActivityLevel', y='HeartRate', data=health_data, ax=ax)
    plt.title('Heart Rate by Activity Level')
    plt.ylabel('Heart Rate (beats per minute)')
    plt.xlabel('Activity Level')
    st.pyplot(fig)
    st.write('It shows that the median heart rate increases from resting to walking, which is expected as physical activity increases. However, the median heart rate does not significantly increase further during running compared to walking, which is unusual since we would expect a higher median heart rate for a more strenuous activity.')
    st.write('There is considerable overlap in the interquartile ranges between walking and running, suggesting similar variability in heart rates for these activities within the sampled population. The presence of outliers in the resting category indicates that some individuals have resting heart rates that are much higher than the typical range for the rest of the group')


elif analysis_option == "Blood Pressure Distribution":
    st.write("## Blood Pressure Distribution")
    health_data[['SystolicBP', 'DiastolicBP']] = health_data['BloodPressure'].str.split('/', expand=True).astype(int)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(health_data['SystolicBP'], color="skyblue", label="Systolic", kde=True)
    sns.histplot(health_data['DiastolicBP'], color="red", label="Diastolic", kde=True)
    plt.title('Blood Pressure Distribution')
    plt.xlabel('Blood Pressure (mmHg)')
    plt.legend()
    st.pyplot(fig)
    st.write('The systolic blood pressure, represented in blue, shows a more spread-out distribution with peaks suggesting common readings around 120 mmHg and 140 mmHg. The diastolic blood pressure, in red, appears to have a narrower distribution, with a significant peak around 80 mmHg.')
    st.write('The spread of systolic values is broader than the diastolic ones, which is typical as systolic pressure tends to vary more with factors like activity level and stress. This distribution is consistent with general population trends where a systolic reading of around 120 mmHg and a diastolic reading of around 80 mmHg are considered normal.')


elif analysis_option == "Health Metrics by Gender":
    st.write("## Health Metrics by Gender")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sns.boxplot(x='Gender', y='HeartRate', data=health_data, ax=axes[0])
    axes[0].set_title('Heart Rate by Gender')
    axes[0].set_xlabel('Gender')
    axes[0].set_ylabel('Heart Rate (beats per minute)')

    sns.boxplot(x='Gender', y='OxygenSaturation', data=health_data, ax=axes[1])
    axes[1].set_title('Oxygen Saturation by Gender')
    axes[1].set_xlabel('Gender')
    axes[1].set_ylabel('Oxygen Saturation (%)')

    plt.tight_layout()
    st.pyplot(fig)
    st.write('For heart rate, both males and females show similar median values with a relatively similar interquartile range, indicating no significant difference in heart rate between genders within this dataset.')
    st.write('In terms of oxygen saturation, again, both genders exhibit nearly identical medians and interquartile ranges, suggesting that oxygen saturation does not differ notably between males and females in this sample.')
    st.write('There are a few outliers in oxygen saturation for both genders, indicating a few individuals with lower than typical values, but these do not seem to affect the overall distribution significantly.')