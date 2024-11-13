from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from pydantic import BaseModel

# 가상의 데이터베이스
fake_users_db = {
    "johndoe": {
        "username": "johndoe",  
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashed_secret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashed_secret2",
        "disabled": True,
    },
}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# 임시로 비밀번호를 암호화하는 함수
def fake_hash_password(password: str):
    return "fakehashed_" + password



@app.post("/token")
def login(form_data : OAuth2PasswordRequestForm = Depends()):
    # 데이터베이스에서 유저를 검색한다. (이미 가입된 유저여야함)
    user_dict = fake_users_db.get(form_data.username)

    # 가입된 유저가 없다면 에러를 발생시킨다.
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # 유저가 있는 상태에서 비밀번호가 있는지 확인한다. 
    hashed_password = fake_hash_password(form_data.password)

    # 해시된 비밀번호와 다르다면 에러를 발생시킨다. 
    if not hashed_password == user_dict["hashed_password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # 유저가 존재하고 비밀번호가 맞다면 즉, 인증이되었다면 토큰을 발행한다.
    #return user_dict
    return {"access_token": user_dict["username"], "token_type": "bearer"}

########################################################
# 여기서부터 인증된 사용자만 들어갈 수 있는 위치

# 유저를 확인하는 함수
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return user_dict


# 토큰을 해체하는 함수
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

# 현재 토큰을 넘겨준 유저의 정보를 가져온다. 
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 토큰을 해체하여 정보를 얻는다. 
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# 유저가 토큰을 넘겨주었고 유저의 정보가 파악되었음 
# 만기된 유저이면 비활성 유저라고 알려주고
# 사용가능한 유저이면 현 유저를 다시 전달해줌
# 현 예제에서 jondoe는 사용가능 유저이며
# alice는 사용불가능 유저이다.
async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return current_user


if __name__ == "__main__":
    uvicorn.run("oauth:app", reload=True)