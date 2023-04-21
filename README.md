# Minha API

Este API é a parte backend da entrega do MVP para o primeiro sprint do  **Curso de Pós Graduação em Engenharia de software** 

 
## Pré-requisito
---
1)Git e Python instalado no desktop e/ou notebook   

2)Clonar o repositório https://github.com/Etyonamine/puc-rio-mvp-sprint-1-back-end.git

3)Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.

## Como executar 
---
É recomendado o uso de ambientes virtuais do tipo [virtualenv]
(https://virtualenpython -m venv .v.pypa.io/en/latest/).

1)Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.

2)Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.
```
    Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.
    2.1) $ pip install -r requirements.txt     

```

3)Para executar a API  basta executar:

3.1) Executado sem reload
```
    (env)$ flask run --host 0.0.0.0 --port 5000
```
3.2)Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
    (env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

4)Para acessar os serviços da api clique no link = [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

5)Selecione uma das opções : swagger / redoc / rapiDoc para visualizar via interface os serviços e métodos.
