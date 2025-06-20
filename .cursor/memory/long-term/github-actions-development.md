
## 2025-06-20 20:08:26
# GitHub Actions Development Best Practices

## 🧪 Critical Rule: Test Docker Commands Locally First

### The Golden Rule
**ALWAYS test Docker commands locally before pushing to GitHub Actions pipeline!**

### Why This Matters
- Docker context differs between local and CI/CD
- Volume mounts behave differently
- Working directories can cause confusion
- Path resolution varies between environments

### Testing Workflow for Docker Steps

1. **Build the image locally first:**
   ```bash
   docker build -t test-image-name .
   ```

2. **Test each command individually:**
   ```bash
   # Test basic functionality
   docker run --rm -v $PWD:/workspace -w /app -e PYTHONPATH=/app test-image-name python -c "import test"
   
   # Test file access
   docker run --rm -v $PWD:/workspace -w /workspace test-image-name ls -la
   ```

3. **Debug container contents:**
   ```bash
   # Check what's in the container
   docker run --rm test-image-name ls -la /app
   
   # Check what's in workspace volume
   docker run --rm -v $PWD:/workspace test-image-name ls -la /workspace
   ```

### Common Issues Found During Local Testing

#### Issue: ModuleNotFoundError
- **Problem**: PYTHONPATH not set correctly
- **Solution**: Add `-e PYTHONPATH=/app` to docker run command

#### Issue: File Not Found  
- **Problem**: Working directory mismatch
- **Solution**: Files in volume mount (`/workspace`) vs container (`/app`)
- **Fix**: Use correct `-w` (working directory) parameter

#### Issue: Import Path Problems
- **Problem**: Relative imports don't work in container context  
- **Solution**: Use absolute imports or adjust PYTHONPATH

### Real Example From cursor-intelligent-memory Project

**Problem Found**: 
```bash
# This failed:
docker run -w /app test-image python test_discovery.py
# Error: can't open file '/app/test_discovery.py': No such file exists

# Root cause: test_discovery.py was in workspace volume, not container
```

**Solution Applied**:
```bash
# Working command:
docker run -v $PWD:/workspace -w /workspace -e PYTHONPATH=/app test-image python test_discovery.py
```

**Key Learning**: 
- Use `/workspace` working directory for files from repo
- Use `/app` PYTHONPATH for installed Python modules
- Mount repo as volume to access test files

### Testing Checklist

Before pushing GitHub Actions with Docker steps:

- [ ] Build image locally
- [ ] Test each docker run command individually  
- [ ] Verify file paths and working directories
- [ ] Check environment variables are set
- [ ] Confirm imports work correctly
- [ ] Test with same volume mounts as CI/CD

### Time Saved
Testing locally prevented:
- Multiple failed CI/CD runs
- Debugging in GitHub Actions environment
- Trial-and-error pipeline commits
- Wasted CI/CD minutes

**Bottom Line**: 5 minutes of local testing saves hours of CI/CD debugging!

## 2025-06-20 20:13:06

## 🚀 Advanced: Validating Entire Workflows with `act`

### The Complete Validation Strategy

Beyond testing individual Docker commands, you should validate the **entire workflow** before pushing:

### 1. Install `act` (GitHub Actions local runner)

```bash
# macOS
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows (using choco)
choco install act-cli
```

### 2. Validate Workflow Syntax & Structure

```bash
# List all available workflows
act --list

# Dry-run a specific workflow (no actual execution)
act release -n -j release

# Dry-run with specific event trigger
act release -n
```

### 3. Act Validation Benefits

#### What `act` catches that Docker tests don't:
- **YAML syntax errors** in workflow files
- **Action version conflicts** (e.g., actions/checkout@v4 issues)
- **Environment variable** setup problems
- **Job dependencies** and execution order
- **Matrix strategy** configurations
- **Conditional steps** logic
- **Secrets and environment** availability

#### Real Example Output:
```bash
$ act release -n -j release
*DRYRUN* [Release and Publish/Build and Publish Release] ⭐ Run Set up job
*DRYRUN* [Release and Publish/Build and Publish Release] ⭐ Run Main Extract version from tag
*DRYRUN* [Release and Publish/Build and Publish Release] ⭐ Run Main Test Docker image
✅ All steps validated successfully!
```

### 4. Complete Validation Workflow

**Before pushing to GitHub:**

1. **Individual Docker commands** (as documented above)
   ```bash
   docker build -t test-image .
   docker run --rm -v $PWD:/workspace -w /app -e PYTHONPATH=/app test-image python -c "import test"
   ```

2. **Full workflow validation**
   ```bash
   act release -n -j release
   ```

3. **Environment-specific testing** (if needed)
   ```bash
   # Test with specific runner environment
   act release -n --platform ubuntu-latest=catthehacker/ubuntu:act-latest
   ```

### 5. Act Limitations to be Aware Of

- **Secrets**: Won't have access to real GitHub secrets
- **External services**: Can't connect to real external APIs  
- **Runners**: Uses Docker containers, not real GitHub runners
- **Timing**: Some timing-dependent operations may behave differently

### 6. Act Configuration Tips

Create `.actrc` file for consistent settings:
```bash
# .actrc
--platform ubuntu-latest=catthehacker/ubuntu:act-latest
--container-architecture linux/amd64
```

### 7. Integration with Development Flow

**Recommended validation sequence:**

```bash
# 1. Quick syntax check
act --list

# 2. Dry-run validation  
act release -n -j release

# 3. Docker command testing (if Docker steps exist)
docker build -t test-image .
docker run --rm -v $PWD:/workspace -w /app test-image python -c "import test"

# 4. Final push
git push origin main
```

### 8. Time Investment vs. Returns

- **Setup time**: 5 minutes (install act)
- **Per-workflow validation**: 30 seconds  
- **Bugs prevented**: Syntax errors, action conflicts, logic issues
- **CI/CD minutes saved**: Significant (especially for complex workflows)

### 🎯 Key Takeaway

**Use `act` for workflow structure validation + Docker commands for functionality testing = Zero-failure pipelines!**

Example of issues caught by `act`:
- Missing required environment variables
- Incorrect job dependencies (`needs:` syntax)
- Action version incompatibilities  
- Matrix strategy configuration errors

This two-layer validation approach (act + docker) ensures both **structural correctness** and **functional correctness** before any CI/CD execution.
