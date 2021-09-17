## Julia Affonso Figueiredo Rocha
## 1710635 

from sys import argv, stderr, exit
from socket import getaddrinfo, socket
from socket import AF_INET, SOCK_STREAM, AI_ADDRCONFIG, AI_PASSIVE
from socket import IPPROTO_TCP, SOL_SOCKET, SO_REUSEADDR
from posix import abort
import threading

from configs import DEFAULT_PAGES, NOT_FOUND_PAGE, SERVER_PORT

## Metodos vistos em aula
def getEnderecoHost(porta):
    try:
        enderecoHost = getaddrinfo(None, porta, family=AF_INET, type=SOCK_STREAM,
                                   proto=IPPROTO_TCP, flags=AI_ADDRCONFIG | AI_PASSIVE)
    except:
        print("Não obtive informações sobre o servidor (???)", file=stderr)
        abort()
    return enderecoHost

def criaSocket(enderecoServidor):
    fd = socket(enderecoServidor[0][0], enderecoServidor[0][1])
    if not fd:
        print("Não consegui criar o socket", file=stderr)
        abort()
    return fd

def setModo(fd):
    fd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return

def bindaSocket(fd, porta):
    try:
        fd.bind(('', porta))
    except:
        print("Erro ao dar bind no socket do servidor", porta, file=stderr)
        abort()
    return

def escuta(fd):
    try:
        fd.listen(0)
    except:
        print("Erro ao começar a escutar a porta", file=stderr)
        abort()
    print("Iniciando o serviço");
    return

def conecta(fd):
    (con, cliente) = fd.accept()
    print("Servidor conectado com", cliente)
    return con, cliente 

## Handler das requisicoes
def handler(con, cliente):

    ## Mensagem do Socket
    message = con.recv(1024).decode("utf-8")

    if not message:
        ## Fecha conexao
        con.close()
        abort()

    print(message)

    ## Separa metodo e arquivo
    request = message.splitlines()[0]
    method, path, protocol = request.split(' ')

    if (method != 'GET'):
        ## Erro metodo
        body = ''
        status_code = '501'

    else:
        print(f'Abrindo: {path}...\n')
        try:
            if path == '/':
                ## Pagina default
                with open(DEFAULT_PAGES[0], 'rb') as f:
                    body = f.read()
            else:
                ## Requisicao de arquivo
                with open(path[1:], 'rb') as f:
                    body = f.read()
            status_code = '200'

        except FileNotFoundError:
            ## Arquivo nao encontrado, carrega pagina 404
            with open(NOT_FOUND_PAGE, 'rb') as f:
                body = f.read()
            status_code = '404'

        except OSError:
            ## Erro sistema operacional
            body = ''
            status_code = '500'

        except UnicodeDecodeError:
            ## Erro decodificação
            body = ''
            status_code = '500'

    response_header = [
        f'Content-Length: {len(body)}',
        'Connection: close'
    ]

    con.send(
        (f'HTTP/1.1 {status_code}').encode("utf-8"))
    con.send(''.join(response_header).encode("utf-8"))
    con.send('\n\n'.encode("utf-8"))
    con.send(body)
    con.close()


def main():
    if not (isinstance(SERVER_PORT,int)  and isinstance(DEFAULT_PAGES,list) and isinstance(NOT_FOUND_PAGE,str) and (SERVER_PORT == 8080 or SERVER_PORT == 80)):
        print("Erro no arquivo de configs")
        exit()
    endereco = getEnderecoHost(SERVER_PORT)
    fpSocket = criaSocket(endereco)
    setModo(fpSocket)
    bindaSocket(fpSocket, SERVER_PORT)
    escuta(fpSocket)
    print("Servidor pronto na porta: ", SERVER_PORT)
    try:
        while(True):
            con, cliente = conecta(fpSocket)

            ## Thread para multiconexoes 
            new_thread = threading.Thread(group=None, target=handler, args=(con, cliente))
            new_thread.start()
    except:
        print("Erro na conexao\n")

if __name__ == '__main__':
    main()
