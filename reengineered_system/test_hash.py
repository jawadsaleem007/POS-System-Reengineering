from werkzeug.security import generate_password_hash, check_password_hash

password = "1"
hashed = generate_password_hash(password)
print(f"Password: {password}")
print(f"Hash: {hashed}")
print(f"Check: {check_password_hash(hashed, password)}")
