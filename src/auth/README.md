# Auth microservice

## General endpoints
- **Superuser**:
  - `POST /users/`: Create an user
  - `GET /users/`: List users
  - `GET /users/{uid}`: Get an user by `uuid`
  - `PATCH /users/{uid}`: Update an user by `uuid`
  - `DELETE /users/{uid}`: Delete an user by `uuid`
  
- **Logged user**:
  - `GET /users/me/`: Get current user info
  - `DELETE /users/me/`: Delete current user
  - `POST /users/set-password/`: Set password for current user
- **Anonymous**:
  - `POST /users/register/`: Register an user
  - `POST /users/activate/`: Activate an user
  - `POST /users/resend-activation/`: Resend activation email

## Endpoints detail

### Superuser

#### `POST /users/`
Create an user

- **Body**:
  - `email`: Required
  - `password`: Required
  - `is_active`: Optional. Default to `false`
  - `is_superuser`: Optional. Default to `false`

- **Responses**:
  - `HTTP_201_CREATED`: User created object
  - `HTTP_400_BAD_REQUEST`: If something wrong


#### `GET /users/`
List current user

- **Responses**:
  - `HTTP_200_OK`: List of users


#### `GET /users/{uid}`
Get an specific user by `uuid`.

- **Path**:
  - `uid`: User uuid.

- **Responses**:
  - `HTTP_200_OK`: Founded user
  - `HTTP_404_NOT_FOUND`: If user not found


#### `PATCH /users/{uid}`
Update an user by `uuid`.

- **Path**:
  - `uid`: User uuid.

- **Body**:
  - `email`: Optional.
  - `is_active`: Optional.
  - `is_superuser`: Optional.
  - `password`: Optional.
  
- **Responses**:
  - `HTTP_200_OK`: Updated user
  - `HTTP_400_BAD_REQUEST`: If something wrong


#### `DELETE /users/{uid}`
Delete an user by `uuid`.

- **Path**:
  - `uid`: User uuid.

- **Responses**:
  - `HTTP_200_OK`: Deleted user.
  - `HTTP_400_BAD_REQUEST`: If something wrong

### Logged

#### `GET /users/me/`
Get current user

- **Responses**:
  - `HTTP_200_OK`: Current user info


#### `DELETE /users/me/`
Delete current user

- **Body**:
  - `password`: Required.

- **Responses**:
  - `HTTP_200_OK`: Current user deleted


#### `POST /users/set-password/`
Update current user password

- **Body**:
  - `password`: Required.

- **Responses**:
  - `HTTP_200_OK`: Current user info


### Anonymous

#### `POST /users/register/`
Register an inactive user and send activation email

- **Body**:
  - `email`: Required
  - `password`: Required

- **Responses**:
  - `HTTP_201_CREATED`: User created object
  - `HTTP_400_BAD_REQUEST`: If something wrong


#### `POST /users/activate/`
Activate an inactive user with `uuid` and `token`

- **Body**:
  - `uid`: Required
  - `token`: Required

- **Responses**:
  - `HTTP_200_OK`: User activated object
  - `HTTP_400_BAD_REQUEST`: If something wrong


#### `POST /users/resend-activation/`
Resend user activation mail

- **Body**:
  - `email`: Required.

- **Responses**:
  - `HTTP_200_OK`: Confirm data
  - `HTTP_400_BAD_REQUEST`: If something wrong