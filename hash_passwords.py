# ターミナルコマンドで実行
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


passwords = ['abc']  # ハッシュ化したいパスワードをここに入力
for pwd in passwords:
    print(f'{pwd}: {hash_password(pwd)}')
    