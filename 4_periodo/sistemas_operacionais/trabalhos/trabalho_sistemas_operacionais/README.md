# Simulador FAT - Sistema de Arquivos

![C](https://img.shields.io/badge/C-99-blue)

## Descrição

Simulador do sistema de arquivos FAT (File Allocation Table) desenvolvido para a disciplina de Sistemas Operacionais da UNIFAL-MG. O programa simula o gerenciamento de arquivos em disco usando listas encadeadas para representar a alocação de setores.

---

## Compilação e Execução

**Compilar o projeto:**

```bash
make
```

**Executar o simulador:**

```bash
./fat_simulator
```

**Limpar arquivos compilados:**

```bash
make clean
```

---

## Comandos do Simulador

| Comando | Descrição |
|---------|-----------|
| `G` | Gravar um novo arquivo |
| `D` | Deletar um arquivo existente |
| `A` | Apresentar conteúdo de um arquivo |
| `M` | Mostrar estruturas do sistema |
| `C` | Desfragmentar o disco |
| `H` | Exibir ajuda com todos os comandos |
| `F` | Sair do simulador |

---

## Estrutura do Projeto

```
fat_simulator/
├── main.c      # Programa principal e interface do usuário
├── fat.c       # Implementação das funções do sistema de arquivos
├── fat.h       # Definições de estruturas e protótipos
└── Makefile    # Script de compilação
```

---

## Informações Acadêmicas

- **Universidade**: UNIFAL-MG
- **Disciplina**: Sistemas Operacionais
- **Professor**: Romario
- **Alunos**: Jeann Victor Batista, Nicolas Rodrigues Texeira de Oliveira, Thallysson
