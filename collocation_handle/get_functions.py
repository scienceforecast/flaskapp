from . import db_adaptor
from . import pd_func
from . import support

import os
import json

import pandas as pd


def get_from_primary(primary_domain):
    """
    Функция возвращает датафрейм со словосочетаниями
    """
    primary_domain_name = url_form_to_name(primary_domain)
    query_list = db_adaptor.primary_select_collocations(primary_domain_name)
    
    if query_list is None:
        return None

    df = pd_func.query_to_df(query_list)
    dict_for_graphic = pd_func.output_for_page(df)
    return dict_for_graphic, primary_domain_name


def get_from_journal(journal_id):
    """
    Функция возвращает датафрейм со словосочетаниями
    """

    output = from_journal_for_forecast(journal_id)  # форма для форкаста
    if not output:
        return None
    df = output[0]  #
    
    journal_name = output[1]
    
    # prediction block
    for i in range(1, 5):
        collocataions = df.Collocation.unique()
        collocation_to_ts = {
        collocation: pd.Series(
            data=df.loc[df["Collocation"] == collocation, "records"].values,
            index=df.loc[df["Collocation"] == collocation, "Publication year"]
            ) for collocation in collocataions
        }
        for _, ts in collocation_to_ts.items():
            ts.index = pd.to_datetime(ts.index)
            ts.sort_index(inplace=True)
        predictions = {collocation: ts[-8:].median()
        for collocation, ts in collocation_to_ts.items()}

        for predict in predictions:
            dict_predict = {}
            
            dict_predict = {'Collocation': predict, 'Publication year': 2019,
                        'Publication quarter': f'Q{i}',
                        'records': predictions[predict]}
            # print(dict_predict)
            df = df.append(dict_predict, ignore_index=True)

    df.sort_values(by= ['Collocation', 'Publication year'])
    dict_for_graphic = pd_func.output_for_page(df)
    print(dict_for_graphic)

    return dict_for_graphic, journal_name

def from_journal_for_forecast(journal_id):

    output = db_adaptor.journal_select_collocations(journal_id)
    if not output:
        return None
    query_list = output[0]
    journal_name = output[1]
    return pd_func.query_to_df(query_list), journal_name # форма для форкаста
    

def url_form_to_name(domain_url):
    """
    Функция преобразует url в название согласно файлу
    """
    file_path = os.path.join(os.getcwd(), 'collocation_handle', 'domains.json')
    with open(file_path) as file:
        data = json.load(file)
    for super_domain in data:
        if domain_url == super_domain['url']:
            return super_domain['name']
        for domain in super_domain['domains']:
            if domain_url == domain['url']:
                return domain['name']
            for subdomain in domain['subdomains']:
                if domain_url == subdomain['url']:
                    return subdomain['name']

    return None

def get_list_for_super_domains():
    super_domain_list_total = db_adaptor.get_total_list_of_super_domains()
    super_domain_list_availabe = db_adaptor.get_available_list_of_super_domains()
    new_list = []
    for super_domain in super_domain_list_total:
        new_dict = {}
        
        for name in super_domain:
            if name in super_domain_list_availabe:
                new_dict['is available'] = True
            else:
                new_dict['is available'] = False
            new_dict['name'] = name
            new_dict['url'] = super_domain[name]
        new_list.append(new_dict)

    return new_list

def get_list_for_domains(super_domain_url):
    super_domain_name = url_form_to_name(super_domain_url)
    domain_list_total = db_adaptor.get_total_list_of_domains(super_domain_url)
    domain_list_availabe = db_adaptor.get_available_list_of_domains(super_domain_name)

    new_list = []
    for domain in domain_list_total:
        new_dict = {}
        
        for name in domain:
            if name in domain_list_availabe:
                new_dict['is available'] = True
            else:
                new_dict['is available'] = False
            new_dict['name'] = name
            new_dict['url'] = domain[name]
        new_list.append(new_dict)
    return new_list

def get_list_for_subdomains(super_domain_url, domain_url):
    super_domain_name = url_form_to_name(super_domain_url)
    domain_name = url_form_to_name(domain_url)
    subdomain_list_total = db_adaptor.get_total_list_of_subdomains(super_domain_url, domain_url)
    subdomain_list_availabe = db_adaptor.get_available_list_of_subdomains(domain_name)
    new_list = []
    for subdomain in subdomain_list_total:
        new_dict = {}
        
        for name in subdomain:
            if name in subdomain_list_availabe:
                new_dict['is available'] = True
            else:
                new_dict['is available'] = False
            new_dict['name'] = name
            new_dict['url'] = subdomain[name]
        new_list.append(new_dict)
    return new_list

def get_list_for_journals(subdomain_name):
    journal_list = db_adaptor.get_available_list_of_journals(subdomain_name)
    return journal_list

def get_journal_name(journal_id):
    return db_adaptor.get_journal_name(journal_id)