from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

# инициализация приложения FastAPI
app = FastAPI(
    title="User Management API",
    description="Простой REST API для управления пользователями",
    version="1.0.0"
)

# База данных пользователей
users_db: Dict [int, dict] = {}
next_id = 1 # счётчик ID


# Модель валидации данных пользователя
class User(BaseModel):
    name: str
    email: str
    age: int


# Pydantic модель для обновления (опционально)
class UserUpdate(BaseModel):
    name: str | None=None
    email: str | None=None
    age: int | None=None


# Эндпоинт 1: Создание нового пользователя
@app.post("/users/", response_model=User, status_code=201)
def create_user(user: User):
    global next_id
    user_dict = user.model_dump()
    users_db[next_id] = user_dict
    created_user = {**user_dict, "id": next_id}
    next_id += 1
    return created_user

#Эндпоинт 2: Получение пользователя по ID: (GET)
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_data = users_db[user_id]
    return {**user_data, "id": user_id}


#Эндпоинт 3: Получение списка всех пользователей (GET)
@app.get("/users/   ", response_model=List[User])
def list_users():
    return list(users_db.values())


#Эндпоинт 4: Обновление пользователя (PUT)
@app.put(   "/users/{user_id}", response_model=User)
def update_user(user_id: int,user_update: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    existing_user = users_db[user_id]

    #Обновляем только те поля, которые переданы
    updated_data = user_update.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        existing_user[key] = value


#Эндпоинт 5: Удаление пользователя (DELETE)
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    del users_db[user_id]
    return {"message": "Пользователь успешно удалён"}
