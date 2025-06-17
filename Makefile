TAG ?= latest

.PHONY: help install dev run test test-tools clean build-image push-image

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo "Installing Memory MCP server dependencies..."
	pip install -e .

dev: ## Install development dependencies
	@echo "🔍 Starting Memory MCP server with Inspector..."
	DANGEROUSLY_OMIT_AUTH=true npx @modelcontextprotocol/inspector \
		python -m memory_mcp_server.server

run: ## Run the Memory MCP server
	@echo "Starting Memory MCP server..."
	python -m memory_mcp_server.server

test: ## Run tests (placeholder)
	@echo "Running Memory MCP server tests..."
	@echo "No tests implemented yet"

test-tools: ## Test Memory MCP server tool discovery
	@echo "🔍 Installing dependencies and testing Memory MCP server tool discovery..."
	@pip install -e . > /dev/null 2>&1
	@python3 test_discovery.py

clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	rm -rf dist/ build/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build-image: ## Build Docker image
	@echo "🔨 Building Memory MCP server Docker image..."
	docker build -t memory-mcp-server:$(TAG) .

push-image: build-image ## Build and push Docker image
	@echo "Pushing Memory MCP server Docker image..."
	docker push memory-mcp-server:$(TAG)

# GitHub Container Registry targets
GITHUB_REGISTRY = ghcr.io
GITHUB_REPO = $(shell basename $(shell git config --get remote.origin.url 2>/dev/null || echo "cursor-intelligent-memory") .git)
GITHUB_USER = $(shell git config --get remote.origin.url 2>/dev/null | sed -n 's|.*github.com[:/]\([^/]*\)/.*|\1|p' || echo "gdantas")
GITHUB_IMAGE = $(GITHUB_REGISTRY)/$(GITHUB_USER)/$(GITHUB_REPO)

login-ghcr: ## Login to GitHub Container Registry
	@echo "🔐 Logging into GitHub Container Registry..."
	@read -p "Enter your GitHub token: " token; \
	echo $$token | docker login $(GITHUB_REGISTRY) -u $(GITHUB_USER) --password-stdin

build-for-ghcr: ## Build image for GitHub Container Registry
	@echo "🔨 Building image for GitHub Container Registry..."
	docker build -t $(GITHUB_IMAGE):$(TAG) -t $(GITHUB_IMAGE):latest .

push-to-ghcr: build-for-ghcr ## Build and push to GitHub Container Registry
	@echo "📤 Pushing to GitHub Container Registry..."
	docker push $(GITHUB_IMAGE):$(TAG)
	docker push $(GITHUB_IMAGE):latest
	@echo "✅ Image pushed successfully!"
	@echo "📦 Image available at: $(GITHUB_IMAGE):$(TAG)"

publish: login-ghcr push-to-ghcr ## Login and publish to GitHub Container Registry

# act (GitHub Actions testing) targets
install-act: ## Install act for local GitHub Actions testing
	@echo "📦 Installing act for GitHub Actions testing..."
	@command -v brew > /dev/null && brew install act || \
	(command -v curl > /dev/null && curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash)

test-actions: ## Test GitHub Actions locally with act
	@echo "🎬 Testing GitHub Actions locally with act..."
	@command -v act > /dev/null || (echo "❌ act not installed. Run 'make install-act' first" && exit 1)
	act --list

test-docker-build: ## Test Docker build action locally
	@echo "🐳 Testing Docker build action locally..."
	@command -v act > /dev/null || (echo "❌ act not installed. Run 'make install-act' first" && exit 1)
	act push --job build

test-pr-build: ## Test pull request build locally
	@echo "🔀 Testing pull request build locally..."
	@command -v act > /dev/null || (echo "❌ act not installed. Run 'make install-act' first" && exit 1)
	act pull_request --job build

act-help: ## Show act help and available events
	@echo "📋 Available act commands:"
	@command -v act > /dev/null && act --help || echo "❌ act not installed. Run 'make install-act' first" 
