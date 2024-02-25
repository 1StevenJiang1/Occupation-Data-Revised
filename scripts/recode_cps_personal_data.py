import math

import pandas as pd
from pandas import DataFrame, Series
import os


def insert_serial_num(df) -> None:
    """ give a serial number to each item in the
    workbook
    """
    num_row = len(df)

    serial_num = [i for i in range(num_row)]
    df.insert(loc=0, column="serial number", value=serial_num)
    print("finished inserting serial num")


def recode_sex(df: pd.DataFrame) -> pd.DataFrame:
    """the filter indicates that the data set does not contain missing code for this category.
    hence the missing code is not handled here

    coding: 1 is men and 2 is women
    """
    temp = []
    num_row = len(df)
    column_data = df["SEX"]
    for i in range(num_row):
        if column_data[i] == 1:
            temp.append([1, 0])
        else:
            temp.append([0, 1])
    # Dummy code the 'SEX' column with custom prefix and prefix_sep
    dummy_df = pd.DataFrame(temp, columns=["Men", "Women"])

    # Concatenate the dummy coded DataFrame with the original DataFrame
    df = pd.concat([df, dummy_df], axis=1)

    print("Finished recoding sex")
    return df


def dummy_code_race(df: DataFrame) -> DataFrame:
    """here we only care about white black indian asian. 651 and 652, which are asian only and pacific islander
    only are collapsed into asian and pacific islander (650). all other races are in the category of other
    999 represents missing code and is replaced with 0 in all categories

    coding: 100 is white; 200 is black; 300 is indian; 650 651 652 is asian and pacific islander.
    all other codes except 999 are categorized as other. 999 are missing and will be handled later
    """
    temp = []
    num_row = len(df)
    column_data = df["RACE"]

    for i in range(num_row):
        if column_data[i] == 100:
            temp.append([1, 0, 0, 0, 0])  # white
        elif column_data[i] == 200:
            temp.append([0, 1, 0, 0, 0])  # black
        elif column_data[i] == 300:
            temp.append([0, 0, 1, 0, 0])  # indian
        elif column_data[i] in [650, 651, 652]:
            temp.append([0, 0, 0, 1, 0])  # asian
        elif column_data[i] == 999:
            temp.append([0, 0, 0, 0, 0])  # missing value
            print("you have encountered 999 at line" + str(i) + "\n")
        else:
            temp.append([0, 0, 0, 0, 1])  # other

    # Create new DataFrame with dummy coded columns
    dummy_df = pd.DataFrame(temp, columns=["Race_White", "Race_Black", "Race_Indian", "Race_Asian", "Race_Other"])

    # Concatenate dummy coded DataFrame with original DataFrame
    df = pd.concat([df, dummy_df], axis=1)
    print("finished dummy coding race")
    return df


def dummy_code_educ(df: DataFrame) -> DataFrame:
    """group all levels of education by diploma. Hence, we have:  less than high school, high school, college, more
     than college.

    coding: 0<= educ< 73 are less than high school; 73 <= educ < 111 are high school, 111 == educ are college, 111<
    educ < 999 are more than college; 999 are missing and will be handled later
    """

    temp = []
    num_row = len(df)
    column_data = df["EDUC"]
    for i in range(num_row):
        if 0 < column_data[i] < 73:
            temp.append([1, 0, 0, 0])  # less than high school
        elif 73 <= column_data[i] < 111:
            temp.append([0, 1, 0, 0])  # high school
        elif column_data[i] == 111:
            temp.append([0, 0, 1, 0])  # college
        elif 111 < column_data[i] <= 998:
            temp.append([0, 0, 0, 1])  # more than college
        else:
            temp.append([0, 0, 0, 0])  # missing value
            print("you have encountered 999 at line" + str(i) + "\n")
    dummy_df = pd.DataFrame(temp, columns=["Less_Than_High_School", "High_School", "College", "More_Than_College"])
    df = pd.concat([df, dummy_df], axis=1)
    print("finished dummy coding educ")
    return df

