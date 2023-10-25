import anyio
import typer
from typing import List
from uuid import UUID
from rich.console import Console
from typing_extensions import Annotated
from auth.schemas.admin import User, UserCreate
from api._manage import (
    parse_object_as,
    create_user,
    delete_user,
    list_users,
    get_user,
)


console = Console()
app = typer.Typer(help="Manage Auth database with CLI 💻")
users_app = typer.Typer(help="Manage database users 👨")
app.add_typer(users_app, name="users")


@users_app.command("create", help="Create a normal user 👨")
def users_create(
    email: Annotated[str, typer.Option(help="User login email.")],
    password: Annotated[str, typer.Option(help="User login password.")],
) -> None:
    user_data = UserCreate(
        email=email,
        password=password,
        is_active=True,
        is_superuser=False,
    )
    created = anyio.run(create_user, user_data)
    console.print(parse_object_as(User, created, from_attributes=True))


@users_app.command("create-superuser", help="Create a superuser 🦸")
def users_createsuperuser(
    email: Annotated[str, typer.Option(help="User login email.")],
    password: Annotated[str, typer.Option(help="User login password.")],
) -> None:
    user_data = UserCreate(
        email=email,
        password=password,
        is_active=True,
        is_superuser=True,
    )
    created = anyio.run(create_user, user_data)
    console.print(parse_object_as(User, created, from_attributes=True))


@users_app.command("delete", help="Delete an existent user 🚨")
def users_delete(
    uid: Annotated[UUID, typer.Argument(help="User identifier.")]
) -> None:
    deleted = anyio.run(delete_user, uid)
    console.print(
        parse_object_as(User, deleted, from_attributes=True),
    )


@users_app.command("list", help="List current users 👥")
def users_list(
    offset: Annotated[int, typer.Option(help="Start index")] = 0,
    limit: Annotated[int, typer.Option(help="Page limit")] = 100,
) -> None:
    usrs = anyio.run(list_users, offset, limit)
    console.print(parse_object_as(List[User], usrs, from_attributes=True))


@users_app.command("get", help="Get user by UUID 👨")
def users_get(
    uid: Annotated[UUID, typer.Argument(help="User identifier.")]
) -> None:
    usrs = anyio.run(get_user, uid)
    console.print(parse_object_as(User, usrs, from_attributes=True))


if __name__ == "__main__":
    app()
