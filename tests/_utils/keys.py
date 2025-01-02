def pressed_keys(*keys):
    key_list = [0] * 512  # Create a list of unpressed keys
    for key in keys:
        key_list[key] = 1
    return key_list