def ln_wage(df: DataFrame) -> DataFrame:
    """Take the log of income

    coding: 0, 99999999 , 99999998 are treted as missing values
    """
    temp = []
    num_row = len(df)
    column_data = df["INCWAGE"]

    for i in range(num_row):
        if column_data[i] not in [0, 99999999, 99999998]:
            temp.append(math.log(int(column_data[i])))
        else:
            temp.append(0)
    df["Log_Income"] = temp
    print("finished taking the log of income")
    return df


def merge_occupation(df_1: DataFrame, df_2: DataFrame) -> DataFrame:
    """import the occupation classification of the individuals into the cps data set. df_1 is the cps data
    whereas df_2 is the occupation classifications of the occupations"""
    temp = []
    num_row = len(df_1)
    ipums_occ = df_1["OCC"]
    cross_walk_ACS = df_2["ACS"]
    classifications = df_2["Vulnerability"]

    for i in range(num_row):
        item = ipums_occ[i]
        if item != 0:
            # for each occ code, if it is not 0, then we look for its index in the
            # corresponding column in the crosswalk file. We then use the index to obtain
            # the associated occupation classification
            cross_walk_index = cross_walk_ACS.index(item)
            classification = classifications[cross_walk_index]
            temp.append(classification)
        else:
            temp.append(["no classification"])
    df_1["Vulnerability"] = temp
    print("finished merging the classifications")
    return df_1


def merge_occupation1(df_1: DataFrame, df_2: DataFrame) -> DataFrame:
    """Merge the occupation classifications of the individuals into the CPS data set."""
    temp = []
    ipums_occ = df_1["OCC"]
    cross_walk_ACS = df_2["ACS"]
    classifications = df_2["Vulnerability"]

    for item in ipums_occ:
        if item != 0:
            # Find the corresponding row in df_2 where ACS equals item
            mask = cross_walk_ACS == item
            classification = classifications[mask].values
            if len(classification) > 0:
                temp.append(classification[0])
            else:
                temp.append("No classification")
        else:
            temp.append("No classification")

    df_1["Vulnerability"] = temp
    print("Finished merging the classifications")
    return df_1


def dummy_code_vulnerability(df: DataFrame) -> DataFrame:
    temp = []
    num_row = len(df)
    column_data = df["Vulnerability"]
    for i in range(num_row):
        if column_data[i] == "Vulnerable":
            temp.append([1, 0, 0, 0])
        elif column_data[i] == "Replaced":
            temp.append([0, 1, 0, 0])
        elif column_data[i] == "Mildly Complemented":
            temp.append([0, 0, 1, 0])
        elif column_data[i] == "Complemented":
            temp.append([0, 0, 0, 1])
        else:
            temp.append([0, 0, 0, 0])
    dummy_df = pd.DataFrame(temp, columns=["Vulnerable", "Replaced", "Mildly Complemented", "Complemented"])
    df = pd.concat([df, dummy_df], axis=1)
    print("finished dummy coding occ")
    return df



if __name__ == "__main__":
    cwd = os.getcwd()
    cps_path = os.path.join(cwd, "data", "occupation_merged.csv")
    cross_walk_path = os.path.join(cwd, "data", "merged_cross_walk.csv")
    dataframe = pd.read_csv(cps_path, encoding="utf-8")
    dataframe2 = pd.read_csv(cross_walk_path)
    # insert_serial_num(dataframe)
    # dataframe = recode_sex(dataframe)
    # dataframe = dummy_code_race(dataframe)
    # dataframe = dummy_code_educ(dataframe)
    # dataframe = ln_wage(dataframe)
    # dataframe = merge_occupation1(dataframe, dataframe2)
    dataframe = dummy_code_vulnerability(dataframe)
    dataframe.to_csv("dummy occ.csv", index=False)


