# Clear Streamlit Cache

If you're experiencing issues with the web interface not picking up code changes, you need to clear Streamlit's cache.

## Quick Fix

1. **Stop the Streamlit server** (Ctrl+C in the terminal)

2. **Clear the cache:**
   ```powershell
   streamlit cache clear
   ```

3. **Restart Streamlit:**
   ```powershell
   streamlit run src/cq_agent/web/app.py --server.address localhost --server.port 8501
   ```

## Alternative: Delete Cache Manually

If the command doesn't work, manually delete the cache:

1. Navigate to: `C:\Users\YOUR_USERNAME\.streamlit\cache`
2. Delete all files in that directory
3. Restart Streamlit

## Why This Happens

Streamlit caches function results and code to improve performance. When you make code changes, sometimes the cache needs to be cleared for changes to take effect.

