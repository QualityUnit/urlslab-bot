export interface SessionResponse {
  session_id: string; // Format: uuid
  created_at: string; // Description: Session created at, Example: "2021-09-24, 12:00:00"
}

export interface DocumentSource {
  source: string; // Description: Document source, Example: "document source"
  title: string; // Description: The title of the document, Example: "document title"
}

export interface Completed {
  status: string; // Example: "OK"
}

export interface ChatCompletionRequest {
  human_input: string; // Example: "human input"
}