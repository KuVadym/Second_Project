from typing import List
from typing import Optional
from utils.regex import check_phone, check_birthday

from fastapi import Request


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("registerName")
        self.email = form.get("registerEmail")
        self.password = form.get("registerPassword")  


    async def is_valid(self):
        if not self.username or not len(self.username) > 3:
            self.errors.append("Username should be > 3 chars")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False      


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None


    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "loginEmail"
        )  # since outh works on username field we are considering email as username
        self.password = form.get("loginPassword")


    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


class ContactCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.name: Optional[str] = None
        self.email: Optional[str] = None
        self.birth_date: Optional[str] = None
        self.address: Optional[str] = None
        self.phones: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.birth_date = form.get("birth_date")
        self.address = form.get("address")
        self.email = form.get("emails")
        self.phones = form.get("phones")  

    async def is_valid(self):
        if check_phone(self.phones) == False:
            self.errors.append("Phone is not correct!\nCorrect form is: 0801234567 ")
        if not self.errors:
            return True
        return False      


class ContactDeleteForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.id: Optional[str] = None
        self.code: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.id = form.get("id")
        self.code = form.get("code")


class ContactUpdateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.name: Optional[str] = None
        self.email: Optional[str] = None
        self.birth_date: Optional[str] = None
        self.address: Optional[str] = None
        self.phones: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("new_name")
        self.birth_date = form.get("new_birth_date")
        self.address = form.get("new_address")
        self.email = form.get("new_emails")
        self.phones = form.get("new_phones")  