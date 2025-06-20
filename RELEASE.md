# 🚀 Release Process

Este documento descreve como criar releases e publicar imagens Docker para o Cursor Intelligent Memory MCP Server.

## 📋 Workflows Disponíveis

### 1. Development Build (`.github/workflows/docker-publish.yml`)
- **Trigger**: Push para `main` ou `develop`, Pull Requests
- **Propósito**: Builds de desenvolvimento e testes
- **Tags produzidas**: 
  - `dev` (branch main)
  - `develop` (branch develop)
  - `pr-123` (pull requests)
  - `main-abc1234` (commit hash)

### 2. Release Build (`.github/workflows/release.yml`)
- **Trigger**: Criação de release no GitHub
- **Propósito**: Publicação oficial de versões estáveis
- **Tags produzidas**:
  - `latest` (sempre a última release)
  - `1.2.3` (versão exata)
  - `1.2` (major.minor)
  - `1` (major)

## 🏷️ Como Criar uma Release

### Método 1: Via Makefile (Recomendado)
```bash
# Criar uma nova release
make create-release VERSION=1.0.0

# Listar releases existentes
make list-releases

# Deletar uma release (se necessário)
make delete-release VERSION=1.0.0
```

### Método 2: Via Git Manualmente
```bash
# Criar tag
git tag -a v1.0.0 -m "Release v1.0.0"

# Enviar tag para o repositório
git push origin v1.0.0
```

### Método 3: Via GitHub Web Interface
1. Vá para a página do repositório no GitHub
2. Clique em "Releases" → "Create a new release"
3. Digite a tag (ex: `v1.0.0`)
4. Adicione título and descrição da release
5. Clique em "Publish release"

## 🔄 Fluxo Automático de Release

Quando uma release é criada:

1. **GitHub Actions detecta** a criação da release
2. **Build multi-platform** (linux/amd64, linux/arm64)
3. **Testes automáticos** da imagem Docker
4. **Publicação** no GitHub Container Registry
5. **Atualização automática** do README.md com nova versão
6. **Relatório detalhado** no GitHub Actions

## 📦 Versionamento Semântico

Seguimos o [Semantic Versioning (SemVer)](https://semver.org/):

- **MAJOR** (1.0.0): Mudanças incompatíveis na API
- **MINOR** (0.1.0): Novas funcionalidades compatíveis
- **PATCH** (0.0.1): Bug fixes e correções

### Exemplos:
- `v1.0.0` - Primeira versão estável
- `v1.1.0` - Nova funcionalidade adicionada
- `v1.1.1` - Bug fix na versão 1.1.0
- `v2.0.0` - Mudança breaking na API

## 🐳 Como Usar as Imagens

### Versão Específica (Recomendado para produção)
```bash
docker pull ghcr.io/gabriel-dantas98/cursor-intelligent-memory:1.0.0
```

### Última Versão Estável
```bash
docker pull ghcr.io/gabriel-dantas98/cursor-intelligent-memory:latest
```

### Versão de Desenvolvimento
```bash
docker pull ghcr.io/gabriel-dantas98/cursor-intelligent-memory:dev
```

## 🔍 Verificar Releases Disponíveis

### Via GitHub Container Registry
```bash
# Listar todas as tags disponíveis
docker search ghcr.io/gabriel-dantas98/cursor-intelligent-memory
```

### Via GitHub API
```bash
curl -s https://api.github.com/repos/gabriel-dantas98/cursor-intelligent-memory/releases/latest
```

### Via Git
```bash
git tag -l | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+' | sort -V
```

## 🛠️ Comandos Make Disponíveis

```bash
# Release management
make create-release VERSION=1.0.0  # Criar nova release
make list-releases                  # Listar releases
make delete-release VERSION=1.0.0  # Deletar release

# Development
make build-image                    # Build local
make push-to-ghcr                  # Push manual
make login-ghcr                    # Login no registry

# Testing
make test-tools                    # Testar ferramentas
make test-actions                  # Testar com act
```

## ✅ Checklist de Release

Antes de criar uma release:

- [ ] **Código testado** e funcionando corretamente
- [ ] **README.md atualizado** com mudanças relevantes
- [ ] **Versionamento** seguindo SemVer
- [ ] **CHANGELOG** atualizado (se existir)
- [ ] **Tests** passando no CI/CD
- [ ] **Documentação** atualizada

## 🚨 Rollback de Release

Se precisar fazer rollback:

```bash
# Deletar release problemática
make delete-release VERSION=1.0.1

# Criar nova release com correção
make create-release VERSION=1.0.2
```

## 📈 Monitoramento

- **GitHub Actions**: Acompanhar builds em tempo real
- **Container Registry**: Verificar images publicadas
- **GitHub Releases**: Ver histórico e downloads

## 🆘 Troubleshooting

### Build falhou
1. Verificar logs no GitHub Actions
2. Testar build localmente: `make build-image`
3. Verificar se dependências estão atualizadas

### Imagem não aparece no Registry
1. Verificar se release foi criada corretamente
2. Confirmar permissões do GitHub Token
3. Verificar se workflow foi executado

### Tag já existe
```bash
# Deletar tag local e remota
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# Criar nova tag
make create-release VERSION=1.0.0
``` 
