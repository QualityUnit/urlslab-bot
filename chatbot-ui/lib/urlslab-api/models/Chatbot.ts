export interface ChatbotCreate {
  title: string;
  system_prompt: string;
  chat_model_class: string;
  chat_model_name: string;
}

export interface ChatbotResponse {
  title: string;
  system_prompt: string;
  chat_model_class: string;
  chat_model_name: string;
  id: number;
}
