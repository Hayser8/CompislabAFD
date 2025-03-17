from thelexer import scan, get_token

test_tokens = ["if", "(", "x", "+", "10", ")", ";"]
for token in test_tokens:
    try:
        tk, act, adv = get_token(token)
        print(f"Entrada: {token!r} -> {tk!r}, {act!r}, adv: {adv}")
    except Exception as e:
        print(f"Entrada: {token!r} -> Error: {e}")
