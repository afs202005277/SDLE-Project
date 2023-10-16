from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_email_or_pwd_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

private_info_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Trying to access private user information",
    headers={"WWW-Authenticate": "Bearer"},
)

private_info_ws_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Trying to access private workspace information",
    headers={"WWW-Authenticate": "Bearer"},
)

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="The resource you are looking for cannot be found",
    headers={"WWW-Authenticate": "Bearer"},
)