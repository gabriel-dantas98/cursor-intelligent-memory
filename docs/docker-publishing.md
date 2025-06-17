# Docker Publishing Guide

Este documento explica como publicar imagens Docker tanto localmente quanto via GitHub Actions.

## GitHub Container Registry (ghcr.io)

Este projeto está configurado para publicar automaticamente no GitHub Container Registry.

### Configuração Automática (GitHub Actions)

A pipeline em `.github/workflows/docker-publish.yml` publica automaticamente quando:

- **Push para `main`**: Cria tag `latest` 
- **Push para `develop`**: Cria tag `develop`
- **Tags `v*`**: Cria tags semver (`v1.0.0`, `1.0`, `1`)
- **Pull Requests**: Apenas build (não publica)

### Tags Automáticas

| Evento | Tag Criada | Exemplo |
|--------|------------|---------|
| Push main | `latest` | `latest` |
| Push develop | `develop` | `develop` |
| Tag `v1.0.0` | `v1.0.0`, `1.0`, `1` | `v1.0.0` |
| PR #123 | `pr-123` | `pr-123` |
| Commit SHA | `{branch}-{sha}` | `main-abc1234` |

## Publicação Local

### 1. Configuração Inicial

```bash
# Ver informações calculadas automaticamente
make build-for-ghcr
```

Isso mostra:
- **Registry**: `ghcr.io`
- **User**: Extraído do remote git
- **Repo**: Nome do repositório atual
- **Image**: `ghcr.io/{user}/{repo}`

### 2. Login no GitHub Container Registry

```bash
# Login interativo (recomendado)
make login-ghcr

# Ou manual
echo $GITHUB_TOKEN | docker login ghcr.io -u {seu-usuario} --password-stdin
```

**Onde conseguir o token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Criar novo token com escopo `write:packages`
3. Copiar e usar no login

### 3. Build e Push

```bash
# Build + Push em um comando
make publish

# Ou separadamente:
make build-for-ghcr     # Apenas build
make push-to-ghcr       # Build + push
```

### 4. Comandos Avançados

```bash
# Publicar versão específica
make publish TAG=v1.0.0

# Ver variáveis calculadas
make -n build-for-ghcr

# Apenas build local
make build-image TAG=dev
```

## Usando a Imagem Publicada

### Pull da imagem

```bash
# Última versão
docker pull ghcr.io/{user}/cursor-intelligent-memory:latest

# Versão específica
docker pull ghcr.io/{user}/cursor-intelligent-memory:v1.0.0
```

### Executar

```bash
# Executar diretamente
docker run -it ghcr.io/{user}/cursor-intelligent-memory:latest

# Com volume montado (para projetos)
docker run -it -v $(pwd):/workspace ghcr.io/{user}/cursor-intelligent-memory:latest

# Como MCP server
docker run -p 8000:8000 ghcr.io/{user}/cursor-intelligent-memory:latest
```

### Usar no Cursor MCP Config

```json
{
  "mcpServers": {
    "memory": {
      "command": "docker",
      "args": [
        "run", "--rm", 
        "-v", "$(pwd):/workspace", 
        "-w", "/workspace",
        "ghcr.io/{user}/cursor-intelligent-memory:latest"
      ]
    }
  }
}
```

## Troubleshooting

### Erro de autenticação

```bash
# Verificar login
docker info | grep Username

# Re-fazer login
make login-ghcr
```

### Erro de permissão

1. Verificar se o token tem escopo `write:packages`
2. Verificar se o repositório permite packages
3. Verificar se está logado no usuário correto

### Imagem não aparece no GitHub

1. Ir para GitHub → Seu Repo → Packages
2. Se primeira vez, pode demorar alguns minutos
3. Verificar se o push foi bem-sucedido

## Comandos Úteis

```bash
# Ver todas as tags da imagem
docker images | grep cursor-intelligent-memory

# Ver informações da imagem
docker inspect ghcr.io/{user}/cursor-intelligent-memory:latest

# Limpar imagens antigas
docker image prune -f

# Ver repositório remoto
git config --get remote.origin.url
```

## Automatização Completa

Para configurar CI/CD completo:

1. **Desenvolvimento**: Usar `make build-image` localmente
2. **Testing**: Usar `act` para testar GitHub Actions
3. **Staging**: Push para `develop` → imagem `develop`
4. **Production**: Tag `v*` → imagem versionada + `latest`

## Próximos Passos

1. **Primeiro deploy**: `make publish`
2. **Configurar Cursor**: Atualizar MCP config
3. **Versionamento**: Usar tags git para releases
4. **CI/CD**: Configurar branch protection rules 
