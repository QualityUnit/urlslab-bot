import axiosInstance from '../helpers/axios_client';
import { TenantCreate, TenantResponse } from '../models/Tenant';
import { HTTPValidationError } from "@/lib/urlslab-api/models/HttpError";

class TenantService {
  public async getTenants(): Promise<TenantResponse[] | HTTPValidationError> {
    try {
      const response = await axiosInstance.get<TenantResponse[]>('/v1/tenants/');
      return response.data;
    } catch (error) {
      return this.handleError<HTTPValidationError>(error);
    }
  }

  public async createTenant(tenantData: TenantCreate): Promise<TenantResponse | HTTPValidationError> {
    try {
      const response = await axiosInstance.post<TenantResponse>('/v1/tenants/', tenantData);
      return response.data;
    } catch (error) {
      return this.handleError<HTTPValidationError>(error);
    }
  }

  public async getTenant(tenantId: number): Promise<TenantResponse | HTTPValidationError> {
    try {
      const response = await axiosInstance.get<TenantResponse>(`/v1/tenants/${tenantId}`);
      return response.data;
    } catch (error) {
      return this.handleError<HTTPValidationError>(error);
    }
  }

  private handleError<T>(error: any): T {
    if (error.response && error.response.data) {
      return error.response.data;
    } else {
      return error.message;
    }
  }
}

export const tenantService = new TenantService();
