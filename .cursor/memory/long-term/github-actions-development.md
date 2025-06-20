
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
