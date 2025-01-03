# AutoSync

AutoSync é um sistema desenvolvido para oficinas mecânicas e microempreendedores, projetado para oferecer uma visão geral do negócio. O sistema inclui funcionalidades como dashboards, envio de e-mails para clientes, gerenciamento de tarefas e controle de operações. Construído com Django, PostgreSQL, RabbitMQ e Celery, ele foi otimizado para funcionar em ambientes Docker.

## Funcionalidades

- **Dashboards:** Visualização intuitiva dos dados do negócio.
- **Envio de E-mails:** Notificações automatizadas para clientes.
- **Gerenciamento e Controle:** Ferramentas para otimizar a operação do dia a dia.
- **Processamento Assíncrono:** Execução de tarefas em segundo plano com Celery.
- **Mensageria:** Integração com RabbitMQ para gerenciamento de filas.
- **Banco de Dados:** Armazenamento estruturado usando PostgreSQL.

## Requisitos

Certifique-se de ter os seguintes requisitos instalados:

- Docker
- Docker Compose

## Configuração do Ambiente

1. Clone este repositório:
   ```bash
   git clone https://github.com/strvictor/AutoSync.git
   cd AutoSync
   ```

2. Configure as variáveis de ambiente:
   Copie o arquivo `.env-exemplo` e renomeie para `.env`. Atualize os valores conforme sua configuração:
   ```bash
   cp .env-exemplo .env
   ```

   Exemplo do conteúdo do arquivo `.env`:
   ```env
   # Configurações de Email
   EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST='smtp.seuprovedor.com'
   EMAIL_PORT='587'
   EMAIL_HOST_USER='seu_email@dominio.com'
   EMAIL_HOST_PASSWORD='sua_senha'
   EMAIL_USE_TLS='True'

   # Configurações do Banco de Dados
   POSTGRES_DB=nome_do_banco
   POSTGRES_USER=usuario_do_banco
   POSTGRES_PASSWORD=senha_do_banco
   DB_HOST=db-postgres

   # Configurações do RabbitMQ
   RABBITMQ_DEFAULT_USER=usuario_rabbitmq
   RABBITMQ_DEFAULT_PASS=senha_rabbitmq

   # Configurações do Celery
   CELERY_BROKER_URL=amqp://usuario:senha@host:porta//
   ```

3. Inicie os contêineres com Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Acesse a aplicação:
   - A aplicação web estará disponível em [http://localhost:8000](http://localhost:8000)

## Testes

Execute os testes para garantir que tudo esteja funcionando corretamente:
```bash
docker-compose run web python manage.py test
```

## Estrutura do Projeto

- **Django:** Backend principal do sistema.
- **PostgreSQL:** Banco de dados relacional para armazenar informações estruturadas.
- **RabbitMQ:** Sistema de mensageria para processamento assíncrono.
- **Celery:** Executor de tarefas assíncronas.

## Contribuição

Fique à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades. Siga as etapas abaixo para contribuir:

1. Fork este repositório.
2. Crie uma branch para sua contribuição:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Commit suas alterações:
   ```bash
   git commit -m "Adiciona nova funcionalidade"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin feature/nova-funcionalidade
   ```
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

## Contato

Para dúvidas ou sugestões, entre em contato:
- **Autor:** Paulo Victor
- **GitHub:** [strvictor](https://github.com/strvictor)

