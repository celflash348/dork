import os
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def google_search(query, num_results=5, verbose=False):
    url = f'https://www.google.com/search?q={query}&num={num_results}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    if verbose:
        print(f'Haciendo solicitud a URL: {url}')
    response = requests.get(url, headers=headers)
    if verbose:
        print(f'Estado de la respuesta: {response.status_code}')
    if response.status_code == 200:
        if verbose:
            print('Solicitud exitosa, parseando el contenido HTML...')
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='g')
        if verbose:
            print(f'Número de resultados encontrados: {len(results)}')
        links = []
        for i, result in enumerate(results[:num_results]):
            try:
                link = result.find('a')['href']
                links.append(link)
                if verbose:
                    print(f'Resultado {i+1}: {link}')
            except Exception as e:
                if verbose:
                    print(f'Error al extraer enlace del resultado {i+1}: {e}')
        return links
    else:
        print(f'Error al realizar la búsqueda: {response.status_code}')
        return []

def save_results_to_file(links, filename):
    with open(filename, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

def create_folder_tree_and_save_file(url, content):
    parsed_url = urlparse(url)
    path = os.path.join(parsed_url.netloc, *parsed_url.path.split('/')[1:])
    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    
    if os.path.exists(directory):
        base, ext = os.path.splitext(directory)
        directory = f"{base}1{ext}"
    
    os.makedirs(directory, exist_ok=True)
    
    with open(os.path.join(directory, filename), 'wb') as file:
        file.write(content)

def download_files(links, verbose=False):
    for link in links:
        if verbose:
            print(f'Descargando {link}...')
        try:
            response = requests.get(link)
            if response.status_code == 200:
                create_folder_tree_and_save_file(link, response.content)
                if verbose:
                    print(f'Descargado y guardado en {link}')
            else:
                if verbose:
                    print(f'Error al descargar {link}: Estado {response.status_code}')
        except Exception as e:
            if verbose:
                print(f'Error al descargar {link}: {e}')

def main():
    parser = argparse.ArgumentParser(description='Script para realizar búsquedas en Google y manejar resultados.')
    parser.add_argument('-q', '--query', required=True, help='Consulta de búsqueda.')
    parser.add_argument('-e', '--export', help='Archivo para exportar los resultados.')
    parser.add_argument('-r', '--results', default='5', help='Número de resultados a obtener (o "all" para todos).')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verboso para mostrar detalles.')
    parser.add_argument('-f', '--folder', action='store_true', help='Crea un árbol de carpetas según la URL.')
    parser.add_argument('-d', '--download', action='store_true', help='Descarga las URLs y guarda en la estructura de carpetas correspondiente.')

    args = parser.parse_args()

    num_results = int(args.results) if args.results.isdigit() else 100 if args.results == 'all' else 5
    links = google_search(args.query, num_results=num_results, verbose=args.verbose)

    if args.export:
        save_results_to_file(links, args.export)

    if args.folder and args.download:
        download_files(links, verbose=args.verbose)

    for i, link in enumerate(links, start=1):
        print(f'Resultado {i}: {link}')

if __name__ == '__main__':
    main()
