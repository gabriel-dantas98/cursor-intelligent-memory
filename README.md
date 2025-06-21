# Cursor Intelligent Memory MCP Server

Sistema de memória inteligente para Cursor IDE que mantém contexto persistente entre sessões de desenvolvimento.

## O que faz?

- **Memória de 2 camadas**: Curto prazo (sessão atual) e longo prazo (conhecimento consolidado)
- **Reconhecimento de padrões**: Aprende com seus padrões de desenvolvimento
- **Prevenção de erros**: Lembra e evita problemas recorrentes
- **Integração com Cursor**: Funciona automaticamente com o IDE

## Instalação Rápida

### Via Docker (Recomendado)
```bash
# Configurar no .cursor/mcp.json
{
  "mcpServers": {
    "memory-docker": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "./:/workspace",
        "-w", "/workspace",
        "ghcr.io/gabriel-dantas98/cursor-intelligent-memory:0.0.4"
      ],
      "cwd": "."
    }
  }
}
```

### Via Python
```bash
git clone https://github.com/gabriel-dantas98/cursor-intelligent-memory.git
cd cursor-intelligent-memory
pip install -e .

# Configurar no .cursor/mcp.json
{
  "mcpServers": {
    "memory": {
      "command": "python",
      "args": ["-m", "memory_mcp_server.server"],
      "env": {
        "CURSOR_MEMORY_BASE_PATH": "/Users/gabriel.dantas/git/gdantas/cursor-intelligent-memory"
      }
    },
  }
}
```

## Como usar?

1. **Configure** uma das opções acima no `.cursor/mcp.json`
2. **Reinicie** o Cursor
3. **Comece a conversar** - o sistema criará automaticamente:
   ```
   .cursor/memory/
   ├── short-term/working-memory.md    # Memória da sessão
   └── long-term/
       ├── project-knowledge.md        # Conhecimento consolidado
       └── known-issues.md            # Problemas conhecidos
   ```

## Ferramentas Disponíveis

- `validate_memory_system` - Valida configuração do sistema de memória
- `get_memory_prompt_for_current_state` - Retorna prompts baseados no estado atual
- `list_memory_files` - Lista arquivos de memória com metadados
- `load_memory_files` - Carrega conteúdo dos arquivos de memória
- `memory_update` - Atualiza arquivos de memória com novo conteúdo

## Desenvolvimento

```bash
# Instalar dependências e testar ferramentas
make test-tools

# Desenvolvimento com MCP Inspector
make dev

# Build da imagem Docker
make build-image

# Publicar no GitHub Container Registry  
make push-to-ghcr

# Comandos auxiliares
make install          # Instalar dependências
make run             # Executar servidor MCP
make clean           # Limpar artefatos de build
make test-actions     # Testar GitHub Actions localmente
make login-ghcr       # Login no GitHub Container Registry
make install-act      # Instalar act para testes locais
```

## Como funciona?

O sistema funciona como memória humana:
- **Curto prazo**: Informações da sessão atual (volátil)
- **Longo prazo**: Padrões e conhecimento consolidado (persistente)
- **Promoção automática**: Padrões recorrentes (3+ vezes) viram conhecimento permanente

## Repositório

- **GitHub**: https://github.com/gabriel-dantas98/cursor-intelligent-memory
- **Docker**: `ghcr.io/gabriel-dantas98/cursor-intelligent-memory:0.0.4`
- **Licença**: MIT
