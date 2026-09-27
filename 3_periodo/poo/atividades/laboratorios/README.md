# Labs de POO

![Java](https://img.shields.io/badge/Java-orange?logo=openjdk&logoColor=white)
![Maven](https://img.shields.io/badge/Maven-C71A36?logo=apachemaven&logoColor=white)

Mini-projetos Maven desenvolvidos nos laboratórios da disciplina de Programação Orientada a Objetos.

---

## Estrutura

| Caminho | Descrição |
|---|---|
| `lab10.pdf` | Enunciado do laboratório 10 (sem resolução na pasta) |
| `respostas_labs/` | Enunciados e resoluções dos laboratórios 1 a 9 |

---

## respostas_labs/

| Pasta | Conteúdo |
|---|---|
| `lab_1_4/` | Laboratórios introdutórios (escolha de IDE, uso do Maven). Contém apenas os PDFs dos enunciados (`lab1.pdf` a `lab4.pdf`) e um resumo (`resumo.txt`); não há exercícios de código nesses. |
| `lab_5/` a `lab_9/` | A partir daqui os laboratórios têm exercícios práticos de código. Cada subpasta contém o PDF do enunciado e um ou mais mini-projetos Maven (com `pom.xml`) implementando o exercício. |

### Tópicos cobertos em cada lab

| Lab | Tópico |
|---|---|
| `lab_5/encapsulamento_versao1_2_3` | Encapsulamento e versionamento de classes |
| `lab_5/banco`, `lab_6/banco` | Modelagem de conta bancária e cliente |
| `lab_7/banco`, `lab_8/banco`, `lab_9/banco` | Evolução do modelo de conta bancária e cliente |
| `lab_8/banco`, `lab_9/banco` | Herança com conta corrente/poupança |
| `lab_9/banco/.../relatorios` | Pacotes e relatórios |

---

## Como compilar e rodar

Cada `lab_N` é um exercício independente. Para compilar e rodar um deles, entre na subpasta do projeto (a que contém o `pom.xml`) e use os comandos padrão do Maven:

```bash
mvn compile
mvn exec:java -Dexec.mainClass="org.example.NomeDaClassePrincipal"
```

Ou, para gerar um jar executável, conforme configurado no `pom.xml` de cada projeto:

```bash
mvn package
```
