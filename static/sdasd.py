import secrets
app.secret_key = secrets.token_hex(16)  # 32-character random key
