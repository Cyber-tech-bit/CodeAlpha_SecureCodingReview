# Secure Code Review Notes

## Scope
- Files reviewed: `insecure_app.py` and `secure_app.py`
- Method: manual inspection plus Bandit static analysis
- Environment: local educational demo only

## Findings

### SC-01 - Hard-coded password
- **Severity:** Medium
- **Location:** `DATABASE_PASSWORD`
- **Risk:** Secrets stored in source code can be exposed through repositories, backups, logs, or shared files.
- **Fix:** Use environment variables or a secret-management service. Do not commit credentials.

### SC-02 - Weak password hashing (MD5)
- **Severity:** High
- **Location:** `create_password_hash()`
- **Risk:** MD5 is fast and unsuitable for password storage, making password-guessing attacks more practical if hashes are exposed.
- **Fix:** Use a dedicated password-hashing method such as Argon2, bcrypt, scrypt, or PBKDF2 with a unique salt and appropriate work factor.

### SC-03 - Unsafe deserialization
- **Severity:** High
- **Location:** `load_preferences()`
- **Risk:** Deserializing untrusted data with `pickle` can execute attacker-controlled code.
- **Fix:** Use safe interchange formats such as JSON and validate the expected schema.

### SC-04 - Shell command injection risk
- **Severity:** High
- **Location:** `run_diagnostic()`
- **Risk:** Passing untrusted input to `subprocess.run(..., shell=True)` may allow unintended shell command execution.
- **Fix:** Avoid `shell=True`, pass an explicit argument list, and allow-list supported actions.

## Verification
Run:

```powershell
py -m pip install -r requirements.txt
py -m bandit -r insecure_app.py
```

Bandit analyses source code; it does not run the intentionally insecure demo functions.
