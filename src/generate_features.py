import numpy as np # linear algebra
import pandas as pd
import argparse
import yaml
import warnings
warnings.filterwarnings("ignore")
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def clean_gender(my_df):
    '''
    clean up gender in the table
    :param my_df: the table that has all covariates
    :return: cleaned table
    '''
    # Made gender groups
    male_str = ["male", "m", "male-ish", "maile", "mal", "male (cis)", "make", "male ", "man", "msle", "mail", "malr",
                "cis man", "Cis Male", "cis male"]
    trans_str = ["trans-female", "something kinda male?", "queer/she/they", "non-binary", "nah", "all", "enby", "fluid",
                 "genderqueer", "androgyne", "agender", "male leaning androgynous", "guy (-ish) ^_^", "trans woman",
                 "neuter", "female (trans)", "queer", "ostensibly male, unsure what that really means"]
    female_str = ["cis female", "f", "female", "woman", "femake", "female ", "cis-female/femme", "female (cis)",
                  "femail"]

    for (row, col) in my_df.iterrows():

        if str.lower(col.Gender) in male_str:
            my_df['Gender'].replace(to_replace=col.Gender, value='male', inplace=True)

        if str.lower(col.Gender) in female_str:
            my_df['Gender'].replace(to_replace=col.Gender, value='female', inplace=True)

        if str.lower(col.Gender) in trans_str:
            my_df['Gender'].replace(to_replace=col.Gender, value='trans', inplace=True)

    # Get rid of bs
    stk_list = ['A little about you', 'p']
    my_df = my_df[~my_df['Gender'].isin(stk_list)]
    my_df.index = np.arange(0, my_df.shape[0])

    return  my_df

def pdtable(key,df):
    return df.groupby(key).size().sort_values(ascending=False)

