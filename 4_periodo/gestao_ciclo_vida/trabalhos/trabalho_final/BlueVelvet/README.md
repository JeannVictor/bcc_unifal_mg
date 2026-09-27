# Blue Velvet Music Store

![Java](https://img.shields.io/badge/Java-21-orange)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-brightgreen)
![Maven](https://img.shields.io/badge/Maven-build-C71A36)
![MySQL](https://img.shields.io/badge/MySQL-8-blue)

Trabalho final da disciplina de Gestão do Ciclo de Vida de Software. Aplicação web para uma loja de discos/produtos musicais, construída com Spring Boot, implementando autenticação de usuários e gerenciamento de categorias de produtos (com suporte a categorias hierárquicas, ex: Music > subcategorias).

---

## Funcionalidades

- Cadastro e login de usuários (`AuthController`, `AuthService`), com página web de login e registro.
- Gerenciamento de categorias de produtos (`CategoryController`, `CategoryService`), incluindo categorias pai/filho.
- Dashboard web (`WebDashboardController`) para visualização após login.
- Documentação de API via springdoc-openapi (Swagger UI).

---

## Tech Stack

| Tecnologia | Função |
|---|---|
| Java 21 | Linguagem principal |
| Spring Boot 3.5 (Web) | Framework backend e endpoints REST |
| Spring Data JPA | Persistência no banco de dados |
| Thymeleaf | Renderização das páginas web |
| MySQL | Banco de dados relacional |
| Lombok | Redução de código repetitivo |
| springdoc-openapi | Documentação automática via Swagger |
| Maven | Build e gerenciamento de dependências |

---

## Como Rodar

### Pré-requisitos

- MySQL rodando localmente na porta `3306`, com um banco chamado `db` e um usuário `gestao` / senha `gestao-pass` (ou ajuste `src/main/resources/application.yaml` conforme o seu ambiente).

### Compilar e rodar

O projeto inclui o Maven Wrapper, não sendo necessário instalar o Maven separadamente:

```bash
./mvnw clean install
./mvnw spring-boot:run
```

A aplicação sobe por padrão em `http://localhost:8080`.

---

## Endpoints

| Rota | Descrição |
|---|---|
| `/login` | Página web de login |
| `/register` | Página web de cadastro |
| `/dashboard` | Dashboard após login |
| `/api/auth` | API REST de autenticação |
| `/api/categories` | API REST de categorias |

---

## Observações

O schema é criado/atualizado automaticamente pelo Hibernate (`ddl-auto: update`) e os dados iniciais de categorias são populados via `data.sql` na inicialização.
