from src import app
from flask import render_template
from flask import jsonify
from flask import request
from .hasura import query

@app.route("/")
def home():
    search_arg = request.args.get('search')
    result = {"ensembl":[]}
    is_search_page = False
    if search_arg:
        is_search_page = True
        result = query('''
            query {
              ensembl (where: {name: {_ilike: $ARG}}) {
                name
                ensembl_id
                start_bp
                end_bp
                chromosome_scaffold_name
              }
            }
        ''', {"ARG": "%"+search_arg+"%"})
    return render_template(
        'home.html',
        **{
            "search": is_search_page,
            "results": result['ensembl'],
        }
    )

@app.route("/genes/")
def genes():
    data = query('''
    query {
        gene {
            name
            protein_name
            ensembl_id
            uniprot_id
            mgi_id
            ncbi_id
        }
    }
    ''')

    return render_template(
        'list.html', genes=data['gene']
    )

@app.route("/gene/<name>")
def gene_details(name):
    data = query('''
        query {
            gene (where: {name: {_eq: $NAME}}) {
                name
                protein_name
                ensembl_id
                uniprot_id
                mgi_id
                ncbi_id
                
                ensembl{
                chromosome_scaffold_name
                start_bp
                end_bp
                transcript_count
                percentage_gc_content
                }
                go_cellular_component{
                go{
                    id
                    text
                }
                }
                go_molecular_function{
                go{
                    id
                    text
                }
                }
                go_biological_process{
                go{
                    id
                    text
                }
                }
                phenotypes{
                phenotype
                term
                definition
                }
            }
        }
    ''', {'NAME': name})

    if len(data['gene']) == 0:
        gene = {}
    else:
        gene = data['gene'][0]

    return render_template(
        'details.html',
        gene=gene
    )
