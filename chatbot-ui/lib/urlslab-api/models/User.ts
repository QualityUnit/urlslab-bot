interface RegisterUserRequest {
  email: string;
  password: string;
  username: string;
}

interface RegisterUserResponse {
  email: string;
  username: string;
}

interface LoginUserRequest {
  email: string;
  password: string;
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
}

interface UserResponse {
  email: string;
  username: string;
}
