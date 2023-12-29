import axiosInstance from '../helpers/axios_client';
import { ChatbotCreate, ChatbotResponse } from '../models/Chatbot';
import { HTTPValidationError } from "@/lib/urlslab-api/models/HttpError";

class ChatbotService {
  public async getChatbots(tenantId: number): Promise<ChatbotResponse[] | HTTPValidationError> {
    try {
      const response = await axiosInstance.get<ChatbotResponse[]>(`/v1/chatbots/${tenantId}`);
      return response.data;
    } catch (error) {
      return this.handleError<HTTPValidationError>(error);
    }
  }

  public async createChatbot(tenantId: number, chatbotData: ChatbotCreate): Promise<ChatbotResponse | HTTPValidationError> {
    try {
      const response = await axiosInstance.post<ChatbotResponse>(`/v1/chatbots/${tenantId}`, chatbotData);
      return response.data;
    } catch (error) {
      return this.handleError<HTTPValidationError>(error);
    }
  }

  public async getChatbot(tenantId: number, chatbotId: number): Promise<ChatbotResponse | HTTPValidationError> {
    try {
      const response = await axiosInstance.get<ChatbotResponse>(`/v1/chatbots/${tenantId}/${chatbotId}`);
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

export const chatbotService = new ChatbotService();