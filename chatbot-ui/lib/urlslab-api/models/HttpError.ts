export interface ValidationErrorItem {
  loc: Array<string | number>;
  msg: string;
  type: string;
}

export interface HTTPValidationError {
  detail: ValidationErrorItem[];
}
