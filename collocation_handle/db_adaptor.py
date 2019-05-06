import psycopg2
import json
import os

from .DBsettings import DB_SETTINGS


def primary_select_collocations(name):
    """
    Функция для запроса статистики по супердомену выводит список из кортежей вида
    (collocation, year, quarter)
    """
    connector= psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("""SELECT collocations.collocation, years.year, quarters.name FROM articles_collocations
                     JOIN collocations ON (collocations.id = articles_collocations.collocation_id)
                     JOIN articles ON (articles.id = articles_collocations.article_id)
                     JOIN years ON (years.id = articles.pub_year_id)
                     JOIN quarters ON (quarters.id = articles.pub_quarter_id)
                     WHERE articles_collocations.article_id IN (
                     SELECT id
                     FROM articles
                     WHERE journal_id IN (
                       SELECT id FROM journals WHERE id IN (
                         SELECT subdomain_id FROM subdomains_journals WHERE subdomain_id IN (
                           SELECT id FROM subdomains WHERE domain_id IN (
                             SELECT id from domains WHERE primary_id = (
                               SELECT id from primary_domains WHERE name = %s)
                              )
                           )
                         )
                       )
                     )
                """, (name, ))


    output_query = cur.fetchall()
    cur.close()
    connector.close()
    if not output_query:
        return None
    output = []
    for row in output_query:
        output.append(row)

    return output


def domain_select_collocations(name):
    """
    Функция для запроса статистики по домену выводит список из кортежей вида
    (collocation, year, quarter)
    """
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("""SELECT collocations.collocation, years.year, quarters.name FROM articles_collocations
                     JOIN collocations ON (collocations.id = articles_collocations.collocation_id)
                     JOIN articles ON (articles.id = articles_collocations.article_id)
                     JOIN years ON (years.id = articles.pub_year_id)
                     JOIN quarters ON (quarters.id = articles.pub_quarter_id)
                     WHERE articles_collocations.article_id IN (
                     SELECT id
                     FROM articles
                     WHERE journal_id IN (
                       SELECT id FROM journals WHERE id IN (
                         SELECT subdomain_id FROM subdomains_journals WHERE subdomain_id IN (
                           SELECT id FROM subdomains WHERE domain_id IN (
                             SELECT id from domains WHERE name = %s)
                           )
                         )
                       )
                     )
                """, (name, ))
    
    output_query = cur.fetchall()
    cur.close()
    connector.close()
    if not output_query:
        return None
    output = []
    for row in output_query:
        output.append(row)

    return output


def subdomain_select_collocations(name):
    """
    Функция для запроса статистики по поддомену выводит список из кортежей вида
    (collocation, year, quarter)
    """
    connector= psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("""SELECT collocations.collocation, years.year, quarters.name FROM articles_collocations
                     JOIN collocations ON (collocations.id = articles_collocations.collocation_id)
                     JOIN articles ON (articles.id = articles_collocations.article_id)
                     JOIN years ON (years.id = articles.pub_year_id)
                     JOIN quarters ON (quarters.id = articles.pub_quarter_id)
                     WHERE articles_collocations.article_id IN (
                     SELECT id
                     FROM articles
                     WHERE journal_id IN (
                       SELECT id FROM journals WHERE id IN (
                         SELECT subdomain_id FROM subdomains_journals WHERE subdomain_id IN (
                           SELECT id FROM subdomains WHERE name = %s)
                         )
                       )
                     )
                """, (name, ))
    
    output_query = cur.fetchall()
    cur.close()
    connector.close()
    if not output_query:
        return None
    output = []
    for row in output_query:
        output.append(row)

    return output

def journal_select_collocations(journal_id):
    """   
    Функция для запроса статистики по журналу выводит список из кортежей вида
    (collocation, year, quarter), а так же название журнала
    """
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("""SELECT collocations.collocation, years.year, quarters.name FROM articles_collocations
                     JOIN collocations ON (collocations.id = articles_collocations.collocation_id)
                     JOIN articles ON (articles.id = articles_collocations.article_id)
                     JOIN years ON (years.id = articles.pub_year_id)
                     JOIN quarters ON (quarters.id = articles.pub_quarter_id)
                     WHERE articles_collocations.article_id IN (
                     SELECT id
                     FROM articles
                     WHERE journal_id = %s)
                """, (journal_id, ))
    
    output_query = cur.fetchall()
    if not output_query:
        return None
    cur.execute("SELECT name FROM journals WHERE id = %s", (journal_id,))
    journal_name = cur.fetchone()[0]
    cur.close()
    connector.close()
    
    output = []
    for row in output_query:
        output.append(row)

    return output, journal_name