def clean_data(my_df):
    '''

    :param my_df: the table contains all covariates
    :return:
    '''

    logging.info("generate features begin")
    my_df.treatment.loc[my_df.treatment == "Yes"] = 1
    my_df.treatment.loc[my_df.treatment == "No"] = 0

    # Treat NA
    my_df = my_df.drop(['comments'], axis=1)  # comments too much NA just drop
    my_df = my_df.drop(['Timestamp'], axis=1)  # Others are not missing at random so shouldnt dropped

    # treat gender
    my_df = clean_gender(my_df)

    my_df.Gender = pd.Series([1 if x == "male" else 0 for x in my_df.Gender])

    # look at age
    my_df.Age.loc[my_df.Age < 18] = 18
    my_df.Age.loc[my_df.Age > 80] = 80

    # country and state
    top_10_country = list(pdtable('Country', my_df)[:10].index)
    my_df = my_df[my_df.Country.isin(top_10_country)]

    # treat self_employed
    my_df.self_employed.fillna("No", inplace=True)
    my_df.self_employed.loc[my_df.self_employed == "Yes"] = 1
    my_df.self_employed.loc[my_df.self_employed == "No"] = 0

    # treat family history
    my_df.family_history.loc[my_df.family_history == "Yes"] = 1
    my_df.family_history.loc[my_df.family_history == "No"] = 0

    # treat work interfere
    my_df.work_interfere.fillna("Don't Know", inplace=True)
    my_df.work_interfere.loc[my_df.work_interfere == "Don't Know"] = 0
    my_df.work_interfere.loc[my_df.work_interfere == "Never"] = 1
    my_df.work_interfere.loc[my_df.work_interfere == "Rarely"] = 2
    my_df.work_interfere.loc[my_df.work_interfere == "Sometimes"] = 3
    my_df.work_interfere.loc[my_df.work_interfere == "Often"] = 4

    # treat no_employee
    my_df.no_employees.loc[my_df.no_employees == "More than 1000"] = 5
    my_df.no_employees.loc[my_df.no_employees == "26-100"] = 2
    my_df.no_employees.loc[my_df.no_employees == "6-25"] = 1
    my_df.no_employees.loc[my_df.no_employees == "100-500"] = 3
    my_df.no_employees.loc[my_df.no_employees == "1-5"] = 0
    my_df.no_employees.loc[my_df.no_employees == "500-1000"] = 4

    # remote work
    my_df.remote_work.loc[my_df.remote_work == "Yes"] = 1
    my_df.remote_work.loc[my_df.remote_work == "No"] = 0

    # tech company
    my_df.tech_company.loc[my_df.tech_company == "Yes"] = 1
    my_df.tech_company.loc[my_df.tech_company == "No"] = 0

    # benefits
    my_df.benefits.loc[my_df.benefits == "Yes"] = 2
    my_df.benefits.loc[my_df.benefits == "Don't know"] = 1
    my_df.benefits.loc[my_df.benefits == "No"] = 0

    #care option
    my_df.care_options.loc[my_df.care_options == "Yes"] = 2
    my_df.care_options.loc[my_df.care_options == "Not sure"] = 1
    my_df.care_options.loc[my_df.care_options == "No"] = 0

    # wellness program
    my_df.wellness_program.loc[my_df.wellness_program == "Yes"] = 2
    my_df.wellness_program.loc[my_df.wellness_program == "Don't know"] = 1
    my_df.wellness_program.loc[my_df.wellness_program == "No"] = 0

    # seek_help
    my_df.seek_help.loc[my_df.seek_help == "Yes"] = 2
    my_df.seek_help.loc[my_df.seek_help == "Don't know"] = 1
    my_df.seek_help.loc[my_df.seek_help == "No"] = 0

    # annonymity
    my_df.anonymity.loc[my_df.anonymity == "Yes"] = 2
    my_df.anonymity.loc[my_df.anonymity == "Don't know"] = 1
    my_df.anonymity.loc[my_df.anonymity == "No"] = 0

    # leave
    my_df.leave.loc[my_df.leave == "Don't know"] = 0
    my_df.leave.loc[my_df.leave == "Very easy"] = 1
    my_df.leave.loc[my_df.leave == "Somewhat easy"] = 2
    my_df.leave.loc[my_df.leave == "Somewhat difficult"] = 3
    my_df.leave.loc[my_df.leave == "Very difficult"] = 4

    #mental_health_consequence
    my_df.mental_health_consequence.loc[my_df.mental_health_consequence == "Yes"] = 2
    my_df.mental_health_consequence.loc[my_df.mental_health_consequence == "Maybe"] = 1
    my_df.mental_health_consequence.loc[my_df.mental_health_consequence == "No"] = 0

    #phys_health_consequence
    my_df.phys_health_consequence.loc[my_df.phys_health_consequence == "Yes"] = 2
    my_df.phys_health_consequence.loc[my_df.phys_health_consequence == "Maybe"] = 1
    my_df.phys_health_consequence.loc[my_df.phys_health_consequence == "No"] = 0

    # coworkers
    my_df.coworkers.loc[my_df.coworkers == "Yes"] = 2
    my_df.coworkers.loc[my_df.coworkers == "Some of them"] = 1
    my_df.coworkers.loc[my_df.coworkers == "No"] = 0

    # supervisor
    my_df.supervisor.loc[my_df.supervisor == "Yes"] = 2
    my_df.supervisor.loc[my_df.supervisor == "Some of them"] = 1
    my_df.supervisor.loc[my_df.supervisor == "No"] = 0

    #mental_health_interview
    my_df.mental_health_interview.loc[my_df.mental_health_interview == "Yes"] = 2
    my_df.mental_health_interview.loc[my_df.mental_health_interview == "Maybe"] = 1
    my_df.mental_health_interview.loc[my_df.mental_health_interview == "No"] = 0

    #phys_health_interview
    my_df.phys_health_interview.loc[my_df.phys_health_interview == "Yes"] = 2
    my_df.phys_health_interview.loc[my_df.phys_health_interview == "Maybe"] = 1
    my_df.phys_health_interview.loc[my_df.phys_health_interview == "No"] = 0

    #mental_vs_physical
    my_df.mental_vs_physical.loc[my_df.mental_vs_physical == "Yes"] = 2
    my_df.mental_vs_physical.loc[my_df.mental_vs_physical == "Don't know"] = 1
    my_df.mental_vs_physical.loc[my_df.mental_vs_physical == "No"] = 0

    #obs_consequence
    my_df.obs_consequence.loc[my_df.obs_consequence == "Yes"] = 1
    my_df.obs_consequence.loc[my_df.obs_consequence == "No"] = 0

    # one hot country
    country_dummies = pd.get_dummies(my_df['Country'], prefix='country')
    my_df = pd.concat([my_df, country_dummies], axis=1)
    my_df = my_df.drop(['Country'], axis=1)

    # get top 10 states
    top_10_states = list(pdtable('state', my_df)[:10].index)
    states_dummmies = pd.get_dummies(my_df['state'], prefix='state')
    top_10_states = ['state_' + x for x in top_10_states]
    my_df = pd.concat([my_df, states_dummmies.loc[:, top_10_states]], axis=1)
    my_df = my_df.drop(['state'], axis=1)

    # finish up and save
    my_df = my_df.apply(pd.to_numeric)
    my_df.index = np.arange(0, my_df.shape[0])

    logging.info("generate features done")

    return my_df

def choose_features(args):
    """Loads config and executes load data set
    Args:
        args: passed in argparser
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    config = config['generate_features']
    if args.loadcsv is not None:
        df = pd.read_csv(args.loadcsv)
    else:
        df = pd.read_csv(config['read_path'])

    df = clean_data(df)

    df = df[config['choose_features']['features_to_use']]

    if args.savecsv is not None:
        df.to_csv(args.savecsv)
    else:
        df.to_csv(config['save_features'])

    logging.info("cleaned data saved")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', default= 'config/config.yml',help='path to yaml file with configurations')
    parser.add_argument('--loadcsv', help='Path to where the raw data is stored (optional)')
    parser.add_argument('--savecsv', help='Path to where the dataset should be saved to (optional)')

    args = parser.parse_args()

    choose_features(args)

