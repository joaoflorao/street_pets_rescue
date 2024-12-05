# Street Pets Rescue
MVP de uma aplicação web para cadastro, adoção e acompanhamento de animais em situação de vulnerabilidade.

## Pré-requisitos

- **Python 3.8 (ou superior)** **Docker** e **Docker Compose** instalados.

## Configuração
1- Crie um arquivo .env na raiz do projeto e configure de acordo com as configurações do seu banco de dados. 
(necessário somente na primeira execução). 

Neste projeto, o arquivo .env já está criado e configurado com parâmetros
fictícios apenas para demonstrar as funcionalidades do projeto.

**OBS: Lembre-se de nunca deixar credenciais expostas no código ou enviar o arquivo .env para o repositório.**

```
# Database Config
DB_USER=_YOUR_DB_USER_
DB_PASSWORD=_YOUR_DB_PASS_
DB_NAME=_YOUR_DB_NAME_
DB_PORT=5432
CONTAINER_DB_PORT=5432
DATABASE_URL=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@db:${DB_PORT}/${DB_NAME}

# Application Config
SECRET_KEY=_YOUR_APPLICATION_SECRET_KEY_
APP_PORT=5000
CONTAINER_APP_PORT=5000
```
**Observações:** Lembre-se de alterar o valor das variáveis de acordo com o banco de dados que deseja utilizar, 
os valores mostrados acima são apenas para exemplo.

2- Persistência dos dados da aplicação

Caso o banco de dados não exista, ele será criado com usuário, senha e nome do db informados no arquivo .env.

Para utilizar um banco de dados externo, ajuste as seguintes configurações no arquivo **docker-compose.yml**:
- Remova o serviço do banco de dados: No arquivo docker-compose.yml, exclua a configuração do serviço db 
(ou qualquer nome que esteja usando para o container do banco de dados).

- Ajuste as dependências do serviço da aplicação web: Remova a linha **depends_on** associada ao serviço web. 
Como o banco de dados não será gerenciado pelo Docker, não há necessidade de aguardar seu início. 
A aplicação irá se conectar ao banco externo ao ser inicializada.

3- Iniciando a aplicação

```
docker-compose up
```

4- A aplicação estará disponível em http://localhost:5000 (ou a porta especificada em APP_PORT).

## Comandos úteis
Parar os containers:
```
docker-compose down
```

Reconstruir os containers (após alterações no código ou nas dependências):
```
docker-compose up --build
```

## Resolvendo principais problemas
Ao rodar essa aplicação com Docker Compose, podem ocorrer alguns conflitos comuns. Veja alguns cenários e como resolvê-los:

**Conflito de porta com PostgreSQL local**:
Se você já tiver uma instância do PostgreSQL rodando localmente na mesma porta (5432 ou porta definida no arquivo .env), 
isso pode causar um conflito. Você pode resolver isso de duas maneiras: 
- Alterando a porta do container: Mude a porta exposta do PostgreSQL no arquivo .env
- Parando o PostgreSQL local: Pare o serviço PostgreSQL local temporariamente 
se ele não for necessário durante o uso do container. Você pode fazer isso com o comando: 
```
systemctl stop postgresql
``` 


**Conflito com portas locais:**
Caso outras aplicações já estejam usando as portas configuradas (por exemplo, 5000 para a aplicação Flask), 
você pode alterar a porta externa no arquivo .env, definindo outra porta para acessar a aplicação. Exemplo: 5001:5000.


**Volume existente ou em uso:**
Se você já tiver um volume com o mesmo nome criado anteriormente, 
pode ocorrer um erro ao tentar recriar ou remover esse volume. 
Para resolver isso, remova o volume manualmente, garantindo que ele não esteja em uso. 
Você pode fazer isso com os comandos:
```
docker volume ls                    # lista os volumes
docker volume rm <nome_do_volume>   # Remove o volume informado
```


**Containers existentes com o mesmo nome:**
Se existirem containers com o mesmo nome o Docker Compose pode tentar recriá-los e falhar. 
Para resolver isso, pare e remova os containers antigos antes de subir a aplicação novamente.
Você pode fazer isso com o comando:
```
docker-compose down
```