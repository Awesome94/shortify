[run]
omit =
    # omit anything in a .local directory anywhere
    */.local/*
    # omit everything in /usr
    /usr/*
    # omit this single file
    /Users/AWESOME/.virtualenvs/shortify/*
    utils/tirefire.py
    migrations/*
    models/*