def get_total_list_of_super_domains():
    """
    возвращает список всех супер доменов
    в формате [{'Chemical Engineering': 'chemical-engineering'},
    {'Chemistry': 'chemistry'}]
    """
    file_path = os.path.join(os.getcwd(), 'collocation_handle', 'domains.json')
    total_super_domains = []
    with open(file_path) as file:
        data = json.load(file)
    for super_domain in data:
        total_super_domains.append({f'{super_domain["name"]}': f'{super_domain["url"]}'})

    return total_super_domains




def get_total_list_of_domains(superdomain_url_name):
    """
    возвращает список всех доменов в требуемом супердомене (разделе) в
    формате [{'Chemical Engineering': 'chemical-engineering'},
    {'Chemistry': 'chemistry'}]
    """
    total_list_of_domains = []
    file_path = os.path.join(os.getcwd(), 'collocation_handle', 'domains.json')
    with open(file_path) as f:
        data = json.load(f)
        for super_domain in data:
            print(super_domain['url'])
            if (super_domain['url'] == superdomain_url_name):
                for domain in super_domain['domains']:
                    total_list_of_domains.append({domain['name']: domain['url']})

    return total_list_of_domains


def get_total_list_of_subdomains(superdomain_url_name,
                                 domain_url_name):
    """
    возвращает список всех поддоменов в требуемом домене в
    формате [['Chemical Engineering', 'chemical-engineering'],
    ['Chemistry', 'chemistry']]
    """
    file_path = os.path.join(os.getcwd(), 'collocation_handle', 'domains.json')
    total_list_of_subdomains = []
    with open(file_path) as f:
        data = json.load(f)
        for super_domain in data:
            if (super_domain['url'] == superdomain_url_name):
                for domain in super_domain['domains']:
                    if domain['url'] == domain_url_name:
                        for subdomain in domain['subdomains']:
                            total_list_of_subdomains.append({subdomain['name']: subdomain['url']})

    return total_list_of_subdomains

def get_available_list_of_super_domains():
    """
    возвращает список всех супер доменов 
    в которых есть журналы в базе
    формате ['Chemical Engineering', 'Chemistry'}
    """
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("SELECT name FROM primary_domains")
    domains_list = []
    for domain in cur:
        domains_list.append(domain[0])
    return domains_list



def get_available_list_of_domains(primary_domain_name):
    """
    возвращает список всех доменов в требуемом супердомене (разделе),
    в которых есть журналы в базе
    формате ['Chemical Engineering', 'Chemistry'}
    """
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("SELECT name FROM domains WHERE primary_id = (SELECT id FROM primary_domains WHERE name = %s)", (primary_domain_name, ))
    domains_list = []
    for domain in cur:
        domains_list.append(domain[0])
    return domains_list



def get_available_list_of_subdomains(domain_name):
    """
    возвращает список всех поддоменов в требуемом домене,
    в которых есть журналы в базе
    формате ['Chemical Engineering', 'Chemistry'}
    """
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("SELECT name FROM subdomains WHERE domain_id = (SELECT id FROM domains WHERE name = %s)", (domain_name, ))
    output_query = cur.fetchall()
    cur.close()
    connector.close()
    print(output_query)
    if not output_query:
        return None
    output = []
    for row in output_query:
        output.append(row[0])

    return output


def get_available_list_of_journals(subdomain_name):
    """
    возвращает список всех журналов из базы в требуемом поддомене в
    формате [{'id': 'AASRI Procedia'}]
    """
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("""SELECT name, id FROM journals WHERE id IN ( 
                     SELECT journal_id FROM subdomains_journals 
                       WHERE subdomain_id = (SELECT id FROM subdomains WHERE name = %s))""", (subdomain_name, ))
    output_query = cur.fetchall()
    cur.close()
    connector.close()
    if not output_query:
        return None
    output = {}
    for row in output_query:
        output[f'{row[1]}'] = row[0]

    return output

def get_journal_name(journal_id):
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    cur.execute("SELECT name FROM journals WHERE id = %s", (journal_id,))
    journal_name = cur.fetch()[0]
    cur.close()
    connector.close()
    return journal_name

if __name__ == '__main__':
    print('Available super domains \n', get_available_list_of_super_domains())
    print('Available domains in Life Scinces\n', get_available_list_of_domains('Life Sciences'))
    print('Available subdomains in Biochemistry, Genetics and Molecular Biolog\n',get_available_list_of_subdomains("Biochemistry, Genetics and Molecular Biology"))
    print('Available journals in Ageing\n', get_available_list_of_journals("Ageing"))
    print('Total super domains\n', get_total_list_of_super_domains('domains.json'))
    print('Total domains in Life Scinces\n', get_total_list_of_domains('domains.json', 'life-sciences'))
    print('Total subdomains in Biochemistry, Genetics and Molecular Biology\n', get_total_list_of_subdomains('domains.json', 'life-sciences', 'biochemistry-genetics-and-molecular-biology'))
