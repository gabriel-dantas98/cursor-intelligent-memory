# GitHub Actions Testing with act

Este documento explica como usar o `act` para testar as GitHub Actions localmente antes de fazer push para o repositório.

## O que é o act?

O `act` é uma ferramenta que permite executar GitHub Actions localmente usando Docker. Isso é extremamente útil para:

- **Feedback rápido**: Testar mudanças sem precisar fazer commit/push
- **Debugging**: Iterar rapidamente sobre problemas na pipeline
- **Desenvolvimento**: Criar e ajustar workflows localmente

## Instalação

### macOS (Homebrew)
```bash
brew install act
```

### Linux
```bash
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### Windows (Chocolatey)
```bash
choco install act-cli
```

### Via Makefile (recomendado)
```bash
make install-act
```

## Configuração

O projeto já está configurado com:

- **`.actrc`**: Configuração padrão do act (imagens medium-size)
- **`.secrets`**: Arquivo com secrets para teste (fake tokens)
- **`.gitignore`**: Exclusão dos arquivos sensíveis

## Como Usar

### 1. Listar workflows disponíveis
```bash
make test-actions
# ou
act --list
```

### 2. Testar build Docker (evento push)
```bash
make test-docker-build
# ou
act push --job build
```

### 3. Testar build em pull request
```bash
make test-pr-build
# ou
act pull_request --job build
```

### 4. Testar workflow específico
```bash
act -W .github/workflows/docker-publish.yml
```

### 5. Executar com dry-run (apenas mostra o que seria executado)
```bash
act --dryrun
```

### 6. Ver o grafo de execução
```bash
act --graph
```

## Pipeline Implementada

O workflow `docker-publish.yml` implementa:

1. **Trigger em**:
   - Push para `main` e `develop`
   - Tags com padrão `v*`
   - Pull requests para `main`

2. **Build multi-arquitetura**:
   - `linux/amd64`
   - `linux/arm64`

3. **Registro no GitHub Container Registry**:
   - `ghcr.io/[owner]/[repo]`

4. **Tags automáticas**:
   - `latest` (branch main)
   - `main`, `develop` (branches)
   - `v1.0.0` (tags semver)
   - `pr-123` (pull requests)
   - `main-abc1234` (commit SHA)

5. **Cache inteligente**:
   - Cache de layers do Docker
   - Reutilização entre builds

## Comandos Úteis

### Testar com event personalizado
```bash
act -e tests/sample-event.json
```

### Executar job específico
```bash
act --job build
```

### Ver logs detalhados
```bash
act --verbose
```

### Usar imagem personalizada
```bash
act -P ubuntu-latest=catthehacker/ubuntu:act-20.04
```

### Testar com secrets diferentes
```bash
act --secret-file .secrets.prod
```

## Limitações do act

Algumas funcionalidades não são suportadas:

- **Concurrency**: Controle de execução paralela
- **Vars context**: Variáveis de nível organizacional
- **GitHub context incompleto**: Alguns campos podem estar vazios
- **Serviços**: Containers de serviço podem ter comportamento diferente

## Dicas de Debugging

### 1. Usar dry-run primeiro
```bash
act --dryrun --verbose
```

### 2. Testar steps individualmente
```bash
act --job build --verbose
```

### 3. Entrar no container para debug
```bash
act --reuse
# Em outro terminal:
docker exec -it <container_id> /bin/bash
```

### 4. Ver variáveis de ambiente
Adicione step temporário no workflow:
```yaml
- name: Debug Environment
  run: env | sort
```

## Estrutura de Arquivos

```
.
├── .github/workflows/
│   └── docker-publish.yml    # Pipeline principal
├── .actrc                    # Configuração do act
├── .secrets                  # Secrets para teste (no git)
├── .gitignore               # Ignora arquivos sensíveis
└── docs/
    └── github-actions-testing.md  # Esta documentação
```

## Próximos Passos

1. **Instalar act**: `make install-act`
2. **Testar pipeline**: `make test-docker-build`
3. **Ajustar conforme necessário**: Modificar `.github/workflows/docker-publish.yml`
4. **Iterar**: Usar act para testar mudanças rapidamente
5. **Commit final**: Quando tudo estiver funcionando

## Links Úteis

- [Documentação oficial do act](https://nektosact.com/)
- [GitHub do act](https://github.com/nektos/act)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action) 
