# INF1407-Servidor

### Grupo: Julia Rocha - 1710735

# Servidor Web

O servidor está configurado por default na porta 8080 e aceita requisições GET para arquivos contidos na pasta raiz. Caso um arquivo não seja encontrado, será exibida uma página de erro 404. 

## Como instalar

1. Clone o repositório:

````
git clone https://github.com/juliarocha/INF1407-Servidor.git
````

2. Cheque o arquivo de configuração para a o caminho correto para o diretório físico.

3. Rode o comando:

```
python3 server.py
```

4. Acesse o servidor em:

```
localhost:{porta}
```

5. Para fazer requisições de arquivos:

```
localhost:{porta}/{nome_do_arquivo}.{extensão_do_arquivo}
```


## Testes realizados:


| Teste | Status| 
|--------|-----------|
| Requisições de arquivos existentes no diretório raiz | Ok |
| Requisições de arquivos não existentes no diretório raiz | Ok |
| Exibição de erro ao configurar de maneira errada | Ok |
| Multiconexões | Ok |
| Erro de decodificação | Não testado |
| Erro de SO | Não testado |