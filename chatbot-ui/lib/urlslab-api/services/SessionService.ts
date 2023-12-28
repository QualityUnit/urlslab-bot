import axiosInstance from '../helpers/axios_client';
import {ChatCompletionRequest, Completed, DocumentSource, SessionResponse,} from '../models/Session';
import {HTTPValidationError} from "@/lib/urlslab-api/models/HttpError";
import {UrlslabStream} from "@/lib/urlslab-api/helpers/urlslab-stream";
import {AIStream} from "ai";

class SessionService {
  apiKey: string;
  baseURL: string;

  public constructor() {
    this.apiKey = process.env.URLSLAB_BOT_API_KEY as string;
    this.baseURL = process.env.NEXT_PUBLIC_URLSLAB_BOT_BASE_URL as string;
  }

  // Create a session
  public async createSession(tenantId: number, chatbotId: number): Promise<SessionResponse | HTTPValidationError> {
    try {
      const response = await axiosInstance.put<SessionResponse>(`/v1/sessions/${tenantId}/${chatbotId}`);
      return response.data;
    } catch (error) {
      return this.handleError<HTTPValidationError>(error);
    }
  }

  // Delete a session
  public async deleteSession(sessionId: string): Promise<Completed | HTTPValidationError> {
    try {
      const response = await axiosInstance.delete<Completed>(`/v1/sessions/${sessionId}`);
      return response.data;
    } catch (error) {
      return this.handleError<HTTPValidationError>(error);
    }
  }

  // Get the last source of a session
  public async getSessionLastSource(sessionId: string): Promise<DocumentSource | HTTPValidationError> {
    try {
      const response = await axiosInstance.get<DocumentSource>(`/v1/sessions/${sessionId}/sources`);
      return response.data;
    } catch (error) {
      return this.handleError<HTTPValidationError>(error);
    }
  }

  // Stream Chatbot Response (assuming this operation returns a specific type, here we use `any`)
  public async streamChatbotResponse(sessionId: string, chatCompletionRequest: ChatCompletionRequest): Promise<any> {
    // using simple fetch just for streaming
    return await fetch(`${this.baseURL}/v1/sessions/${sessionId}/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey
      },
      body: JSON.stringify(chatCompletionRequest)
    });
  }

  // Handle Axios errors, returning the expected error type
  private handleError<T>(error: any): T {
    if (error.response) {
      // The server responded with a status code that falls out of the range of 2xx
      // and with a response payload
      return error.response.data;
    } else {
      // Something happened in setting up the request or no response was received

      throw error;
    }
  }

}

// Export the service
export const sessionService = new SessionService();