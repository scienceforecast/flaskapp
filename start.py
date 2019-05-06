from collocation_handle import get_functions
#import psycopg2
from flask import Flask, render_template
import os



app = Flask(__name__)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/list')
def list_super_domains():
    super_domains_list = get_functions.get_list_for_super_domains()
    return render_template('super_domains-list.html',
                           list_of=super_domains_list,
                           urlfor = 'list_domains')   

@app.route('/<primary_domain_url>')
def list_domains(primary_domain_url):
    domains_list = get_functions.get_list_for_domains(primary_domain_url)
    super_domain_name = get_functions.url_form_to_name(primary_domain_url)
    super_domain = {'name': super_domain_name, 'url': primary_domain_url}
    return render_template('domains-list.html',
                           list_of=domains_list,
                           super_domain = super_domain)


@app.route('/<super_domain_url>/<domain_url>')
def list_subdomains(super_domain_url, domain_url):
    subdomains_list = get_functions.get_list_for_subdomains(super_domain_url, domain_url)
    super_domain_name = get_functions.url_form_to_name(super_domain_url)
    super_domain = {'name': super_domain_name, 'url': super_domain_url}
    domain_name = get_functions.url_form_to_name(domain_url)
    domain = {'name': domain_name, 'url': domain_url}
    return render_template('subdomains-list.html',
                           list_of = subdomains_list,
                           super_domain = super_domain,
                           domain = domain)


@app.route('/<super_domain_url>/<domain_url>/<subdomain_url>')
def subdomain_view(super_domain_url, domain_url, subdomain_url):
    # Получение имен
    super_domain_name = get_functions.url_form_to_name(super_domain_url)
    domain_name = get_functions.url_form_to_name(domain_url)
    subdomain_name = get_functions.url_form_to_name(subdomain_url)

    super_domain = {'name': super_domain_name, 'url': super_domain_url}
    domain = {'name': domain_name, 'url': domain_url}
    subdomain = {'name': subdomain_name, 'url': subdomain_url}
    if not (bool(super_domain_name) & bool(domain_name) & bool(subdomain_name)):
        return render_template('404.html', text='Incorrect subdomain path')

    journals = get_functions.get_list_for_journals(subdomain_name)

    return render_template('journals-list.html',
                            list_of = journals,
                            super_domain = super_domain,
                            domain = domain,
                            subdomain = subdomain)



@app.route('/<super_domain_url>/<domain_url>/<subdomain_url>/<int:journal_id>')
def get_journal(super_domain_url, domain_url, subdomain_url, journal_id):
    # Получение имен
    super_domain_name = get_functions.url_form_to_name(super_domain_url)
    domain_name = get_functions.url_form_to_name(domain_url)
    subdomain_name = get_functions.url_form_to_name(subdomain_url)

    # Проверка наличия такого пути
    if not (bool(super_domain_name) & bool(domain_name) & bool(subdomain_name)):
        return render_template('404.html', text='Incorrect journal path')
    # Для формирования ссылок
    super_domain = {'name': super_domain_name, 'url': super_domain_url}
    domain = {'name': domain_name, 'url': domain_url}
    subdomain = {'name': subdomain_name, 'url': subdomain_url}
    
    
    result = get_functions.get_from_journal(journal_id)
    if result is None:
        return render_template('404.html', text='Incorrect journal id')
    output = result[0]
    journal_name = result[1]
    journal = {'name': journal_name, 'url': journal_id}
    names = {'super_domain': super_domain_name, 'domain': domain_name, 'subdomain': subdomain_name, 'journal': journal_name}
    urls = {'super_domain': super_domain_url, 'domain': domain_url, 'subdomain': subdomain_url, 'journal': journal_id}

    return render_template('journal-graph.html', output=output,
                            super_domain = super_domain,
                            domain = domain,
                            subdomain = subdomain,
                            journal = journal)

if __name__ == "__main__":
    app.run()

