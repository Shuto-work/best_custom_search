import secrets

# 32バイトの16進文字列を生成
secret_key = secrets.token_hex(32)
print(secret_key)
