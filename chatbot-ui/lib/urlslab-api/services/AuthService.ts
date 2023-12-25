import {AxiosResponse} from "axios";
import axiosInstance from "../helpers/axios_client";


export class AuthService {
  public async registerUser(requestData: RegisterUserRequest): Promise<RegisterUserResponse> {
    try {
      const response: AxiosResponse<RegisterUserResponse> = await axiosInstance.post('/v1/users/', requestData);
      return response.data;
    } catch (error: any) {
      throw this.handleValidationError(error);
    }
  }

  public async loginUser(requestData: LoginUserRequest): Promise<TokenResponse> {
    try {
      const response: AxiosResponse<TokenResponse> = await axiosInstance.post('/v1/users/login', requestData);
      const { access_token, refresh_token } = response.data;
      this.setAuthToken(access_token);
      return { access_token, refresh_token };
    } catch (error: any) {
      throw this.handleValidationError(error);
    }
  }

  public async getUser(): Promise<UserResponse> {
    try {
      const response: AxiosResponse<UserResponse> = await axiosInstance.get('/v1/users/me');
      return response.data;
    } catch (error: any) {
      throw this.handleValidationError(error);
    }
  }

  private setAuthToken(token: string): void {
    axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  private handleValidationError(error: any): Error | HTTPValidationError {
    if (error && error.response && error.response.data && error.response.data.detail) {
      return error.response.data as HTTPValidationError;
    }
    return error;
  }
}
