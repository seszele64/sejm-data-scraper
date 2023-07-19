import pandas as pd
import logging

from paths import data_folder


def load_df():

    # check if mps.csv exists
    try:
        mps_df = pd.read_csv(data_folder + '/mps.csv', sep=';', encoding='utf-8',
                             index_col=0, dtype={'id': str})

        # always zfill id to 3 digits
        mps_df['id'] = mps_df['id'].apply(lambda x: x.zfill(3))

    except FileNotFoundError:
        # create dataframe
        mps_df = pd.DataFrame(columns=['id', 'name', 'surname', 'link', 'party_list', 'constituency', 'elected_date', 'no_of_votes',
                                       'oath_date', 'parliamentary_experience', 'club', 'birth_date', 'education', 'school', 'profession', 'email'])

    return mps_df


# def save df to csv
def save_df_to_csv(df):

    logging.info("Saving df to csv...")

    # save df to csv -> data folder
    df.to_csv(data_folder + '/mps.csv', sep=';', encoding='utf-8', index=True)


# check if id already in df['id']


def check_if_id_exists(id, mps_df):

    logging.info("Checking if id exists in df['id']...")

    if id in mps_df['id'].values:
        logging.info(f"ID {id} exists in df['id'], skipping...")
        return True

    else:
        logging.info(f"ID {id} does not exist in df['id'], adding...")
        return False


# insert mp to df
def insert_mp_to_df(mp, mps_df):

    logging.info("Inserting mp to df...")

    # append mp data to mps_df
    new_df = mps_df.append(mp.to_df, ignore_index=True)

    # log inserting data
    logging.info("Data inserted successfully for MP: ", mp._name, mp._surname)

    # return updated dataframe
    return new_df
