import pandas as pd

def query_to_df(query_list):
    df = pd.DataFrame(query_list, columns =  ['Collocation', 'Publication year', 'Publication quarter'])
    # Получение топ словосочетаний
    ser = df.groupby(['Collocation']).size().sort_values(ascending=False).nlargest(5)

    df = df.loc[df['Collocation'].isin(ser.keys())]  # фильтрация по топу
    new_df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0:'records'})
    # Получение датафрейма из топ 5 словосочетаний разбитые по кварталам
    new_df.sort_values(by=['Collocation', 'Publication year', 'Publication quarter', 'records'], ascending=False, inplace=True)
    normalize_range_data_frame(new_df)
    new_df = new_df[new_df['Publication year'] != 2019]
    return new_df

def output_for_page (df):
    """
    Функция вводит словарь вида
    {
        'years': [2010, ....],
        'collocation_name': {'records': , 'color':}
    }
    """

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]

    df = df.drop(columns=['Publication quarter'])
    col_dict = df.to_dict('list')

    output_dict = {'years': df['Publication year'].sort_values().unique()}
    for collocation, year, records in zip(col_dict['Collocation'], col_dict['Publication year'], col_dict['records']):
        if collocation in output_dict:
            print(collocation,'     ', records)
            if year in output_dict[collocation]['years']:
                ident = output_dict[collocation]['years'].index(year)
                output_dict[collocation]['records'][ident] += int(records)
            else:
                output_dict[collocation]['years'].append(year)
                output_dict[collocation]['records'].append(int(records))

        else:
            output_dict[collocation] = {'years': [year], 'records': [records]}
    i = 0
    # Приведение к возростающему виду
    for collocation in output_dict:
        if collocation == 'years':
            continue
        output_dict[collocation]['color'] = colors[i]
        output_dict[collocation]['records'].reverse()
        del output_dict[collocation]['years']
        i += 1
    print(output_dict)
    return output_dict

def normalize_range_data_frame(frame):
    """
    Functions gets a frame of sevaral years of type collocation, number, year.
    Adds to this frame zero number of collocations in year records when they
    were absent (Example: matrix ECM 0 2015, matrix ECM 0 2016)
    """
    collocations = frame['Collocation'].unique()
    years = frame['Publication year'].unique()
    quarters = frame['Publication quarter'].unique()
    for collocation in collocations:
        for year in years:
            for quarter in quarters:
                test_frame = frame.loc[(frame['Collocation'].isin([collocation])) &
                                   (frame['Publication year'].isin([year])) &
                                    (frame['Publication quarter'].isin([quarter]))]
                if test_frame.empty:
                    frame = frame.append({'Collocation': collocation,
                                          'Publication year': year,
                                          'Publication quarter': quarter,
                                          'records': 0}, ignore_index=True)

    return frame
