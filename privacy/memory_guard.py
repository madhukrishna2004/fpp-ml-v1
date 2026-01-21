def wipe(obj):
    try:
        if isinstance(obj, list):
            obj.clear()
    except Exception:
        pass
