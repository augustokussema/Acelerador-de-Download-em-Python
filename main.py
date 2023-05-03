'''
    Autor: Augusto Kussema
    GitHub: https://github.com/augustokussema
    Email: augusto.kussema@hotmail.com
    Geo: Luanda, Angola
'''

import augustokussema.pacote
import requests
import threading
import time
import os
from tqdm import tqdm


def download(www_url):
    # Define a URL do arquivo que deseja baixar
    url = www_url

    # Define o número de threads que serão usadas para fazer o download
    num_threads = 4

    # Define o tamanho do buffer em bytes
    buffer_size = 1024

    # Obtém o tamanho total do arquivo em bytes
    response = requests.head(url)
    total_size = int(response.headers.get('content-length', 0))

    # Calcula o tamanho de cada bloco de download em bytes
    block_size = int(total_size / num_threads) + 1

    # Define uma função para fazer o download de um bloco específico
    def download_block(start_byte, end_byte, thread_num, progress_bar):
        headers = {"Range": "bytes={}-{}".format(start_byte, end_byte)}
        r = requests.get(url, headers=headers, stream=True)

        # Abre o arquivo no modo "append binary" para escrever o bloco de download
        with open("parte{}.zip".format(thread_num), "ab") as f:
            for chunk in r.iter_content(buffer_size):
                f.write(chunk)
                progress_bar.update(len(chunk))

    # Cria uma barra de progresso com o tamanho total do arquivo
    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Download") as progress_bar:
        # Cria uma lista de threads e começa cada thread
        threads = []
        for i in range(num_threads):
            start_byte = block_size * i
            end_byte = min(start_byte + block_size, total_size)
            thread = threading.Thread(target=download_block, args=(start_byte, end_byte, i, progress_bar))
            thread.start()
            threads.append(thread)

        # Espera todas as threads terminarem
        for thread in threads:
            thread.join()

        # Junta todas as partes baixadas em um único arquivo
        with open("arquivo_final.zip", "wb") as f:
            for i in range(num_threads):
                with open("parte{}.zip".format(i), "rb") as part:
                    f.write(part.read())

        # Remove as partes individuais baixadas
        for i in range(num_threads):
            os.remove("parte{}.zip".format(i))

    return True

url = input('Informe a url do arquivo a ser transferido (https://): ')

if download(url) == True:
    print("Download completo!")
else:
    print('Ocorreu um erro durante a transferência.')
